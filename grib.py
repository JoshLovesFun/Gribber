# Goal: Extract what we want from the GRIB files.

# HRRR GRIB Info Example:
# Key/Value: edition/2, centre/kwbc, date/20220105, dataType/fc,
# Key/Value: gridType/lambert, stepRange/0 typeOfLevel/hybrid,
# Key/Value: level/1, shortName/pres,
# Key/Value: packingType/grid_complex_spatial_differencing

import sys
import traceback
from collections import OrderedDict
from typing import Dict, List

from eccodes import (
    codes_grib_new_from_file, codes_grib_find_nearest,
    codes_get, codes_get_array, codes_release, CodesInternalError
)

from file_and_time_control import (delete_coordinates_file,
                                   nearest_coordinates_from_grib_files,
                                   match_strings_and_add_dummy_files)


def process_grib_files(working_directory_main, working_directory_grib,
                       processed_data, files):
    delete_coordinates_file(working_directory_main)
    match_strings_and_add_dummy_files(working_directory_grib)

    skip_file_path = "missing_file"
    grib_latitude = processed_data.get('latitude')
    grib_calculated_longitude = processed_data.get('calculated_longitude')

    results_grib_setup = []

    # for file_path in all_files_prs + all_files_nat: (add this later)
    for file_path in files:
        if skip_file_path in file_path:
            nearest_index = int(-999)
            nearest_distance = int(-999)
            nearest_lat = int(-999)
            nearest_lon = int(-999)
        else:
            with open(file_path, 'rb') as f:
                grib_message_handle = codes_grib_new_from_file(f)

                nearest_info = codes_grib_find_nearest(
                    grib_message_handle, grib_latitude,
                    grib_calculated_longitude, is_lsm=False, npoints=1)
                nearest_info_dict = nearest_info[0]

                nearest_lat = nearest_info_dict['lat']
                nearest_lon = nearest_info_dict['lon']
                nearest_distance = nearest_info_dict['distance']
                nearest_index = nearest_info_dict['index']

        rounded_distance = round(nearest_distance, 3)
        results_grib_setup.append((nearest_lat, nearest_lon,
                                   nearest_distance, nearest_index))
        print(f"File: {file_path} --> Data is {rounded_distance}"
              f" kilometers from the requested location and the chosen "
              f"grid cell is: {nearest_index}")

        # This is for coordinates output file.
        # Call the function without assigning its result to a variable.
        nearest_coordinates_from_grib_files(
            working_directory_main, [file_path],
            nearest_lat, nearest_lon)
    print("\n\n")

    return [item[3] for item in results_grib_setup]


def grib_dictionary_from_inputs(processed_data):
    # Define dictionary_for_grib with a type hint
    dictionary_for_grib: Dict[str, List[str]] = {}
    string_levels = [str(i) for i in range(1, 13)]

    if processed_data.get('BoundaryLayerHeight') == "yes":
        dictionary_for_grib.setdefault("blh", []).append("0")

    for height_levels, key_names, prefix in [
        (string_levels if processed_data.get('U_and_V_WindComponent') == "yes"
         else [], ["u", "v"], "Wind"),
        (string_levels if processed_data.get('Temperature') == "yes" else [],
         ["t"], "Temperature"),
        (string_levels if processed_data.get('TKE') == "yes" else [],
         ["tke"], "TKE"),
        (string_levels if processed_data.get('PRES') == "yes" else [],
         ["pres"], "PRES"),
        (string_levels if processed_data.get('SPFH') == "yes" else [],
         ["q"], "SPFH")
    ]:
        for level in height_levels:
            if processed_data.get(f"{prefix}HeightLevel{level}") == "yes":
                for key_name in key_names:  # Iterate over "u" and "v" for wind
                    if key_name not in dictionary_for_grib:
                        dictionary_for_grib[key_name] = []
                    dictionary_for_grib[key_name].append(f"{level}")

    # Now we are making 2 lists that populate based on the dictionary created.
    grib_short_name = []
    grib_level = []

    for key, values in dictionary_for_grib.items():
        if values:
            for value in values:
                grib_short_name.append(key)
                grib_level.append(value)
    print("\n\n")
    print(f'GRIB shortName list requested: {grib_short_name}')
    print(f'GRIB level list requested:     {grib_level}')
    print("\n\n")

    return grib_short_name, grib_level


# We use an ordered dictionary to be extra safe
# Function to populate the dictionary based on given inputs
def populate_files(prs_files, nat_files,
                   shortnames_for_prs, level_for_prs, grid_cell_for_prs,
                   hour_date_for_prs,
                   shortnames_for_nat, level_for_nat, grid_cell_for_nat,
                   hour_date_for_nat):
    # Initialize the dictionary
    test = {
        "prs": OrderedDict(),
        "nat": OrderedDict()
    }

    # Function to assign data to a given dictionary key
    def assign_data(file_list, key, shortnames, levels, grid_cells,
                    hour_dates):
        for i, file in enumerate(file_list):
            file_name = file
            test[key][file_name] = []

            for j, shortname in enumerate(shortnames):
                # Assign the corresponding grid_cell and hour_date
                # based on file index
                test[key][file_name].append(
                    (shortname, levels[j], grid_cells[i], hour_dates[i], None)
                )

    # Populate all three categories with their respective lists
    assign_data(prs_files, "prs", shortnames_for_prs, level_for_prs,
                grid_cell_for_prs, hour_date_for_prs)
    assign_data(nat_files, "nat", shortnames_for_nat, level_for_nat,
                grid_cell_for_nat, hour_date_for_nat)

    return test


def extract_grib_data(test):
    """Processes GRIB files using the provided dictionary
    and updates values."""
    for category, files in test.items():  # Loop over "prs", "nat", "sub"
        # Loop over each file in the category
        for file_name, data_entries in files.items():

            with (open(file_name, 'rb') as f):
                for idx, (shortName, level, grid_cell, hour_date, _
                          ) in enumerate(data_entries):
                    try:
                        f.seek(0)  # Reset the file pointer
                        info_found = False

                        while True:
                            gid = codes_grib_new_from_file(f)
                            if gid is None:
                                break  # End of file

                            # Check if the GRIB record matches our expected
                            # shortName and level
                            if (codes_get(gid, 'level') == int(level) and
                                    codes_get(gid, 'shortName')
                                    == shortName):

                                values = codes_get_array(gid, 'values')
                                if 0 <= grid_cell < len(values):
                                    value_at_index = values[grid_cell]
                                else:
                                    # Handle invalid grid index
                                    value_at_index = -9999.999

                                # Store the extracted value in place of None
                                test[category][file_name][idx] = (
                                    shortName, level, grid_cell, hour_date,
                                    value_at_index
                                )

                                print(
                                    f'File: {file_name} | Date: {hour_date[1]}'
                                    f' Time: {hour_date[0]}'
                                    f' | Var: {shortName} | Level: {level}'
                                    f' | Value: {value_at_index}')

                                info_found = True

                            codes_release(gid)  # Clean up the GRIB handle

                    except CodesInternalError as err:
                        handle_grib_error(err)

                    # If no matching data was found, store -9999.999
                    if not info_found:
                        test[category][file_name][idx] = (
                            shortName, level, grid_cell, hour_date, -9999.999
                        )

    # We should return something here.
    return test


def handle_grib_error(err):
    """Handle errors during GRIB file processing."""
    verbose = 1  # verbose error reporting
    if verbose:
        traceback.print_exc(file=sys.stderr)
    else:
        sys.stderr.write(err.msg + '\n')


def extract_time_info_from_grib_files(files):
    extracted_time_values = []

    for file_path in files:
        time = "Not_Available"  # Default value
        data_date = "Not_Available"  # Default value

        try:
            f = open(file_path, 'rb')
            gid = codes_grib_new_from_file(f)

            time = codes_get(gid, 'time')
            data_date = codes_get(gid, 'dataDate')

            codes_release(gid)
            f.close()

        except CodesInternalError as err:
            handle_grib_error(err)

        extracted_time_values.append((time, data_date))
        print(f"File: {file_path} --> The date is: {data_date}"
              f"--> The time is: {time}")

    return extracted_time_values

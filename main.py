import sys
import os
import output
import my_herbie
import grib
import file_and_time_control

import pprint

import constants
import read_control
from plot import plot_grib_temperature


def main():
    default_working_directory = "."
    if len(sys.argv) > 1:
        control_filename = sys.argv[1]
    else:
        control_filename = constants.default_control_filename
    return default_working_directory, control_filename


# Call the main function to get the working directory and control filename
default_working_directory, control_filename = main()

control_data = read_control.read_control_file(default_working_directory,
                                              control_filename)
processed_data = read_control.process_control_data(control_data)

dir_file_count = file_and_time_control.expected_file_count(processed_data)

working_directory_grib = processed_data.get('GRIB_files_location')
working_directory_main = processed_data.get('output_directory')
output_filename_with_inputs_used = processed_data.get('Input_Out_File')

# Create the full paths for both output files
output_file_path = os.path.join(working_directory_main,
                                output_filename_with_inputs_used)

if (processed_data.get('flow_options') not in
        ("h", "e", "hw", "hwa", "p", "ps")):
    print('Invalid input entered for "Flow:" option. Try again.')
    sys.exit(1)

output.print_input_data(processed_data)

# Write the processed input data to the specified file
output.write_processed_input_data_to_file(processed_data,
                                          output_file_path)


def handle_flow_option_e():
    """Handles the 'flow_options == "e"' case."""
    main_output = processed_data.get('main_output')

    # Call files_to_do_work_for and unpack its result
    all_files_prs, all_files_nat = file_and_time_control.files_to_do_work_for(
        working_directory_grib, processed_data)

    # First, we call the function with prs files.
    grid_cell_data_prs = grib.process_grib_files(working_directory_main,
                                                 working_directory_grib,
                                                 processed_data,
                                                 all_files_prs)

    # Now, we call the function with nat files.
    grid_cell_data_nat = grib.process_grib_files(working_directory_main,
                                                 working_directory_grib,
                                                 processed_data,
                                                 all_files_nat)

    # First, we call the function with prs files.
    extracted_time_values_prs = grib.extract_time_info_from_grib_files(
        all_files_prs)

    # Now, we call the function with nat files.
    extracted_time_values_nat = grib.extract_time_info_from_grib_files(
        all_files_nat)

    grib_short_name, grib_level = grib.grib_dictionary_from_inputs(
        processed_data)

    prs_files = ["file1.prs", "file2.prs", "file3.prs", "file4.prs"]
    sub_files = []  # No actual sub files, pass an empty list
    nat_files = ["file1.nat", "file2.nat", "file3.nat"]

    shortnames_for_prs = ["blh", "t", "t", "t", "other"]
    grid_cell_for_prs = [150, 150, 175, 121]
    level_for_prs = ["0", "1", "2", "11", "7"]
    hour_date_for_prs = [(11, 202501), (12, 202501), (13, 202501),
                         (14, 202501)]

    shortnames_for_nat = ["blh", "test"]
    grid_cell_for_nat = [140, 119, 140]
    level_for_nat = ["0", "15"]
    hour_date_for_nat = [(5, 202502), (6, 202502), (7, 202502)]

    shortnames_for_sub = ["v", "v", "v"]
    grid_cell_for_sub = [133, 130, 130]
    level_for_sub = ["5", "6", "9"]
    hour_date_for_sub = [(1, 202507), (2, 202507), (3, 202507)]

    test = grib.populate_files(
        all_files_prs, sub_files, all_files_nat,

        grib_short_name, grib_level, grid_cell_data_prs,
        extracted_time_values_prs,

        grib_short_name, grib_level, grid_cell_data_nat,
        extracted_time_values_nat,

        shortnames_for_sub, level_for_sub, grid_cell_for_sub,
        hour_date_for_sub
    )

    pprint.pprint(test)

    grib_data = grib.extract_grib_data(test)

    pprint.pprint(grib_data)

    # Build dictionary code, commented out
    # build_dict = {}
    # extracted_data = grib.extract_value_at_grid_index(
    #     all_files_prs,
    #     all_files_nat,
    #     grid_cell_data_prs,
    #     grib_short_name,
    #     grib_level,
    #     extracted_time_values,
    #     build_dict
    # )

    years, months, days, hours, hours_ending = (
        file_and_time_control.make_all_times(processed_data))

    # Commented out output part
    # DON'T WE NEED SUB FILES NAT AND PRS???????????????????
    output.write_all_data_new(
        years, months, days, hours, hours_ending,
        working_directory_main, main_output, dir_file_count, extracted_time_values_prs, extracted_time_values_nat,
        all_files_prs, all_files_nat, sub_files, grib_data
    )


# --- Main logic starts here ---
if processed_data.get('flow_options') in ("h", "hw", "hwa"):
    if processed_data.get('regional_subset') != "yes":
        my_herbie.fetch_herbie_data_in_range(processed_data)
    if processed_data.get('regional_subset') == "yes":
        # wgrib required
        print("do stuff")







elif processed_data.get('flow_options') == "e":
    handle_flow_option_e()

elif processed_data.get('flow_options') in ("p"):
    print("we always can do this if herbie was done")
    _, all_files_nat = file_and_time_control.files_to_do_work_for(
        working_directory_grib, processed_data)

    first_file_nat = all_files_nat[0] if all_files_nat else None
    print(first_file_nat)
    plot_grib_temperature(grib_file=rf"{first_file_nat}", variable_name="Temperature",
                          level=7)


elif processed_data.get('flow_options') in ("ps"):
    print("Will add this capability later")


if __name__ == "__main__":
    main()

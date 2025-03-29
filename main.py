import sys
import os
import output
import my_herbie
import grib
import file_and_time_control
from pathlib import Path
import pprint

import constants
import read_control
import region_subset
from plot import plot_grib_temperature


def main():
    default_working_dir = "."
    if len(sys.argv) > 1:
        local_control_filename = sys.argv[1]
    else:
        local_control_filename = constants.default_control_filename
    return default_working_dir, local_control_filename


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
        ("h", "e", "hw", "hwa", "p", "ps", "s",
         "del_r", "del_n", "del_p", "del_all")):
    print('Invalid input entered for "Flow:" option. Try again.')
    sys.exit(1)

if (processed_data.get('flow_options') in
        ("h", "e", "hw", "hwa")):
    output.print_input_data(processed_data)
else:
    pass

# Write the processed input data to the specified file
output.write_processed_input_data_to_file(processed_data,
                                          output_file_path)


def handle_flow_option_e():
    """Handles the 'flow_options == "e"' case."""
    main_output = processed_data.get('main_output')

    # Call files_to_do_work_for and unpack its result
    (all_files_prs, all_files_nat,
     all_files_sub) = file_and_time_control.files_to_do_work_for(
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

    # Finally, we call the function with sub files.
    grid_cell_data_sub = grib.process_grib_files(working_directory_main,
                                                 working_directory_grib,
                                                 processed_data,
                                                 all_files_sub)

    # First, we call the function with prs files.
    extracted_time_values_prs = grib.extract_time_info_from_grib_files(
        all_files_prs)

    # Now, we call the function with nat files.
    extracted_time_values_nat = grib.extract_time_info_from_grib_files(
        all_files_nat)

    # Finally, we call the function with sub files.
    extracted_time_values_sub = grib.extract_time_info_from_grib_files(
        all_files_sub)

    grib_short_name, grib_level = grib.grib_dictionary_from_inputs(
        processed_data)

    test = grib.populate_files(
        all_files_prs, all_files_nat, all_files_sub,

        grib_short_name, grib_level, grid_cell_data_prs,
        extracted_time_values_prs,

        grib_short_name, grib_level, grid_cell_data_nat,
        extracted_time_values_nat,

        grib_short_name, grib_level, grid_cell_data_sub,
        extracted_time_values_sub,
    )

    pprint.pprint(test)

    grib_data = grib.extract_grib_data(test)

    pprint.pprint(grib_data)

    years, months, days, hours, hours_ending, _ = (
        file_and_time_control.make_all_times(processed_data))

    # TODO all_files_prs, all_files_nat, all_files_sub_prs, all_files_sub_nat?
    # TODO We do not need to write any sub data to output if we think about it.
    output.write_all_data_new(
        years, months, days, hours, hours_ending,
        working_directory_main, main_output, dir_file_count,
        extracted_time_values_prs, extracted_time_values_nat,
        all_files_prs, all_files_nat, all_files_sub, grib_data
    )


# --- Main logic starts here ---
if processed_data.get('flow_options') in ("h", "hw", "hwa"):
    my_herbie.fetch_herbie_data_in_range(processed_data)

elif (processed_data.get('regional_subset') == "yes" and
        processed_data.get('flow_options') == "s"):

    _, _, _, _, _, num_days = (
        file_and_time_control.make_all_times(processed_data))
    total = num_days * dir_file_count

    # TODO Update names of functions so they make more sense if needed.
    all_files, _ = file_and_time_control.files_to_subset(
        working_directory_grib)

    if not all_files:
        print("No files available to process.")
        sys.exit(1)

    first_file_to_sub = all_files[0]

    wgrib2_path = processed_data.get('wgrib2_path')
    cygwin_path = processed_data.get('cygwin_path')

    wgrib2_path = rf"{wgrib2_path}"
    cygwin_path = rf"{cygwin_path}"

    for all_grib_files_to_subset in all_files:

        input_grib = all_grib_files_to_subset
        input_path = Path(input_grib)
        print(f"Input file: {input_path}")

        output_grib = input_path.parent / f"regional_{input_path.name}"
        print(f"Output file that has been regionally "
              f"subsetted: {output_grib}")

        lon_range = (-79, -67)
        lat_range = (37, 47)

        result = region_subset.process_grib_file(wgrib2_path,
                                                 input_grib, output_grib,
                                                 lon_range, lat_range,
                                                 cygwin_path)
        print(f"Operation: {result}")

elif processed_data.get('flow_options') == "e":
    handle_flow_option_e()

elif processed_data.get('flow_options') in ("p", "ps"):

    nat_files, sub_files = file_and_time_control.files_to_subset(
        working_directory_grib)
    first_file_sub = sub_files[0] if sub_files else None
    first_file_nat = nat_files[0] if nat_files else None

    if processed_data.get('flow_options') == "p":
        plot_grib_temperature(grib_file=rf"{first_file_nat}",
                              variable_name="Temperature",
                              level=7)
    if processed_data.get('flow_options') == "ps":
        plot_grib_temperature(grib_file=rf"{first_file_sub}",
                              variable_name="Temperature",
                              level=7)

elif (processed_data.get('flow_options') in
      ("del_r", "del_n", "del_p", "del_all")):
    # Ask for confirmation before proceeding.
    confirm = input(
        f"Are you sure you want to delete files based on "
        f"{processed_data.get('flow_options')}? (yes/no): ")

    if confirm.lower() == "yes":
        print(
            f"Will delete files based on {processed_data.get('flow_options')}")
        file_and_time_control.delete_files(working_directory_grib,
                                           processed_data.get('flow_options'))
    else:
        print("Deletion cancelled.")
else:
    print("Try to select valid combination of options in the control file.")


if __name__ == "__main__":
    main()

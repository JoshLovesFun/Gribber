import sys
import os
import output
import my_herbie
import grib
import file_and_time_control


import constants
import read_control


def main():
    default_working_directory = "."
    if len(sys.argv) > 1:
        control_filename = sys.argv[1]
    else:
        control_filename = constants.default_control_filename
    return default_working_directory, control_filename


# Call the main function to get the working directory and control filename
default_working_directory, control_filename = main()

control_data = read_control.read_control_file(default_working_directory, control_filename)
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



if processed_data.get('flow_options') in ("h", "hw", "hwa"):
    my_herbie.fetch_herbie_data_in_range(processed_data)





elif processed_data.get('flow_options') == "e":
    main_output = processed_data.get('main_output')

    # Call files_to_do_work_for and unpack its result
    all_files_prs, all_files_nat = file_and_time_control.files_to_do_work_for(
        working_directory_grib, processed_data)

    grid_cell_data = grib.process_grib_files(working_directory_main,
                                             working_directory_grib,
                                             processed_data,
                                             all_files_prs,
                                             all_files_nat)

    extracted_time_values = grib.extract_time_info_from_grib_files(
        all_files_prs, all_files_nat)

    grib_short_name, grib_level = grib.grib_dictionary_from_inputs(
        processed_data)

    build_dict = {}
    extracted_data = grib.extract_value_at_grid_index(
        all_files_prs,
        all_files_nat,
        grid_cell_data,
        grib_short_name,
        grib_level,
        extracted_time_values,
        build_dict
    )

    years, months, days, hours, hours_ending = (
        file_and_time_control.make_all_times(processed_data))


    output.write_all_data(
        years, months, days, hours, hours_ending,
        working_directory_main, main_output, extracted_data, dir_file_count
    )

elif processed_data.get('flow_options') in ("p", "ps"):
    print("Will add this capability later")






if __name__ == "__main__":
    main()

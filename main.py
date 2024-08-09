###********************* This is the main file *********************###

# Actively being developed! Please contribute if you want to help improve the program!

# Run this file in terminal using command: python3 main.py
# All the packages are in the Anaconda environment. Type the following in the terminal: conda activate GRIBTEST1
# Designed for Linux but can work on Windows 10.

import read_control_module
import herbie_module
import grib_module
import output_module


def main():
    working_directory_main = "/home/joshua/CODE/"
    control_filename = "control.txt"
    output_filename_with_inputs_used = "inputs_used_outfile.txt"
    main_output = "all_output.csv" # Do not change file extension!
    working_directory_grib = "/media/joshua/Elements/GRIB/HRRR/hrrr"

    control_data = read_control_module.read_control_file(working_directory_main, control_filename)
    processed_data = read_control_module.process_control_data(control_data)

    output_module.print_input_data(processed_data)
    output_module.write_processed_input_data_to_file(processed_data, output_filename_with_inputs_used)

    herbie_module.fetch_herbie_data_in_range(processed_data)

    no_missing_file_list = grib_module.match_strings_and_add_dummy_files(working_directory_grib)
    all_files = grib_module.files_to_do_work_for(working_directory_grib, processed_data)
    grid_cell_data = grib_module.process_grib_files(working_directory_main, processed_data, all_files)
    extracted_time_values = grib_module.extract_time_info_from_grib_files(all_files)
    GRIB_shortName, GRIB_level = grib_module.grib_dictionary_from_inputs(processed_data)
    build_dict = grib_module.dict_constructor()
    extracted_data = grib_module.extract_value_at_grid_index(all_files, grid_cell_data, GRIB_shortName, GRIB_level, extracted_time_values, build_dict)

    years, months, days, hours, hours_ending = output_module.make_all_times(processed_data)
    output_module.write_all_data(years, months, days, hours, hours_ending, working_directory_main, main_output, extracted_data)

if __name__ == "__main__":
    main()

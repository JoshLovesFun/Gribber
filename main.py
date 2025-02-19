# ********************* This is the main file *********************#

# Actively being developed!
# Please contribute if you want to help improve Gribber!

import sys
import os
import read_control_module
import herbie_module
import grib_module
import output_module


def main():
    default_working_directory = "."
    if len(sys.argv) > 1:
        control_filename = sys.argv[1]
    else:
        control_filename = "Control.txt"

    control_data = (read_control_module.read_control_file
                    (default_working_directory, control_filename))
    processed_data = read_control_module.process_control_data(control_data)
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

    output_module.print_input_data(processed_data)

    # Write the processed input data to the specified file
    output_module.write_processed_input_data_to_file(processed_data,
                                                     output_file_path)

    if processed_data.get('flow_options') in ("h", "hw", "hwa"):
        herbie_module.fetch_herbie_data_in_range(processed_data)
    elif processed_data.get('flow_options') == "e":
        main_output = processed_data.get('main_output')

        grib_module.match_strings_and_add_dummy_files(working_directory_grib)

        all_files = grib_module.files_to_do_work_for(working_directory_grib,
                                                     processed_data)
        grid_cell_data = grib_module.process_grib_files(working_directory_main,
                                                        processed_data,
                                                        all_files)
        extracted_time_values = grib_module.extract_time_info_from_grib_files(
            all_files)

        grib_short_name, grib_level = grib_module.grib_dictionary_from_inputs(
            processed_data)
        build_dict = grib_module.dict_constructor()

        extracted_data = grib_module.extract_value_at_grid_index(
            all_files,
            grid_cell_data,
            grib_short_name,
            grib_level,
            extracted_time_values,
            build_dict
        )
        years, months, days, hours, hours_ending = (
            output_module.make_all_times(processed_data))

        output_module.write_all_data(
            years, months, days, hours, hours_ending,
            working_directory_main, main_output, extracted_data
        )

    elif processed_data.get('flow_options') in ("p", "ps"):
        print("Will add this capability later")


if __name__ == "__main__":
    main()

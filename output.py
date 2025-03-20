# Goal: Record the inputs used, and write data to the main output csv file.

import sys
import pandas as pd
import numpy as np
import os
import time

from met_calcs import (
    kelvin_to_celsius, calculate_wind_speed_and_direction,
    calculate_relative_humidity, calculate_dew_point
)


def write_processed_input_data_to_file(processed_data, output_file_name):
    with open(output_file_name, 'w') as output_file:
        for key, value in processed_data.items():
            row = f"{key}: {value}\n"
            output_file.write(row)


def print_input_data(processed_data):
    run_herbie = processed_data['flow_options']

    if run_herbie in ("h", "hw", "hwa"):
        run_herbie = "yes"
    else:
        run_herbie = "no"

    print("Will Herbie be run?:", run_herbie)
    if run_herbie == "yes":
        print("Warning: This may take a while. You must have stable internet.")
        print("Warning: Lots of disk space may be required.")

    print("")
    print("Was WRF suite requested?:",
          processed_data['wrf'])
    print("")
    print("The input latitude is:", processed_data['latitude'])
    print("The input longitude is:", processed_data['inputlongitude'])
    print("The calculated longitude is:",
          processed_data['calculatedlongitude'])
    print("")
    print("Was the boundary layer height requested?:",
          processed_data['BoundaryLayerHeight'])

    print("Was the U and V wind requested?:",
          processed_data['U_and_V_WindComponent'])
    if processed_data['U_and_V_WindComponent'] == "yes":
        print("")
        print("Was wind level 1 requested:",
              processed_data['WindHeightLevel1'])
        print("Was wind level 2 requested:",
              processed_data['WindHeightLevel2'])
        print("Was wind level 3 requested:",
              processed_data['WindHeightLevel3'])
        print("Was wind level 4 requested:",
              processed_data['WindHeightLevel4'])
        print("Was wind level 5 requested:",
              processed_data['WindHeightLevel5'])
        print("Was wind level 6 requested:",
              processed_data['WindHeightLevel6'])
        print("Was wind level 7 requested:",
              processed_data['WindHeightLevel7'])
        print("Was wind level 8 requested:",
              processed_data['WindHeightLevel8'])
        print("Was wind level 9 requested:",
              processed_data['WindHeightLevel9'])
        print("Was wind level 10 requested:",
              processed_data['WindHeightLevel10'])
        print("Was wind level 11 requested:",
              processed_data['WindHeightLevel11'])
        print("Was wind level 12 requested:",
              processed_data['WindHeightLevel12'])
        print("")

    print("Was temperature requested?:", processed_data['Temperature'])
    if processed_data['Temperature'] == "yes":
        print("")
        print("Was temperature level 1 requested:",
              processed_data['TemperatureHeightLevel1'])
        print("Was temperature level 2 requested:",
              processed_data['TemperatureHeightLevel2'])
        print("Was temperature level 3 requested:",
              processed_data['TemperatureHeightLevel3'])
        print("Was temperature level 4 requested:",
              processed_data['TemperatureHeightLevel4'])
        print("Was temperature level 5 requested:",
              processed_data['TemperatureHeightLevel5'])
        print("Was temperature level 6 requested:",
              processed_data['TemperatureHeightLevel6'])
        print("Was temperature level 7 requested:",
              processed_data['TemperatureHeightLevel7'])
        print("Was temperature level 8 requested:",
              processed_data['TemperatureHeightLevel8'])
        print("Was temperature level 9 requested:",
              processed_data['TemperatureHeightLevel9'])
        print("Was temperature level 10 requested:",
              processed_data['TemperatureHeightLevel10'])
        print("Was temperature level 11 requested:",
              processed_data['TemperatureHeightLevel11'])
        print("Was temperature level 12 requested:",
              processed_data['TemperatureHeightLevel12'])
        print("")

    print("Was turbulent kinetic energy requested?:", processed_data['TKE'])
    if processed_data['TKE'] == "yes":
        print("")
        print("Was TKE level 1 requested:", processed_data['TKEHeightLevel1'])
        print("Was TKE level 2 requested:", processed_data['TKEHeightLevel2'])
        print("Was TKE level 3 requested:", processed_data['TKEHeightLevel3'])
        print("Was TKE level 4 requested:", processed_data['TKEHeightLevel4'])
        print("Was TKE level 5 requested:", processed_data['TKEHeightLevel5'])
        print("Was TKE level 6 requested:", processed_data['TKEHeightLevel6'])
        print("Was TKE level 7 requested:", processed_data['TKEHeightLevel7'])
        print("Was TKE level 8 requested:", processed_data['TKEHeightLevel8'])
        print("Was TKE level 9 requested:", processed_data['TKEHeightLevel9'])
        print("Was TKE level 10 requested:",
              processed_data['TKEHeightLevel10'])
        print("Was TKE level 11 requested:",
              processed_data['TKEHeightLevel11'])
        print("Was TKE level 12 requested:",
              processed_data['TKEHeightLevel12'])
        print("")

    print("Was pressure requested?:", processed_data['PRES'])
    if processed_data['PRES'] == "yes":
        print("")
        print("Was pressure level 1 requested:",
              processed_data['PRESHeightLevel1'])
        print("Was pressure level 2 requested:",
              processed_data['PRESHeightLevel2'])
        print("Was pressure level 3 requested:",
              processed_data['PRESHeightLevel3'])
        print("Was pressure level 4 requested:",
              processed_data['PRESHeightLevel4'])
        print("Was pressure level 5 requested:",
              processed_data['PRESHeightLevel5'])
        print("Was pressure level 6 requested:",
              processed_data['PRESHeightLevel6'])
        print("Was pressure level 7 requested:",
              processed_data['PRESHeightLevel7'])
        print("Was pressure level 8 requested:",
              processed_data['PRESHeightLevel8'])
        print("Was pressure level 9 requested:",
              processed_data['PRESHeightLevel9'])
        print("Was pressure level 10 requested:",
              processed_data['PRESHeightLevel10'])
        print("Was pressure level 11 requested:",
              processed_data['PRESHeightLevel11'])
        print("Was pressure level 12 requested:",
              processed_data['PRESHeightLevel12'])
        print("")

    print("Was specific humidity requested?:", processed_data['SPFH'])
    if processed_data['SPFH'] == "yes":
        print("")
        print("Was specific humidity level 1 requested:",
              processed_data['SPFHHeightLevel1'])
        print("Was specific humidity level 2 requested:",
              processed_data['SPFHHeightLevel2'])
        print("Was specific humidity level 3 requested:",
              processed_data['SPFHHeightLevel3'])
        print("Was specific humidity level 4 requested:",
              processed_data['SPFHHeightLevel4'])
        print("Was specific humidity level 5 requested:",
              processed_data['SPFHHeightLevel5'])
        print("Was specific humidity level 6 requested:",
              processed_data['SPFHHeightLevel6'])
        print("Was specific humidity level 7 requested:",
              processed_data['SPFHHeightLevel7'])
        print("Was specific humidity level 8 requested:",
              processed_data['SPFHHeightLevel8'])
        print("Was specific humidity level 9 requested:",
              processed_data['SPFHHeightLevel9'])
        print("Was specific humidity level 10 requested:",
              processed_data['SPFHHeightLevel10'])
        print("Was specific humidity level 11 requested:",
              processed_data['SPFHHeightLevel11'])
        print("Was specific humidity level 12 requested:",
              processed_data['SPFHHeightLevel12'])

    print("")
    print("The requested start date is:", processed_data['StartDate'])
    print("The requested end date is:", processed_data['EndDate'])
    print("")

    if processed_data['SPFH'] == "yes":
        warning = "\u2757"
        print(warning*5, '***WARNING***', warning*5)
        print("")
        print("If you request specific humidity and do not "
              "request the corresponding")
        print("temperature and pressure levels, no humidity or dew "
              "point calculations")
        print("can be done for that level. Double-check that you have "
              "selected all the")
        print("corresponding levels. If you are only interested in "
              "specific humidity and ")
        print("not relative humidity or dew point, you do not need "
              "temperature or pressure.")
        print("")

    user_input1 = input("Are these inputs correct? Type \"y\" for yes "
                        "or \"n\" for no. (no quotes): ")

    if user_input1 == "y" or user_input1 == "Y":
        print("")
        print("Program continuing...")
        print("")
    else:
        sys.exit()





def pad_list(lst, length, fill_value=np.nan):
    """Pads the list with `fill_value` to ensure it matches `length`."""
    return lst + [fill_value] * (length - len(lst)) if len(lst) < length else lst


def write_all_data_new(years, months, days, hours, hours_ending,
                       working_directory_main, main_output, dir_file_count, extracted_time_values_prs, extracted_time_values_nat,
                       all_files_prs, all_files_nat, sub_files, grib_data):
    print(f'the years is {years}')
    print(f'the months is {months}')
    print(f'the days is {days}')
    print(f'the hours is {hours}')
    print(f'the hours ending is {hours_ending}')
    print(f'the working_dir_main is {working_directory_main}')
    print(f'the main_output is {main_output}')
    print(f'the dir_file_count is {dir_file_count}')  # we don't need this for now
    print(f'the extracted_time_values_prs is {extracted_time_values_prs}')
    print(f'the extracted_time_values_nat is {extracted_time_values_nat}')

    MAX_LEVEL = 12
    # These column names will (should) always be made.
    column_names = ['Year', 'Month', 'Day', 'Hour_UTC', 'Hour_UTC_End',
                    'all_files_prs', 'all_files_nat', 'sub_files',
                    'PRS_Extracted_1', 'PRS_Extracted_2',
                    'NAT_Extracted_1', 'NAT_Extracted_2', 'BoundaryLayerHeight']

    # Dynamically generate level-based column names
    column_names += [f'TempLvl_{i}_K' for i in range(1, MAX_LEVEL + 1)]
    column_names += [f'TempLvl_{i}_C' for i in range(1, MAX_LEVEL + 1)]
    column_names += [f'U_WindLvl_{i}' for i in range(1, MAX_LEVEL + 1)]
    column_names += [f'V_WindLvl_{i}' for i in range(1, MAX_LEVEL + 1)]
    column_names += [f'WindSpeed{i}' for i in range(1, MAX_LEVEL + 1)]
    column_names += [f'WindDir{i}' for i in range(1, MAX_LEVEL + 1)]
    column_names += [f'TKE_Lvl_{i}' for i in range(1, MAX_LEVEL + 1)]
    column_names += [f'PRES_Lvl_{i}' for i in range(1, MAX_LEVEL + 1)]
    column_names += [f'SPFH_Lvl_{i}' for i in range(1, MAX_LEVEL + 1)]
    column_names += [f'RH_Lvl_{i}' for i in range(1, MAX_LEVEL + 1)]
    column_names += [f'Dew_Point_Lvl_{i}_C' for i in range(1, MAX_LEVEL + 1)]

    # The max length is always the length of `years` (24 or whatever max_length is)
    max_length = len(years)

    # Extract time values from tuples
    prs_extracted_1, prs_extracted_2 = zip(
        *extracted_time_values_prs) if extracted_time_values_prs else ([], [])
    nat_extracted_1, nat_extracted_2 = zip(
        *extracted_time_values_nat) if extracted_time_values_nat else ([], [])

    # Initialize DataFrame with all column names, filling with NaN
    df = pd.DataFrame(columns=column_names)

    # Assign padded lists to the DataFrame
    df['Year'] = years
    df['Month'] = pad_list(months, max_length)
    df['Day'] = pad_list(days, max_length)
    df['Hour_UTC'] = pad_list(hours, max_length)
    df['Hour_UTC_End'] = pad_list(hours_ending, max_length)
    df['all_files_prs'] = pad_list(all_files_prs, max_length)
    df['all_files_nat'] = pad_list(all_files_nat, max_length)
    df['sub_files'] = pad_list(sub_files, max_length)
    df['PRS_Extracted_1'] = pad_list(list(prs_extracted_1), max_length)
    df['PRS_Extracted_2'] = pad_list(list(prs_extracted_2), max_length)
    df['NAT_Extracted_1'] = pad_list(list(nat_extracted_1), max_length)
    df['NAT_Extracted_2'] = pad_list(list(nat_extracted_2), max_length)

    # Extract Boundary Layer Height (BLH) values and pad the list only if it's shorter than max_length
    df['BoundaryLayerHeight'] = pad_list(
        [record[4] for key in ['prs', 'nat']
         for file, records in grib_data.get(key, {}).items()
         for record in records if
         record[0] == 'blh' and record[4] != -9999.999],
        max_length
    )

    # Initialize temp_values dictionary for each level from 1 to 12 (Kelvin and Celsius)
    temp_values = {f'TempLvl_{i}_K': [] for i in range(1, 13)}
    temp_values_C = {f'TempLvl_{i}_C': [] for i in range(1, 13)}

    # Populate temp_values with valid data from the grib_data
    for key in ['prs', 'nat']:
        for file, records in grib_data.get(key, {}).items():
            for record in records:
                var_name, level, _, (_, _), value = record  # Extract values
                if var_name == 't' and level.isdigit():
                    level_index = int(level)
                    if 1 <= level_index <= 12 and value != -9999.999:
                        # Add Kelvin values to the temp_values dictionary
                        temp_values[f'TempLvl_{level_index}_K'].append(value)

                        # Convert Kelvin to Celsius and add to temp_values_C dictionary
                        celsius_value = kelvin_to_celsius(value)
                        temp_values_C[f'TempLvl_{level_index}_C'].append(
                            celsius_value)

    # Pad both Kelvin and Celsius values with NaN for missing levels and assign to the DataFrame
    for col_dict in [temp_values, temp_values_C]:
        for col, values in col_dict.items():
            if len(values) < max_length:
                values += [np.nan] * (max_length - len(values))
            df[col] = values

    # Save to CSV
    output_path = os.path.join(working_directory_main, main_output)
    df.to_csv(output_path, index=False)









# Now we are trying to write all the data to the csv file.
# If you get a "pandas" related error, the cause of the error may
# be related to issues caused in the GRIB module and/or column
# length mismatches. However, the issue could be related to any
# module file (including this one).


def write_all_data(years, months, days, hours, hours_ending,
                   working_directory_main, main_output, extracted_data, dir_file_count):
    fingers_crossed = "\U0001F91E"
    print("")
    print("Now trying to write to the output file. Wait 3 or more seconds " +
          fingers_crossed)
    print("")


    print(dir_file_count)

    # These column names will (should) always be made.
    column_names = ['Year', 'Month', 'Day', 'Hour_UTC', 'Hour_UTC_End',
                    'FilePath'] + [
        'GRIB_Date', 'GRIB_Time', 'BoundaryLayerHeight',
        'TempLvl_1_K', 'TempLvl_1_C', 'TempLvl_2_K', 'TempLvl_2_C',
        'TempLvl_3_K', 'TempLvl_3_C', 'TempLvl_4_K', 'TempLvl_4_C',
        'TempLvl_5_K', 'TempLvl_5_C', 'TempLvl_6_K', 'TempLvl_6_C',
        'TempLvl_7_K', 'TempLvl_7_C', 'TempLvl_8_K', 'TempLvl_8_C',
        'TempLvl_9_K', 'TempLvl_9_C', 'TempLvl_10_K', 'TempLvl_10_C',
        'TempLvl_11_K', 'TempLvl_11_C', 'TempLvl_12_K', 'TempLvl_12_C',
        'U_WindLvl_1', 'V_WindLvl_1', 'WindSpeed1', 'WindDir1', 'U_WindLvl_2',
        'V_WindLvl_2', 'WindSpeed2', 'WindDir2',
        'U_WindLvl_3', 'V_WindLvl_3', 'WindSpeed3', 'WindDir3', 'U_WindLvl_4',
        'V_WindLvl_4', 'WindSpeed4', 'WindDir4',
        'U_WindLvl_5', 'V_WindLvl_5', 'WindSpeed5', 'WindDir5', 'U_WindLvl_6',
        'V_WindLvl_6', 'WindSpeed6', 'WindDir6',
        'U_WindLvl_7', 'V_WindLvl_7', 'WindSpeed7', 'WindDir7', 'U_WindLvl_8',
        'V_WindLvl_8', 'WindSpeed8', 'WindDir8',
        'U_WindLvl_9', 'V_WindLvl_9', 'WindSpeed9', 'WindDir9', 'U_WindLvl_10',
        'V_WindLvl_10', 'WindSpeed10', 'WindDir10',
        'U_WindLvl_11', 'V_WindLvl_11', 'WindSpeed11', 'WindDir11',
        'U_WindLvl_12', 'V_WindLvl_12', 'WindSpeed12', 'WindDir12',
        'TKE_Lvl_1', 'TKE_Lvl_2', 'TKE_Lvl_3',
        'TKE_Lvl_4', 'TKE_Lvl_5', 'TKE_Lvl_6',
        'TKE_Lvl_7', 'TKE_Lvl_8', 'TKE_Lvl_9',
        'TKE_Lvl_10', 'TKE_Lvl_11', 'TKE_Lvl_12',
        'PRES_Lvl_1', 'PRES_Lvl_2', 'PRES_Lvl_3',
        'PRES_Lvl_4', 'PRES_Lvl_5', 'PRES_Lvl_6',
        'PRES_Lvl_7', 'PRES_Lvl_8', 'PRES_Lvl_9',
        'PRES_Lvl_10', 'PRES_Lvl_11', 'PRES_Lvl_12',
        'SPFH_Lvl_1', 'SPFH_Lvl_2', 'SPFH_Lvl_3',
        'SPFH_Lvl_4', 'SPFH_Lvl_5', 'SPFH_Lvl_6',
        'SPFH_Lvl_7', 'SPFH_Lvl_8', 'SPFH_Lvl_9',
        'SPFH_Lvl_10', 'SPFH_Lvl_11', 'SPFH_Lvl_12',
        'RH_Lvl_1', 'RH_Lvl_2', 'RH_Lvl_3',
        'RH_Lvl_4', 'RH_Lvl_5', 'RH_Lvl_6',
        'RH_Lvl_7', 'RH_Lvl_8', 'RH_Lvl_9',
        'RH_Lvl_10', 'RH_Lvl_11', 'RH_Lvl_12',
        'Dew_Point_Lvl_1_C', 'Dew_Point_Lvl_2_C', 'Dew_Point_Lvl_3_C',
        'Dew_Point_Lvl_4_C', 'Dew_Point_Lvl_5_C', 'Dew_Point_Lvl_6_C',
        'Dew_Point_Lvl_7_C', 'Dew_Point_Lvl_8_C', 'Dew_Point_Lvl_9_C',
        'Dew_Point_Lvl_10_C', 'Dew_Point_Lvl_11_C', 'Dew_Point_Lvl_12_C',
    ]

    # Create an empty DataFrame with the defined column names
    df = pd.DataFrame(columns=column_names)

    # Assign 'years', 'months', 'days', 'hours', and
    # hours_ending to respective columns
    df['Year'] = years
    df['Month'] = months
    df['Day'] = days
    df['Hour_UTC'] = hours
    df['Hour_UTC_End'] = hours_ending

    # Fill the additional columns with NaN values
    for col in column_names[6:]:
        df[col] = np.nan

    file_paths = []
    for key, value in extracted_data.items():
        #print(extracted_data.items())
        if value:
            file_paths = [item[0] for item in value]
            break
    #print(file_paths)
    df['FilePath'] = file_paths

    #print("Length of file_paths:", len(file_paths))
    #print("File paths:", file_paths)

    grib_time = []
    for key, value in extracted_data.items():
        if value:
            grib_time = [item[4] for item in value]
            break
    df['GRIB_Time'] = grib_time

    grib_date = []
    for key, value in extracted_data.items():
        if value:
            grib_date = [item[5] for item in value]
            break
    df['GRIB_Date'] = grib_date

    # Iterate through the dictionary and extract data for each
    # 'TempLvl_x' column
    for key, value in extracted_data.items():
        if key[0] == 't' and value:
            x = key[1]  # Extract 'x' from the key ('t', x)
            if 1 <= x <= 12:
                column_name_kelvin = f'TempLvl_{x}_K'
                column_name_celsius = f'TempLvl_{x}_C'

                df[column_name_kelvin] = [item[3] for item in value]
                df[column_name_celsius] = [kelvin_to_celsius(item[3]) for
                                           item in value]

    # Iterate through the dictionary and extract data for each
    # 'TKE_Lvl_x' column
    for key, value in extracted_data.items():
        if key[0] == 'tke' and value:
            x = key[1]  # Extract 'x' from the key ('tke', x)
            if 1 <= x <= 12:
                column_name_TKE = f'TKE_Lvl_{x}'
                df[column_name_TKE] = [item[3] for item in value]

    # Iterate through the dictionary and extract data for each
    # 'PRES_Lvl_x' column
    for key, value in extracted_data.items():
        if key[0] == 'pres' and value:
            x = key[1]  # Extract 'x' from the key ('pres', x)
            if 1 <= x <= 12:
                column_name_PRES = f'PRES_Lvl_{x}'
                df[column_name_PRES] = [item[3] for item in value]

    # Iterate through the dictionary and extract data for each
    # 'SPFH_Lvl_x' column
    for key, value in extracted_data.items():
        if key[0] == 'q' and value:
            x = key[1]  # Extract 'x' from the key ('q', x)
            if 1 <= x <= 12:
                column_name_SPFH = f'SPFH_Lvl_{x}'
                df[column_name_SPFH] = [item[3] for item in value]

    # Iterate through the dictionary and extract data for each
    # 'U_WindLvl_x' column
    for key, value in extracted_data.items():
        if key[0] == 'u' and value:
            x = key[1]  # Extract 'x' from the key ('u', x)
            if 1 <= x <= 12:
                column_name_u = f'U_WindLvl_{x}'
                df[column_name_u] = [item[3] for item in value]

    # Iterate through the dictionary and extract data for each
    # 'V_WindLvl_x' column
    for key, value in extracted_data.items():
        if key[0] == 'v' and value:
            x = key[1]  # Extract 'x' from the key ('v', x)
            if 1 <= x <= 12:
                column_name_v = f'V_WindLvl_{x}'
                df[column_name_v] = [item[3] for item in value]

    # Create new columns for wind speed and direction using the
    # calculate_wind_speed_and_direction function
    for x in range(1, 13):
        u_column_name = f'U_WindLvl_{x}'
        v_column_name = f'V_WindLvl_{x}'

        wind_speed_column_name = f'WindSpeed{x}'
        wind_dir_column_name = f'WindDir{x}'

        # Apply the calculate_wind_speed_and_direction function to each row
        wind_data_for_csv = df.apply(
            lambda row: calculate_wind_speed_and_direction(
                row[u_column_name], row[v_column_name]), axis=1)

        # Check if wind_data_for_csv is not None before
        # unzipping and assigning to new columns
        if wind_data_for_csv is not None:
            # Unzip the results and assign them to the new columns
            wind_speed_values, wind_dir_values = zip(*wind_data_for_csv)
            # Assign the values to the new columns
            df[wind_speed_column_name] = wind_speed_values
            df[wind_dir_column_name] = wind_dir_values

    # Create new columns for relative humidity using the
    # calculate_relative_humidity function
    for x in range(1, 13):
        q_column_name = f'SPFH_Lvl_{x}'
        t_column_name = f'TempLvl_{x}_K'
        p_column_name = f'PRES_Lvl_{x}'

        RH_column_name = f'RH_Lvl_{x}'

        # Apply the calculate_relative_humidity function to each row
        RH_data_for_csv = df.apply(lambda row: calculate_relative_humidity(
            row[q_column_name],
            row[t_column_name],
            row[p_column_name]), axis=1)

        # Assign the results to the RH column
        df[RH_column_name] = RH_data_for_csv

    # Create new columns for dew point using the calculate_dew_point function
    for x in range(1, 13):
        t_column_name = f'TempLvl_{x}_K'
        # This should be the RH column that now has data.
        RH_filled_column_name = f'RH_Lvl_{x}'

        dew_point_column_name = f'Dew_Point_Lvl_{x}_C'

        # Apply the calculate_dew_point function to each row
        Dew_Point_data_for_csv = df.apply(lambda row: calculate_dew_point(
            row[t_column_name], row[RH_filled_column_name]), axis=1)

        # Assign the results to the Dew Point column
        df[dew_point_column_name] = Dew_Point_data_for_csv

    # Iterate through the dictionary and extract data for
    # BoundaryLayerHeight column
    for key, value in extracted_data.items():
        if key[0] == 'blh' and value:
            x = key[1]  # Extract 'x' from the key ('blh', x)
            if x == 0:
                column_name = f'BoundaryLayerHeight'
                df[column_name] = [item[3] for item in value]

    # If a GRIB file is missing which is rare or never, the string 'missing'
    # is assigned to each cell that would normally have data. So we use this
    # to convert, the 'missing' to an actual value.
    df = df.replace('missing', -9999.999)

    output_path = os.path.join(working_directory_main, main_output)
    df.to_csv(output_path, index=False)

    time.sleep(3)
    monkey = "\U0001F412"

    print("")
    print(monkey*23)
    print(monkey, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', monkey)
    print(monkey, '!  Successful completion of gribber!!  !', monkey)
    print(monkey, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', monkey)
    print(monkey*23)
    print("")

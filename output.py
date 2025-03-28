# Goal: Record the inputs used, and write data to the main output csv file.

import sys
import pandas as pd
import numpy as np
import os
import time

import constants
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
    print("The input longitude is:", processed_data['input_longitude'])
    print("The calculated longitude is:",
          processed_data['calculated_longitude'])
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
    if len(lst) < length:
        return lst + [fill_value] * (length - len(lst))
    return lst


# Now we are trying to write all the data to the csv file.
# If you get a "pandas" related error, the cause of the error may
# be related to issues caused in the GRIB module and/or column
# length mismatches. However, the issue could be related to any
# module file (including this one).
def write_all_data_new(years, months, days, hours, hours_ending,
                       working_directory_main, main_output,
                       dir_file_count,
                       extracted_time_values_prs, extracted_time_values_nat,
                       all_files_prs, all_files_nat, sub_files, grib_data):

    # These column names will (should) always be made.
    column_names = ['Year', 'Month', 'Day', 'Hour_UTC', 'Hour_UTC_End',
                    'all_files_prs', 'all_files_nat', 'sub_files',
                    'PRS_Extracted_1', 'PRS_Extracted_2',
                    'NAT_Extracted_1', 'NAT_Extracted_2',
                    'BoundaryLayerHeight']

    # Dynamically generate level-based column names
    column_names += [f'TempLvl_{i}_K' for i in range(1, constants.MAX_LVL + 1)]
    column_names += [f'TempLvl_{i}_C' for i in range(1, constants.MAX_LVL + 1)]
    column_names += [f'U_WindLvl_{i}' for i in range(1, constants.MAX_LVL + 1)]
    column_names += [f'V_WindLvl_{i}' for i in range(1, constants.MAX_LVL + 1)]
    column_names += [f'WindSpeed{i}' for i in range(1, constants.MAX_LVL + 1)]
    column_names += [f'WindDir{i}' for i in range(1, constants.MAX_LVL + 1)]
    column_names += [f'TKE_Lvl_{i}' for i in range(1, constants.MAX_LVL + 1)]
    column_names += [f'PRES_Lvl_{i}' for i in range(1, constants.MAX_LVL + 1)]
    column_names += [f'SPFH_Lvl_{i}' for i in range(1, constants.MAX_LVL + 1)]
    column_names += [f'RH_Lvl_{i}' for i in range(1, constants.MAX_LVL + 1)]
    column_names += [f'Dew_Point_Lvl_{i}_C' for i in
                     range(1, constants.MAX_LVL + 1)]

    # The max length is always the length
    # of `years` (24 or whatever max_length is)
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

    # Extract Boundary Layer Height (BLH) values and pad the list only
    # if it's shorter than max_length
    df['BoundaryLayerHeight'] = pad_list(
        [record[4] for key in ['prs', 'nat']
         for file, records in grib_data.get(key, {}).items()
         for record in records if
         record[0] == 'blh' and record[4] != -9999.999],
        max_length
    )

    # Initialize temp_values dictionary for each level from 1 to 12
    # (Kelvin and Celsius)
    temp_values = {f'TempLvl_{i}_K': [] for i in range(1, 13)}
    temp_values_c = {f'TempLvl_{i}_C': [] for i in range(1, 13)}
    tke_values = {f'TKE_Lvl_{i}': [] for i in range(1, 13)}
    pres_values = {f'PRES_Lvl_{i}': [] for i in range(1, 13)}
    spfh_values = {f'SPFH_Lvl_{i}': [] for i in range(1, 13)}
    u_values = {f'U_WindLvl_{i}': [] for i in range(1, 13)}
    v_values = {f'V_WindLvl_{i}': [] for i in range(1, 13)}
    wind_speed_values = {f'WindSpeed{i}': [] for i in range(1, 13)}
    wind_dir_values = {f'WindDir{i}': [] for i in range(1, 13)}

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

                        # Convert Kelvin to Celsius and add to
                        # temp_values_C dictionary
                        celsius_value = kelvin_to_celsius(value)
                        temp_values_c[f'TempLvl_{level_index}_C'].append(
                            celsius_value)

                if var_name == 'tke' and level.isdigit():
                    level_index = int(level)
                    if 1 <= level_index <= 12 and value != -9999.999:
                        # Add tke values to the tke_values dictionary
                        tke_values[f'TKE_Lvl_{level_index}'].append(value)

                if var_name == 'pres' and level.isdigit():
                    level_index = int(level)
                    if 1 <= level_index <= 12 and value != -9999.999:
                        # Add pres values to the pres_values dictionary
                        pres_values[f'PRES_Lvl_{level_index}'].append(value)

                if var_name == 'q' and level.isdigit():
                    level_index = int(level)
                    if 1 <= level_index <= 12 and value != -9999.999:
                        spfh_values[f'SPFH_Lvl_{level_index}'].append(value)

                if var_name == 'u' and level.isdigit():
                    level_index = int(level)
                    if 1 <= level_index <= 12 and value != -9999.999:
                        u_values[f'U_WindLvl_{level_index}'].append(value)

                if var_name == 'v' and level.isdigit():
                    level_index = int(level)
                    if 1 <= level_index <= 12 and value != -9999.999:
                        v_values[f'V_WindLvl_{level_index}'].append(value)

    # Pad values with NaN for missing levels and assign to the DataFrame
    for col_dict in [temp_values, temp_values_c, tke_values,
                     pres_values, spfh_values, u_values, v_values]:
        for col, values in col_dict.items():
            if len(values) < max_length:
                values += [np.nan] * (max_length - len(values))
            df[col] = values

    for x in range(1, 13):
        df[[f'WindSpeed{x}', f'WindDir{x}']] = df.apply(
            lambda row: pd.Series(calculate_wind_speed_and_direction(
                row[f'U_WindLvl_{x}'], row[f'V_WindLvl_{x}'])),
            axis=1
        )

    for x in range(1, 13):
        df[f'RH_Lvl_{x}'] = df.apply(
            lambda row: calculate_relative_humidity(
                row[f'SPFH_Lvl_{x}'], row[f'TempLvl_{x}_K'],
                row[f'PRES_Lvl_{x}']
            ), axis=1
        )

    for x in range(1, 13):
        df[f'Dew_Point_Lvl_{x}_C'] = df.apply(
            lambda row: calculate_dew_point(
                row[f'TempLvl_{x}_K'], row[f'RH_Lvl_{x}']
            ), axis=1
        )

    fingers_crossed = "\U0001F91E"
    print("")
    print("Now trying to write to the output file. Wait 3 or more seconds " +
          fingers_crossed)
    print("")

    # Save to CSV
    output_path = str(os.path.join(working_directory_main, main_output))
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

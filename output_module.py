# Goal: Record the inputs used, and write data to the main output csv file.

import sys
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
import math
import time


def write_processed_input_data_to_file(processed_data, output_file_name):
    with open(output_file_name, 'w') as output_file:
        for key, value in processed_data.items():
            row = f"{key}: {value}\n"
            output_file.write(row)


def print_input_data(processed_data):
    HerbieAlreadyDone = processed_data['HerbieAlreadyDone']

    RunHerbie = "no"
    if HerbieAlreadyDone == "no":
        RunHerbie = "yes"

    print("Will Herbie be run?:", RunHerbie)
    if HerbieAlreadyDone == "no":
        print("Warning: This may take a while. You must have stable internet.")
        print("Warning: Lots of disk space may be required.")

    print("")
    print("The input latitude is:", processed_data['latitude'])
    print("The input longitude is:", processed_data['inputlongitude'])
    print("The calculated longitude is:", processed_data['calculatedlongitude'])
    print("")
    print("Was the boundary layer height requested?:", processed_data['BoundaryLayerHeight'])

    print("Was the U and V wind requested?:", processed_data['U_and_V_WindComponent'])
    if processed_data['U_and_V_WindComponent'] == "yes":
        print("")
        print("Was wind level 1 requested:", processed_data['WindHeightLevel1'])
        print("Was wind level 2 requested:", processed_data['WindHeightLevel2'])
        print("Was wind level 3 requested:", processed_data['WindHeightLevel3'])
        print("Was wind level 4 requested:", processed_data['WindHeightLevel4'])
        print("Was wind level 5 requested:", processed_data['WindHeightLevel5'])
        print("Was wind level 6 requested:", processed_data['WindHeightLevel6'])
        print("Was wind level 7 requested:", processed_data['WindHeightLevel7'])
        print("Was wind level 8 requested:", processed_data['WindHeightLevel8'])
        print("Was wind level 9 requested:", processed_data['WindHeightLevel9'])
        print("Was wind level 10 requested:", processed_data['WindHeightLevel10'])
        print("Was wind level 11 requested:", processed_data['WindHeightLevel11'])
        print("Was wind level 12 requested:", processed_data['WindHeightLevel12'])
        print("")

    print("Was temperature requested?:", processed_data['Temperature'])
    if processed_data['Temperature'] == "yes":
        print("")
        print("Was temperature level 1 requested:", processed_data['TemperatureHeightLevel1'])
        print("Was temperature level 2 requested:", processed_data['TemperatureHeightLevel2'])
        print("Was temperature level 3 requested:", processed_data['TemperatureHeightLevel3'])
        print("Was temperature level 4 requested:", processed_data['TemperatureHeightLevel4'])
        print("Was temperature level 5 requested:", processed_data['TemperatureHeightLevel5'])
        print("Was temperature level 6 requested:", processed_data['TemperatureHeightLevel6'])
        print("Was temperature level 7 requested:", processed_data['TemperatureHeightLevel7'])
        print("Was temperature level 8 requested:", processed_data['TemperatureHeightLevel8'])
        print("Was temperature level 9 requested:", processed_data['TemperatureHeightLevel9'])
        print("Was temperature level 10 requested:", processed_data['TemperatureHeightLevel10'])
        print("Was temperature level 11 requested:", processed_data['TemperatureHeightLevel11'])
        print("Was temperature level 12 requested:", processed_data['TemperatureHeightLevel12'])
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
        print("Was TKE level 10 requested:", processed_data['TKEHeightLevel10'])
        print("Was TKE level 11 requested:", processed_data['TKEHeightLevel11'])
        print("Was TKE level 12 requested:", processed_data['TKEHeightLevel12'])
        print("")

    print("Was pressure requested?:", processed_data['PRES'])
    if processed_data['PRES'] == "yes":
        print("")
        print("Was pressure level 1 requested:", processed_data['PRESHeightLevel1'])
        print("Was pressure level 2 requested:", processed_data['PRESHeightLevel2'])
        print("Was pressure level 3 requested:", processed_data['PRESHeightLevel3'])
        print("Was pressure level 4 requested:", processed_data['PRESHeightLevel4'])
        print("Was pressure level 5 requested:", processed_data['PRESHeightLevel5'])
        print("Was pressure level 6 requested:", processed_data['PRESHeightLevel6'])
        print("Was pressure level 7 requested:", processed_data['PRESHeightLevel7'])
        print("Was pressure level 8 requested:", processed_data['PRESHeightLevel8'])
        print("Was pressure level 9 requested:", processed_data['PRESHeightLevel9'])
        print("Was pressure level 10 requested:", processed_data['PRESHeightLevel10'])
        print("Was pressure level 11 requested:", processed_data['PRESHeightLevel11'])
        print("Was pressure level 12 requested:", processed_data['PRESHeightLevel12'])
        print("")

    print("Was specific humidity requested?:", processed_data['SPFH'])
    if processed_data['SPFH'] == "yes":
        print("")
        print("Was specific humidity level 1 requested:", processed_data['SPFHHeightLevel1'])
        print("Was specific humidity level 2 requested:", processed_data['SPFHHeightLevel2'])
        print("Was specific humidity level 3 requested:", processed_data['SPFHHeightLevel3'])
        print("Was specific humidity level 4 requested:", processed_data['SPFHHeightLevel4'])
        print("Was specific humidity level 5 requested:", processed_data['SPFHHeightLevel5'])
        print("Was specific humidity level 6 requested:", processed_data['SPFHHeightLevel6'])
        print("Was specific humidity level 7 requested:", processed_data['SPFHHeightLevel7'])
        print("Was specific humidity level 8 requested:", processed_data['SPFHHeightLevel8'])
        print("Was specific humidity level 9 requested:", processed_data['SPFHHeightLevel9'])
        print("Was specific humidity level 10 requested:", processed_data['SPFHHeightLevel10'])
        print("Was specific humidity level 11 requested:", processed_data['SPFHHeightLevel11'])
        print("Was specific humidity level 12 requested:", processed_data['SPFHHeightLevel12'])

    print("")
    print("The requested start date is:", processed_data['StartDate'])
    print("The requested end date is:", processed_data['EndDate'])
    print("")

    if processed_data['SPFH'] == "yes":
        warning = "\u2757"
        print(warning*5,'***WARNING***',warning*5)
        print("")
        print("If you request specific humidity and do not request the corresponding")
        print("temperature and pressure levels, no humidity or dew point calculations")
        print("can be done for that level. Double-check that you have selected all the")
        print("corresponding levels. If you are only interested in specific humidity and ")
        print("not relative humidity or dew point, you do not need temperature or pressure.")
        print("")

    user_input1 = input("Are these inputs correct? Type \"y\" for yes or \"n\" for no. (no quotes): ")

    if user_input1 == "y" or user_input1 == "Y":
        print("")
        print("Program continuing...")
        print("")
    else:
        sys.exit()


# This function makes all times based on the requested range.
# It makes the "reference" columns.
def make_all_times(processed_data):
    StartDate_Out = processed_data.get('StartDate')
    EndDate_Out = processed_data.get('EndDate')
    StartDate_OutNodash = int(StartDate_Out.replace("-", ""))
    EndDate_OutNodash = int(EndDate_Out.replace("-", ""))

    start_date = datetime.strptime(str(StartDate_OutNodash), "%Y%m%d")
    end_date = datetime.strptime(str(EndDate_OutNodash), "%Y%m%d")

    years, months, days, hours, hours_ending = [], [], [], [], []
    current_date = start_date
    while current_date <= end_date:
        for hour in range(24):
            years.append(current_date.year)
            months.append(current_date.month)
            days.append(current_date.day)
            hours.append(hour)
            hours_ending.append(hour + 1 if hour < 23 else 24)  # Convert to hour ending format
            current_date += timedelta(hours=1)

    return years, months, days, hours, hours_ending


# Now are some calculation functions.

def kelvin_to_celsius(kelvin):
    if isinstance(kelvin, float):
        celsius = kelvin - 273.15
        rounded_celsius = round(celsius, 3)
        return rounded_celsius
    else:
        return -9999.999


def calculate_wind_speed_and_direction(u, v):
    if (isinstance(u, float) and isinstance(v, float)):

        # Calculate the wind speed
        wind_speed = round(math.sqrt(u**2 + v**2), 3)

        # Calculate the math wind direction
        math_wind_direction_rad = math.atan2(v, u) # v before u but the opposite in Excel???

        meteorological_wind_direction = round((270 - (math_wind_direction_rad * 180.0 / math.pi)) % 360, 3)
        # In Excel: =MOD((270-($Q2)*(180/PI())),360)

        return wind_speed, meteorological_wind_direction
    else:
        return -9999.999, -9999.999


def calculate_relative_humidity(q, t, p):
    # This if statement is used to prevent an error when specific humidity is requested for a
    # particular level, but either the temperature or pressure at that level was not requested.
    if (q is None or q == -9999.999) or (t is None or t == -9999.999) or (p is None or p == -9999.999):
        return -9999.999

    if (q == 0.0): # Rare. Do this to avoid error for dew point calculation.
        return 0.000001

    if (isinstance(q, float) and isinstance(t, float) and isinstance(p, float)):

        # We need specific humidity, temperature, and pressure at the level of interest.
        # Input arguments:
        # q: Specific Humidity [kg/kg]
        # t: Temperature [K]
        # p: Pressure [Pa]

        # Info: https://earthscience.stackexchange.com/questions/2360/how-do-i-convert-specific-humidity-to-relative-humidity
        # Info: https://en.wikipedia.org/wiki/Clausius%E2%80%93Clapeyron_relation
        # Info: https://cran.r-project.org/web/packages/humidity/vignettes/humidity-measures.html

        # First calculate e (vapor pressure)
        # Then calculate e_sub_s (saturation vapor pressure)

        Mw_over_Md = 0.622 # The ratio of the molecular weight of water vapor to the molecular weight of dry air.
        One_Minus_Mw_over_Md = 0.378 # One minus the ratio of the molecular weight of water vapor to the molecular weight of dry air.

        # Equation 6: https://cran.r-project.org/web/packages/humidity/vignettes/humidity-measures.html
        e = (q * p) / (Mw_over_Md + (One_Minus_Mw_over_Md * q)) # Result in Pa


        # August–Roche–Magnus formula: We can use this to calculate saturation vapor pressure.
        # https://en.wikipedia.org/wiki/Clausius%E2%80%93Clapeyron_relation
        # Input temperature for this formula is in Celsius.

        t_C = t - 273.15

        ScaleFactor = 6.1094 # No units but serves to adjust the formula's output to match the desired units (hectopascals in this case).
        ScaleTempFactor1 = 17.625 # No units but used to account for the temperature dependence of the saturation vapor pressure.
        ScaleTempFactor2 = 243.04 # No units but used to account for the temperature dependence of the saturation vapor pressure.

        e_sub_s = ScaleFactor * math.exp((ScaleTempFactor1 * t_C)/(t_C + ScaleTempFactor2)) # Result in hPa

        e_sub_s_Pa = e_sub_s * 100.0 # Convert to Pa

        # Finally, to get RH:
        RH = (e / e_sub_s_Pa) * 100.0 # Pa/Pa * 100%
        RH_cap = RH

        if RH > 100.0: # This should be rare. It shouldn't be that much over 100%.
            RH_cap = 100.0

        # https://www.processsensing.com/en-us/humidity-calculator/rotronic/
        # The above link can be used to check results. Results should be close,
        # but we can't expect them to be identical!
        return RH_cap
    else:
        return -9999.999


def calculate_dew_point(t, RH_cap):
    # This if statement is used to prevent an error when specific humidity is requested for a
    # particular level, but either the temperature or pressure at that level was not requested.
    if (t is None or t == -9999.999) or (RH_cap is None or RH_cap == -9999.999):
        return -9999.999

    if (isinstance(t, float) and isinstance(RH_cap, float)):

        # Formula: https://bmcnoldy.earth.miami.edu/Humidity.html

        # Input temperature is in Kelvin.
        # We want the output temperature to be in Celsius. So:
        t_C = t - 273.15

        numerator = 243.04 * (math.log(RH_cap/100.0) + ((17.625 * t_C) / (243.04 + t_C)))
        denominator = 17.625 - math.log(RH_cap/100.0) - ((17.625 * t_C) / (243.04 + t_C))
        Dew_Point = round((numerator / denominator), 3)

        # Verify the results:
        # https://bmcnoldy.earth.miami.edu/Humidity.html
        # https://www.calculator.net/dew-point-calculator.html
        return Dew_Point
    else:
        return -9999.999

# Now we are trying to write all the data to the csv file.
# If you get a "pandas" related error, the cause of the error may
# be related to issues caused in the GRIB module and/or column length mismatches.
# However, the issue could be related to any module file (including this one).

def write_all_data(years, months, days, hours, hours_ending, working_directory_main, main_output, extracted_data):
    fingers_crossed = "\U0001F91E"
    print("")
    print("Now trying to write to the output file. Wait 3 or more seconds " + fingers_crossed)
    print("")

    # These column names will (should) always be made.
    column_names = ['Year', 'Month', 'Day', 'Hour_UTC', 'Hour_UTC_End', 'FilePath'] + [
        'GRIB_Date', 'GRIB_Time', 'BoundaryLayerHeight',
        'TempLvl_1_K', 'TempLvl_1_C', 'TempLvl_2_K', 'TempLvl_2_C', 'TempLvl_3_K', 'TempLvl_3_C', 'TempLvl_4_K', 'TempLvl_4_C',
        'TempLvl_5_K', 'TempLvl_5_C', 'TempLvl_6_K', 'TempLvl_6_C', 'TempLvl_7_K', 'TempLvl_7_C', 'TempLvl_8_K', 'TempLvl_8_C',
        'TempLvl_9_K', 'TempLvl_9_C', 'TempLvl_10_K', 'TempLvl_10_C', 'TempLvl_11_K', 'TempLvl_11_C', 'TempLvl_12_K', 'TempLvl_12_C',
        'U_WindLvl_1', 'V_WindLvl_1', 'WindSpeed1', 'WindDir1', 'U_WindLvl_2', 'V_WindLvl_2', 'WindSpeed2', 'WindDir2',
        'U_WindLvl_3', 'V_WindLvl_3', 'WindSpeed3', 'WindDir3', 'U_WindLvl_4', 'V_WindLvl_4', 'WindSpeed4', 'WindDir4',
        'U_WindLvl_5', 'V_WindLvl_5', 'WindSpeed5', 'WindDir5', 'U_WindLvl_6', 'V_WindLvl_6', 'WindSpeed6', 'WindDir6',
        'U_WindLvl_7', 'V_WindLvl_7', 'WindSpeed7', 'WindDir7', 'U_WindLvl_8', 'V_WindLvl_8', 'WindSpeed8', 'WindDir8',
        'U_WindLvl_9', 'V_WindLvl_9', 'WindSpeed9', 'WindDir9', 'U_WindLvl_10', 'V_WindLvl_10', 'WindSpeed10', 'WindDir10',
        'U_WindLvl_11', 'V_WindLvl_11', 'WindSpeed11', 'WindDir11', 'U_WindLvl_12', 'V_WindLvl_12', 'WindSpeed12', 'WindDir12',
        'TKE_Lvl_1', 'TKE_Lvl_2', 'TKE_Lvl_3', 'TKE_Lvl_4', 'TKE_Lvl_5', 'TKE_Lvl_6',
        'TKE_Lvl_7', 'TKE_Lvl_8', 'TKE_Lvl_9', 'TKE_Lvl_10', 'TKE_Lvl_11', 'TKE_Lvl_12',
        'PRES_Lvl_1', 'PRES_Lvl_2', 'PRES_Lvl_3', 'PRES_Lvl_4', 'PRES_Lvl_5', 'PRES_Lvl_6',
        'PRES_Lvl_7', 'PRES_Lvl_8', 'PRES_Lvl_9', 'PRES_Lvl_10', 'PRES_Lvl_11', 'PRES_Lvl_12',
        'SPFH_Lvl_1', 'SPFH_Lvl_2', 'SPFH_Lvl_3', 'SPFH_Lvl_4', 'SPFH_Lvl_5', 'SPFH_Lvl_6',
        'SPFH_Lvl_7', 'SPFH_Lvl_8', 'SPFH_Lvl_9', 'SPFH_Lvl_10', 'SPFH_Lvl_11', 'SPFH_Lvl_12',
        'RH_Lvl_1', 'RH_Lvl_2', 'RH_Lvl_3', 'RH_Lvl_4', 'RH_Lvl_5', 'RH_Lvl_6',
        'RH_Lvl_7', 'RH_Lvl_8', 'RH_Lvl_9', 'RH_Lvl_10', 'RH_Lvl_11', 'RH_Lvl_12',
        'Dew_Point_Lvl_1_C', 'Dew_Point_Lvl_2_C', 'Dew_Point_Lvl_3_C', 'Dew_Point_Lvl_4_C', 'Dew_Point_Lvl_5_C', 'Dew_Point_Lvl_6_C',
        'Dew_Point_Lvl_7_C', 'Dew_Point_Lvl_8_C', 'Dew_Point_Lvl_9_C', 'Dew_Point_Lvl_10_C', 'Dew_Point_Lvl_11_C', 'Dew_Point_Lvl_12_C',
    ]

    # Create an empty DataFrame with the defined column names
    df = pd.DataFrame(columns=column_names)

    # Assign 'years', 'months', 'days', 'hours', and hours_ending to respective columns
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
        if value:
            file_paths = [item[0] for item in value]
            break
    df['FilePath'] = file_paths

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


    # Iterate through the dictionary and extract data for each 'TempLvl_x' column
    for key, value in extracted_data.items():
        if key[0] == 't' and value:
            x = key[1]  # Extract 'x' from the key ('t', x)
            if 1 <= x <= 12:
                column_name_kelvin = f'TempLvl_{x}_K'
                column_name_celsius = f'TempLvl_{x}_C'

                df[column_name_kelvin] = [item[3] for item in value]
                df[column_name_celsius] = [kelvin_to_celsius(item[3]) for item in value]

    # Iterate through the dictionary and extract data for each 'TKE_Lvl_x' column
    for key, value in extracted_data.items():
        if key[0] == 'tke' and value:
            x = key[1]  # Extract 'x' from the key ('tke', x)
            if 1 <= x <= 12:
                column_name_TKE = f'TKE_Lvl_{x}'
                df[column_name_TKE] = [item[3] for item in value]

    # Iterate through the dictionary and extract data for each 'PRES_Lvl_x' column
    for key, value in extracted_data.items():
        if key[0] == 'pres' and value:
            x = key[1]  # Extract 'x' from the key ('pres', x)
            if 1 <= x <= 12:
                column_name_PRES = f'PRES_Lvl_{x}'
                df[column_name_PRES] = [item[3] for item in value]

    # Iterate through the dictionary and extract data for each 'SPFH_Lvl_x' column
    for key, value in extracted_data.items():
        if key[0] == 'q' and value:
            x = key[1]  # Extract 'x' from the key ('q', x)
            if 1 <= x <= 12:
                column_name_SPFH = f'SPFH_Lvl_{x}'
                df[column_name_SPFH] = [item[3] for item in value]

    # Iterate through the dictionary and extract data for each 'U_WindLvl_x' column
    for key, value in extracted_data.items():
        if key[0] == 'u' and value:
            x = key[1]  # Extract 'x' from the key ('u', x)
            if 1 <= x <= 12:
                column_name_u = f'U_WindLvl_{x}'
                df[column_name_u] = [item[3] for item in value]

    # Iterate through the dictionary and extract data for each 'V_WindLvl_x' column
    for key, value in extracted_data.items():
        if key[0] == 'v' and value:
            x = key[1]  # Extract 'x' from the key ('v', x)
            if 1 <= x <= 12:
                column_name_v = f'V_WindLvl_{x}'
                df[column_name_v] = [item[3] for item in value]


    # Create new columns for wind speed and direction using the calculate_wind_speed_and_direction function
    for x in range(1, 13):
        u_column_name = f'U_WindLvl_{x}'
        v_column_name = f'V_WindLvl_{x}'

        wind_speed_column_name = f'WindSpeed{x}'
        wind_dir_column_name = f'WindDir{x}'

        # Apply the calculate_wind_speed_and_direction function to each row
        wind_data_for_csv = df.apply(lambda row: calculate_wind_speed_and_direction(row[u_column_name], row[v_column_name]), axis=1)

        # Check if wind_data_for_csv is not None before unzipping and assigning to new columns
        if wind_data_for_csv is not None:
            # Unzip the results and assign them to the new columns
            wind_speed_values, wind_dir_values = zip(*wind_data_for_csv)
            # Assign the values to the new columns
            df[wind_speed_column_name] = wind_speed_values
            df[wind_dir_column_name] = wind_dir_values


    # Create new columns for relative humidity using the calculate_relative_humidity function
    for x in range(1, 13):
        q_column_name = f'SPFH_Lvl_{x}'
        t_column_name = f'TempLvl_{x}_K'
        p_column_name = f'PRES_Lvl_{x}'

        RH_column_name = f'RH_Lvl_{x}'

        # Apply the calculate_relative_humidity function to each row
        RH_data_for_csv = df.apply(lambda row: calculate_relative_humidity(row[q_column_name], row[t_column_name], row[p_column_name]), axis=1)

        # Assign the results to the RH column
        df[RH_column_name] = RH_data_for_csv


    # Create new columns for dew point using the calculate_dew_point function
    for x in range(1, 13):
        t_column_name = f'TempLvl_{x}_K'
        RH_filled_column_name = f'RH_Lvl_{x}' # This should be the RH column that now has data.

        dew_point_column_name = f'Dew_Point_Lvl_{x}_C'

        # Apply the calculate_dew_point function to each row
        Dew_Point_data_for_csv = df.apply(lambda row: calculate_dew_point(row[t_column_name], row[RH_filled_column_name]), axis=1)

        # Assign the results to the Dew Point column
        df[dew_point_column_name] = Dew_Point_data_for_csv


    # Iterate through the dictionary and extract data for BoundaryLayerHeight column
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
    print(monkey,'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',monkey)
    print(monkey,'!  Successful completion of gribber!!  !',monkey)
    print(monkey,'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',monkey)
    print(monkey*23)
    print("")

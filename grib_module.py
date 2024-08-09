# Goal: Extract what we want from the GRIB files.
# HRRR GRIB INFO EXAMPLE:
# KEY:   edition      centre       date         dataType     gridType     stepRange    typeOfLevel  level        shortName    packingType
# VALUE: 2            kwbc         20220105     fc           lambert      0            hybrid       1            pres         grid_complex_spatial_differencing

from eccodes import *
import os
import re
import sys
import traceback

from read_control_module import process_control_data


def extract_hour_from_filename(file_name):
    # Search for a pattern "tXX" within the file name
    match = re.search(r't(\d{2})', file_name)

    if match:
        return int(match.group(1))
    return -1


def files_to_do_work_for(working_directory_grib, processed_data):
    ForGRIB_StartDate = processed_data.get('StartDate')
    ForGRIB_EndDate = processed_data.get('EndDate')
    all_files = []
    ForGRIB_StartDateNodash = int(ForGRIB_StartDate.replace("-", ""))
    ForGRIB_EndDateNodash = int(ForGRIB_EndDate.replace("-", ""))

    for root, dirs, files in os.walk(working_directory_grib):

        subdirs_to_remove = []
        for dir_name in dirs:

            if int(dir_name) > ForGRIB_EndDateNodash or int(dir_name) < ForGRIB_StartDateNodash:
                subdirs_to_remove.append(dir_name)

        for subdir in subdirs_to_remove:
            dirs.remove(subdir)

        for file in files:
            if file.endswith(".grib2"):
                file_path = os.path.join(root, file)
                all_files.append(file_path)

        # Sort all files based on the date and hour components in the directory and file names
        all_files.sort(key=lambda x: (os.path.basename(os.path.dirname(x)), extract_hour_from_filename(os.path.basename(x))))
        # Print for debugging
        # print(all_files)

    return all_files


def match_strings_and_add_dummy_files(working_directory_grib):
    # Define the strings to match
    strings_to_match = ["t00z", "t01z", "t02z", "t03z", "t04z", "t05z", "t06z", "t07z", "t08z", "t09z", "t10z", "t11z", "t12z",
    "t13z", "t14z", "t15z", "t16z", "t17z", "t18z", "t19z", "t20z", "t21z", "t22z", "t23z"
    ]

    for root, dirs, files in os.walk(working_directory_grib):
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            files_in_subdir = os.listdir(subdir_path)

            # Check if any of the strings are present in the file names using regular expressions
            missing_strings = [string for string in strings_to_match if not any(re.search(rf"{string}", file) for file in files_in_subdir)]

            # Add missing strings to the subdirectory
            for missing_string in missing_strings:
                # Create a new file with the missing string
                file_name = f"{missing_string}_missing_file.grib2"
                file_path = os.path.join(subdir_path, file_name)
                with open(file_path, 'w') as dummy_file:
                    dummy_file.write("This is a dummy file that serves as a placeholder for a missing GRIB file.")


def delete_coordinates_file(working_directory_main):
    coordinates_filename = "GRIB_Nearest_Coordinates_Used.txt"
    coordinates_file_path = os.path.join(working_directory_main, coordinates_filename)

    # Check if the file exists, and if it does, delete it
    if os.path.exists(coordinates_file_path):
        os.remove(coordinates_file_path)


# This function gives the GRIB coordinates used, and sends them to an output file.
# We can check this output file to see the exact latitude and longitude that was
# chosen for each GRIB file. We would expect this value to be the same unless there
# was a change in the HRRR (or other model) grid cell locations or model resolution.
def nearest_coordinates_from_GRIB_files(working_directory_main, all_files, nearest_lat, nearest_lon):
    if nearest_lon == -999:
        nearest_lon_converted = nearest_lon
    else:
        nearest_lon_converted = nearest_lon - 360.0

    coordinates_filename = "GRIB_Nearest_Coordinates_Used.txt"
    coordinates_file_path = os.path.join(working_directory_main, coordinates_filename)

    # Open the file in append mode ('a') to write new data
    with open(coordinates_file_path, 'a') as file:
        for f in all_files:
            formatted_line = "{:<10} {:<10} {:<10}".format(f, nearest_lat, nearest_lon_converted)
            # Print for debugging
            # print(formatted_line)
            file.write(formatted_line + '\n')


def process_grib_files(working_directory_main, processed_data, all_files):
    delete_coordinates_file(working_directory_main)

    skip_file_path = "missing_file"
    ForGRIB_latitude = processed_data.get('latitude')
    ForGRIB_calculatedlongitude = processed_data.get('calculatedlongitude')

    resultsGRIBsetup = []

    for file_path in all_files:
        if skip_file_path in file_path:
            nearest_index = int(-999)
            nearest_distance = int(-999)
            nearest_lat = int(-999)
            nearest_lon = int(-999)
        else:
            with open(file_path, 'rb') as f:
                grib_message_handle = codes_grib_new_from_file(f)

                Nearestinfo = codes_grib_find_nearest(grib_message_handle, ForGRIB_latitude, ForGRIB_calculatedlongitude, is_lsm=False, npoints=1)
                NearestinfoDict = Nearestinfo[0]

                nearest_lat = NearestinfoDict['lat']
                nearest_lon = NearestinfoDict['lon']
                nearest_distance = NearestinfoDict['distance']
                nearest_index = NearestinfoDict['index']

        rounded_distance = round(nearest_distance, 3)
        resultsGRIBsetup.append((nearest_lat, nearest_lon, nearest_distance, nearest_index))
        print(f"File: {file_path} --> Data is {rounded_distance} kilometers from the requested location and the chosen grid cell is: {nearest_index}")

        # This is for coordinates output file.
        coordinates = nearest_coordinates_from_GRIB_files(working_directory_main, [file_path], nearest_lat, nearest_lon)

    print("")
    print("")

    return [item[3] for item in resultsGRIBsetup]


def grib_dictionary_from_inputs(processed_data):
    Dictionary_for_GRIB = {}

    BoundaryLayerHeightGRIB = processed_data.get('BoundaryLayerHeight')
    U_and_V_WindComponentGRIB = processed_data.get('U_and_V_WindComponent')
    TemperatureGRIB = processed_data.get('Temperature')
    TKEGRIB = processed_data.get('TKE')
    PRESGRIB = processed_data.get('PRES')
    SPFHGRIB = processed_data.get('SPFH')
    WindHeightLevel1GRIB = processed_data.get('WindHeightLevel1')
    WindHeightLevel2GRIB = processed_data.get('WindHeightLevel2')
    WindHeightLevel3GRIB = processed_data.get('WindHeightLevel3')
    WindHeightLevel4GRIB = processed_data.get('WindHeightLevel4')
    WindHeightLevel5GRIB = processed_data.get('WindHeightLevel5')
    WindHeightLevel6GRIB = processed_data.get('WindHeightLevel6')
    WindHeightLevel7GRIB = processed_data.get('WindHeightLevel7')
    WindHeightLevel8GRIB = processed_data.get('WindHeightLevel8')
    WindHeightLevel9GRIB = processed_data.get('WindHeightLevel9')
    WindHeightLevel10GRIB = processed_data.get('WindHeightLevel10')
    WindHeightLevel11GRIB = processed_data.get('WindHeightLevel11')
    WindHeightLevel12GRIB = processed_data.get('WindHeightLevel12')
    TemperatureHeightLevel1GRIB = processed_data.get('TemperatureHeightLevel1')
    TemperatureHeightLevel2GRIB = processed_data.get('TemperatureHeightLevel2')
    TemperatureHeightLevel3GRIB = processed_data.get('TemperatureHeightLevel3')
    TemperatureHeightLevel4GRIB = processed_data.get('TemperatureHeightLevel4')
    TemperatureHeightLevel5GRIB = processed_data.get('TemperatureHeightLevel5')
    TemperatureHeightLevel6GRIB = processed_data.get('TemperatureHeightLevel6')
    TemperatureHeightLevel7GRIB = processed_data.get('TemperatureHeightLevel7')
    TemperatureHeightLevel8GRIB = processed_data.get('TemperatureHeightLevel8')
    TemperatureHeightLevel9GRIB = processed_data.get('TemperatureHeightLevel9')
    TemperatureHeightLevel10GRIB = processed_data.get('TemperatureHeightLevel10')
    TemperatureHeightLevel11GRIB = processed_data.get('TemperatureHeightLevel11')
    TemperatureHeightLevel12GRIB = processed_data.get('TemperatureHeightLevel12')
    TKEHeightLevel1GRIB = processed_data.get('TKEHeightLevel1')
    TKEHeightLevel2GRIB = processed_data.get('TKEHeightLevel2')
    TKEHeightLevel3GRIB = processed_data.get('TKEHeightLevel3')
    TKEHeightLevel4GRIB = processed_data.get('TKEHeightLevel4')
    TKEHeightLevel5GRIB = processed_data.get('TKEHeightLevel5')
    TKEHeightLevel6GRIB = processed_data.get('TKEHeightLevel6')
    TKEHeightLevel7GRIB = processed_data.get('TKEHeightLevel7')
    TKEHeightLevel8GRIB = processed_data.get('TKEHeightLevel8')
    TKEHeightLevel9GRIB = processed_data.get('TKEHeightLevel9')
    TKEHeightLevel10GRIB = processed_data.get('TKEHeightLevel10')
    TKEHeightLevel11GRIB = processed_data.get('TKEHeightLevel11')
    TKEHeightLevel12GRIB = processed_data.get('TKEHeightLevel12')
    PRESHeightLevel1GRIB = processed_data.get('PRESHeightLevel1')
    PRESHeightLevel2GRIB = processed_data.get('PRESHeightLevel2')
    PRESHeightLevel3GRIB = processed_data.get('PRESHeightLevel3')
    PRESHeightLevel4GRIB = processed_data.get('PRESHeightLevel4')
    PRESHeightLevel5GRIB = processed_data.get('PRESHeightLevel5')
    PRESHeightLevel6GRIB = processed_data.get('PRESHeightLevel6')
    PRESHeightLevel7GRIB = processed_data.get('PRESHeightLevel7')
    PRESHeightLevel8GRIB = processed_data.get('PRESHeightLevel8')
    PRESHeightLevel9GRIB = processed_data.get('PRESHeightLevel9')
    PRESHeightLevel10GRIB = processed_data.get('PRESHeightLevel10')
    PRESHeightLevel11GRIB = processed_data.get('PRESHeightLevel11')
    PRESHeightLevel12GRIB = processed_data.get('PRESHeightLevel12')
    SPFHHeightLevel1GRIB = processed_data.get('SPFHHeightLevel1')
    SPFHHeightLevel2GRIB = processed_data.get('SPFHHeightLevel2')
    SPFHHeightLevel3GRIB = processed_data.get('SPFHHeightLevel3')
    SPFHHeightLevel4GRIB = processed_data.get('SPFHHeightLevel4')
    SPFHHeightLevel5GRIB = processed_data.get('SPFHHeightLevel5')
    SPFHHeightLevel6GRIB = processed_data.get('SPFHHeightLevel6')
    SPFHHeightLevel7GRIB = processed_data.get('SPFHHeightLevel7')
    SPFHHeightLevel8GRIB = processed_data.get('SPFHHeightLevel8')
    SPFHHeightLevel9GRIB = processed_data.get('SPFHHeightLevel9')
    SPFHHeightLevel10GRIB = processed_data.get('SPFHHeightLevel10')
    SPFHHeightLevel11GRIB = processed_data.get('SPFHHeightLevel11')
    SPFHHeightLevel12GRIB = processed_data.get('SPFHHeightLevel12')



    if U_and_V_WindComponentGRIB == "yes":
        strUandV = "yes"
    else:
        strUandV = "no"

    if TemperatureGRIB == "yes":
        strTMP = "yes"
    else:
        strTMP = "no"

    if TKEGRIB == "yes":
        strTKE = "yes"
    else:
        strTKE = "no"

    if PRESGRIB == "yes":
        strPRES = "yes"
    else:
        strPRES = "no"

    if SPFHGRIB == "yes":
        strSPFH = "yes"
    else:
        strSPFH = "no"

    if BoundaryLayerHeightGRIB == "yes":
        BLH = "blh"
        LBLH = "0"

    # Below are for the levels (actual level in GRIB file)

    LBLH = ""
    LWHGT1 = ""
    LWHGT2 = ""
    LWHGT3 = ""
    LWHGT4 = ""
    LWHGT5 = ""
    LWHGT6 = ""
    LWHGT7 = ""
    LWHGT8 = ""
    LWHGT9 = ""
    LWHGT10 = ""
    LWHGT11 = ""
    LWHGT12 = ""
    LTHGT1 = ""
    LTHGT2 = ""
    LTHGT3 = ""
    LTHGT4 = ""
    LTHGT5 = ""
    LTHGT6 = ""
    LTHGT7 = ""
    LTHGT8 = ""
    LTHGT9 = ""
    LTHGT10 = ""
    LTHGT11 = ""
    LTHGT12 = ""
    LTKEHGT1 = ""
    LTKEHGT2 = ""
    LTKEHGT3 = ""
    LTKEHGT4 = ""
    LTKEHGT5 = ""
    LTKEHGT6 = ""
    LTKEHGT7 = ""
    LTKEHGT8 = ""
    LTKEHGT9 = ""
    LTKEHGT10 = ""
    LTKEHGT11 = ""
    LTKEHGT12 = ""
    LPRESHGT1 = ""
    LPRESHGT2 = ""
    LPRESHGT3 = ""
    LPRESHGT4 = ""
    LPRESHGT5 = ""
    LPRESHGT6 = ""
    LPRESHGT7 = ""
    LPRESHGT8 = ""
    LPRESHGT9 = ""
    LPRESHGT10 = ""
    LPRESHGT11 = ""
    LPRESHGT12 = ""
    LSPFHHGT1 = ""
    LSPFHHGT2 = ""
    LSPFHHGT3 = ""
    LSPFHHGT4 = ""
    LSPFHHGT5 = ""
    LSPFHHGT6 = ""
    LSPFHHGT7 = ""
    LSPFHHGT8 = ""
    LSPFHHGT9 = ""
    LSPFHHGT10 = ""
    LSPFHHGT11 = ""
    LSPFHHGT12 = ""

    # Below are for the shortNames (actual name in GRIB file)

    BLH = ""
    UWHGT1 = ""
    UWHGT2 = ""
    UWHGT3 = ""
    UWHGT4 = ""
    UWHGT5 = ""
    UWHGT6 = ""
    UWHGT7 = ""
    UWHGT8 = ""
    UWHGT9 = ""
    UWHGT10 = ""
    UWHGT11 = ""
    UWHGT12 = ""
    VWHGT1 = ""
    VWHGT2 = ""
    VWHGT3 = ""
    VWHGT4 = ""
    VWHGT5 = ""
    VWHGT6 = ""
    VWHGT7 = ""
    VWHGT8 = ""
    VWHGT9 = ""
    VWHGT10 = ""
    VWHGT11 = ""
    VWHGT12 = ""
    THGT1 = ""
    THGT2 = ""
    THGT3 = ""
    THGT4 = ""
    THGT5 = ""
    THGT6 = ""
    THGT7 = ""
    THGT8 = ""
    THGT9 = ""
    THGT10 = ""
    THGT11 = ""
    THGT12 = ""
    TKEHGT1 = ""
    TKEHGT2 = ""
    TKEHGT3 = ""
    TKEHGT4 = ""
    TKEHGT5 = ""
    TKEHGT6 = ""
    TKEHGT7 = ""
    TKEHGT8 = ""
    TKEHGT9 = ""
    TKEHGT10 = ""
    TKEHGT11 = ""
    TKEHGT12 = ""
    PRESHGT1 = ""
    PRESHGT2 = ""
    PRESHGT3 = ""
    PRESHGT4 = ""
    PRESHGT5 = ""
    PRESHGT6 = ""
    PRESHGT7 = ""
    PRESHGT8 = ""
    PRESHGT9 = ""
    PRESHGT10 = ""
    PRESHGT11 = ""
    PRESHGT12 = ""
    SPFHHGT1 = ""
    SPFHHGT2 = ""
    SPFHHGT3 = ""
    SPFHHGT4 = ""
    SPFHHGT5 = ""
    SPFHHGT6 = ""
    SPFHHGT7 = ""
    SPFHHGT8 = ""
    SPFHHGT9 = ""
    SPFHHGT10 = ""
    SPFHHGT11 = ""
    SPFHHGT12 = ""

    # Below variables are assigned only if they were requested

    # Boundary Layer Height**************************************************************

    if BoundaryLayerHeightGRIB == "yes":
        BLH = "blh"
        LBLH = "0"

    # WIND**************************************************************

    if WindHeightLevel1GRIB == "yes" and strUandV == "yes":
        UWHGT1 = "u"
        VWHGT1 = "v"
        LWHGT1 = "1"

    if WindHeightLevel2GRIB == "yes" and strUandV == "yes":
        UWHGT2 = "u"
        VWHGT2 = "v"
        LWHGT2 = "2"

    if WindHeightLevel3GRIB == "yes" and strUandV == "yes":
        UWHGT3 = "u"
        VWHGT3 = "v"
        LWHGT3 = "3"

    if WindHeightLevel4GRIB == "yes" and strUandV == "yes":
        UWHGT4 = "u"
        VWHGT4 = "v"
        LWHGT4 = "4"

    if WindHeightLevel5GRIB == "yes" and strUandV == "yes":
        UWHGT5 = "u"
        VWHGT5 = "v"
        LWHGT5 = "5"

    if WindHeightLevel6GRIB == "yes" and strUandV == "yes":
        UWHGT6 = "u"
        VWHGT6 = "v"
        LWHGT6 = "6"

    if WindHeightLevel7GRIB == "yes" and strUandV == "yes":
        UWHGT7 = "u"
        VWHGT7 = "v"
        LWHGT7 = "7"

    if WindHeightLevel8GRIB == "yes" and strUandV == "yes":
        UWHGT8 = "u"
        VWHGT8 = "v"
        LWHGT8 = "8"

    if WindHeightLevel9GRIB == "yes" and strUandV == "yes":
        UWHGT9 = "u"
        VWHGT9 = "v"
        LWHGT9 = "9"

    if WindHeightLevel10GRIB == "yes" and strUandV == "yes":
        UWHGT10 = "u"
        VWHGT10 = "v"
        LWHGT10 = "10"

    if WindHeightLevel11GRIB == "yes" and strUandV == "yes":
        UWHGT11 = "u"
        VWHGT11 = "v"
        LWHGT11 = "11"

    if WindHeightLevel12GRIB == "yes" and strUandV == "yes":
        UWHGT12 = "u"
        VWHGT12 = "v"
        LWHGT12 = "12"

    # TEMPERATURE**************************************************************

    if TemperatureHeightLevel1GRIB == "yes" and strTMP == "yes":
        THGT1 = "t"
        LTHGT1 = "1"

    if TemperatureHeightLevel2GRIB == "yes" and strTMP == "yes":
        THGT2 = "t"
        LTHGT2 = "2"

    if TemperatureHeightLevel3GRIB == "yes" and strTMP == "yes":
        THGT3 = "t"
        LTHGT3 = "3"

    if TemperatureHeightLevel4GRIB == "yes" and strTMP == "yes":
        THGT4 = "t"
        LTHGT4 = "4"

    if TemperatureHeightLevel5GRIB == "yes" and strTMP == "yes":
        THGT5 = "t"
        LTHGT5 = "5"

    if TemperatureHeightLevel6GRIB == "yes" and strTMP == "yes":
        THGT6 = "t"
        LTHGT6 = "6"

    if TemperatureHeightLevel7GRIB == "yes" and strTMP == "yes":
        THGT7 = "t"
        LTHGT7 = "7"

    if TemperatureHeightLevel8GRIB == "yes" and strTMP == "yes":
        THGT8 = "t"
        LTHGT8 = "8"

    if TemperatureHeightLevel9GRIB == "yes" and strTMP == "yes":
        THGT9 = "t"
        LTHGT9 = "9"

    if TemperatureHeightLevel10GRIB == "yes" and strTMP == "yes":
        THGT10 = "t"
        LTHGT10 = "10"

    if TemperatureHeightLevel11GRIB == "yes" and strTMP == "yes":
        THGT11 = "t"
        LTHGT11 = "11"

    if TemperatureHeightLevel12GRIB == "yes" and strTMP == "yes":
        THGT12 = "t"
        LTHGT12 = "12"

    # TKE**************************************************************

    if TKEHeightLevel1GRIB == "yes" and strTKE == "yes":
        TKEHGT1 = "tke"
        LTKEHGT1 = "1"

    if TKEHeightLevel2GRIB == "yes" and strTKE == "yes":
        TKEHGT2 = "tke"
        LTKEHGT2 = "2"

    if TKEHeightLevel3GRIB == "yes" and strTKE == "yes":
        TKEHGT3 = "tke"
        LTKEHGT3 = "3"

    if TKEHeightLevel4GRIB == "yes" and strTKE == "yes":
        TKEHGT4 = "tke"
        LTKEHGT4 = "4"

    if TKEHeightLevel5GRIB == "yes" and strTKE == "yes":
        TKEHGT5 = "tke"
        LTKEHGT5 = "5"

    if TKEHeightLevel6GRIB == "yes" and strTKE == "yes":
        TKEHGT6 = "tke"
        LTKEHGT6 = "6"

    if TKEHeightLevel7GRIB == "yes" and strTKE == "yes":
        TKEHGT7 = "tke"
        LTKEHGT7 = "7"

    if TKEHeightLevel8GRIB == "yes" and strTKE == "yes":
        TKEHGT8 = "tke"
        LTKEHGT8 = "8"

    if TKEHeightLevel9GRIB == "yes" and strTKE == "yes":
        TKEHGT9 = "tke"
        LTKEHGT9 = "9"

    if TKEHeightLevel10GRIB == "yes" and strTKE == "yes":
        TKEHGT10 = "tke"
        LTKEHGT10 = "10"

    if TKEHeightLevel11GRIB == "yes" and strTKE == "yes":
        TKEHGT11 = "tke"
        LTKEHGT11 = "11"

    if TKEHeightLevel12GRIB == "yes" and strTKE == "yes":
        TKEHGT12 = "tke"
        LTKEHGT12 = "12"

    # Pressure**************************************************************

    if PRESHeightLevel1GRIB == "yes" and strPRES == "yes":
        PRESHGT1 = "pres"
        LPRESHGT1 = "1"

    if PRESHeightLevel2GRIB == "yes" and strPRES == "yes":
        PRESHGT2 = "pres"
        LPRESHGT2 = "2"

    if PRESHeightLevel3GRIB == "yes" and strPRES == "yes":
        PRESHGT3 = "pres"
        LPRESHGT3 = "3"

    if PRESHeightLevel4GRIB == "yes" and strPRES == "yes":
        PRESHGT4 = "pres"
        LPRESHGT4 = "4"

    if PRESHeightLevel5GRIB == "yes" and strPRES == "yes":
        PRESHGT5 = "pres"
        LPRESHGT5 = "5"

    if PRESHeightLevel6GRIB == "yes" and strPRES == "yes":
        PRESHGT6 = "pres"
        LPRESHGT6 = "6"

    if PRESHeightLevel7GRIB == "yes" and strPRES == "yes":
        PRESHGT7 = "pres"
        LPRESHGT7 = "7"

    if PRESHeightLevel8GRIB == "yes" and strPRES == "yes":
        PRESHGT8 = "pres"
        LPRESHGT8 = "8"

    if PRESHeightLevel9GRIB == "yes" and strPRES == "yes":
        PRESHGT9 = "pres"
        LPRESHGT9 = "9"

    if PRESHeightLevel10GRIB == "yes" and strPRES == "yes":
        PRESHGT10 = "pres"
        LPRESHGT10 = "10"

    if PRESHeightLevel11GRIB == "yes" and strPRES == "yes":
        PRESHGT11 = "pres"
        LPRESHGT11 = "11"

    if PRESHeightLevel12GRIB == "yes" and strPRES == "yes":
        PRESHGT12 = "pres"
        LPRESHGT12 = "12"

    # Specific Humidity**************************************************************

    if SPFHHeightLevel1GRIB == "yes" and strSPFH == "yes":
        SPFHHGT1 = "q"
        LSPFHHGT1 = "1"

    if SPFHHeightLevel2GRIB == "yes" and strSPFH == "yes":
        SPFHHGT2 = "q"
        LSPFHHGT2 = "2"

    if SPFHHeightLevel3GRIB == "yes" and strSPFH == "yes":
        SPFHHGT3 = "q"
        LSPFHHGT3 = "3"

    if SPFHHeightLevel4GRIB == "yes" and strSPFH == "yes":
        SPFHHGT4 = "q"
        LSPFHHGT4 = "4"

    if SPFHHeightLevel5GRIB == "yes" and strSPFH == "yes":
        SPFHHGT5 = "q"
        LSPFHHGT5 = "5"

    if SPFHHeightLevel6GRIB == "yes" and strSPFH == "yes":
        SPFHHGT6 = "q"
        LSPFHHGT6 = "6"

    if SPFHHeightLevel7GRIB == "yes" and strSPFH == "yes":
        SPFHHGT7 = "q"
        LSPFHHGT7 = "7"

    if SPFHHeightLevel8GRIB == "yes" and strSPFH == "yes":
        SPFHHGT8 = "q"
        LSPFHHGT8 = "8"

    if SPFHHeightLevel9GRIB == "yes" and strSPFH == "yes":
        SPFHHGT9 = "q"
        LSPFHHGT9 = "9"

    if SPFHHeightLevel10GRIB == "yes" and strSPFH == "yes":
        SPFHHGT10 = "q"
        LSPFHHGT10 = "10"

    if SPFHHeightLevel11GRIB == "yes" and strSPFH == "yes":
        SPFHHGT11 = "q"
        LSPFHHGT11 = "11"

    if SPFHHeightLevel12GRIB == "yes" and strSPFH == "yes":
        SPFHHGT12 = "q"
        LSPFHHGT12 = "12"


    # Now we are trying to add the requested stuff to the dictionary.
    # The key should be the shortName and the value should be the level.

    if BoundaryLayerHeightGRIB == "yes":
        key1 = BLH
        value1 = LBLH
        if key1 not in Dictionary_for_GRIB:
            Dictionary_for_GRIB[key1] = []
        Dictionary_for_GRIB[key1].append(value1)


    if strUandV == "yes":
        wind_height_levels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

        for level in wind_height_levels:
            if eval(f"WindHeightLevel{level}GRIB") == "yes":
                key_u = eval(f"UWHGT{level}")
                key_v = eval(f"VWHGT{level}")
                value = eval(f"LWHGT{level}")

                for key in (key_u, key_v):
                    if key not in Dictionary_for_GRIB:
                        Dictionary_for_GRIB[key] = []
                    Dictionary_for_GRIB[key].append(value)


    if strTMP == "yes":
        temp_height_levels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

        for level in temp_height_levels:
            if eval(f"TemperatureHeightLevel{level}GRIB") == "yes":
                key_t = eval(f"THGT{level}")
                value = eval(f"LTHGT{level}")

                for key in (key_t):
                    if key not in Dictionary_for_GRIB:
                        Dictionary_for_GRIB[key] = []
                    Dictionary_for_GRIB[key].append(value)


    if strSPFH == "yes":
        specific_humidity_height_levels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

        for level in specific_humidity_height_levels:
            if eval(f"SPFHHeightLevel{level}GRIB") == "yes":
                key_q = eval(f"SPFHHGT{level}")
                value = eval(f"LSPFHHGT{level}")

                for key in (key_q):
                    if key not in Dictionary_for_GRIB:
                        Dictionary_for_GRIB[key] = []
                    Dictionary_for_GRIB[key].append(value)


    if strTKE == "yes":
        TKE_height_levels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

        for level in TKE_height_levels:
            if eval(f"TKEHeightLevel{level}GRIB") == "yes":
                key_tke = eval(f"TKEHGT{level}")
                value = eval(f"LTKEHGT{level}")

                for key in [key_tke]: # Note the [] instead of the ()
                    if key not in Dictionary_for_GRIB:
                        Dictionary_for_GRIB[key] = []
                    Dictionary_for_GRIB[key].append(value)


    if strPRES == "yes":
        PRES_height_levels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

        for level in PRES_height_levels:
            if eval(f"PRESHeightLevel{level}GRIB") == "yes":
                key_pres = eval(f"PRESHGT{level}")
                value = eval(f"LPRESHGT{level}")

                for key in [key_pres]: # Note the [] instead of the ()
                    if key not in Dictionary_for_GRIB:
                        Dictionary_for_GRIB[key] = []
                    Dictionary_for_GRIB[key].append(value)



    # Now we are making 2 lists that populate based on the dictionary created.

    GRIB_shortName = []
    GRIB_level = []

    for key, values in Dictionary_for_GRIB.items():
        if values:
            for value in values:
                GRIB_shortName.append(key)
                GRIB_level.append(value)
                # print(f'GRIB_shortName: {GRIB_shortName}, GRIB_level: {GRIB_level}')
    print("")
    print("")
    print(f'GRIB shortName list requested: {GRIB_shortName}')
    print(f'GRIB level list requested:     {GRIB_level}')
    print("")
    print("")

    return GRIB_shortName, GRIB_level


# Function not currently used.
def file_identifier(all_files):
    GRIB_files = []
    missing_files = []

    for file_name in all_files:
        if "missing_file" in file_name:
            missing_files.append(file_name)
        else:
            GRIB_files.append(file_name)
        print(file_name)

    return GRIB_files, missing_files


def dict_constructor():
    build_dict = {}

    return build_dict


# The code for this function is somewhat messy, but it functions as intended.
# If future improvements are planned, it would be advisable to explore alternative approaches.
def extract_value_at_grid_index(all_files, grid_cell_data, GRIB_shortName, GRIB_level, extracted_time_values, build_dict):
    """
    Extracts values at a given grid index from GRIB files and populates a dictionary.

    Args:
        all_files (list): List of file paths.
        grid_cell_data (list): List of grid indices.
        GRIB_shortName (list): List of GRIB shorNames.
        GRIB_level (list): List of GRIB levels.
        extracted_time_values (list): List of (time, data_date) tuples.
        build_dict (dict): Dictionary to store extracted data.

    Returns:
        dict: The populated dictionary.
    """

    VERBOSE = 1  # verbose error reporting
    skip_file_path = "missing_file" # This is used to handle "fake" (non-binary) GRIB files.

    GRIB_level_str = GRIB_level
    GRIB_level_int = []

    for item in GRIB_level_str:
        try:
            integer_value = int(item)
            GRIB_level_int.append(integer_value)
        except ValueError:
            print(f"Unable to convert {item} to an integer")

    for idx, file_path in enumerate(all_files):
        time, data_date = extracted_time_values[idx]  # Access time and data_date from the extracted_time_values list

        if skip_file_path in file_path:
            for shortName, level in zip(GRIB_shortName, GRIB_level_int):

                if (shortName, level) not in build_dict:
                    build_dict[(shortName, level)] = []

                # Assign a string of "missing" without processing the file
                build_dict[(shortName, level)].append((file_path, level, shortName, str("missing"), time, data_date))
        else:
            f = open(file_path, 'rb')
            keys = [
                'level',
                'shortName',
            ]
            grid_index = grid_cell_data[idx]  # Get the grid_index for the current file

            for shortName, level in zip(GRIB_shortName, GRIB_level_int):
                try:

                    info_found = False  # Flag to track whether the tuple was found in the GRIB file.
                    f.seek(0)  # Reset the file pointer to the beginning
                    while 1:
                        gid = codes_grib_new_from_file(f)
                        if gid is None:
                            break

                        if (shortName, level) not in build_dict:
                            build_dict[(shortName, level)] = []

                        if (codes_get(gid, 'level') == int(level) and
                            codes_get(gid, 'shortName') == shortName):

                            values = codes_get_array(gid, 'values')  # Get the values as a list

                            if grid_index >= 0 and grid_index < len(values):
                                value_at_index = values[grid_index]
                                if (file_path, level, shortName, value_at_index, time, data_date) not in build_dict[(shortName, level)]:
                                    build_dict[(shortName, level)].append((file_path, level, shortName, value_at_index, time, data_date))
                                    print(f'File: {file_path} Date: {data_date} Time: {time} Variable: {shortName} Level: {level} Value: {value_at_index}')

                            info_found = True  # Flag to track whether the tuple was found in the GRIB file.
                        codes_release(gid)

                except CodesInternalError as err:
                    if VERBOSE:
                        traceback.print_exc(file=sys.stderr)
                    else:
                        sys.stderr.write(err.msg + '\n')

                if not info_found:
                    value_at_index = -9999.999
                if (file_path, level, shortName, value_at_index, time, data_date) not in build_dict[(shortName, level)]:
                    build_dict[(shortName, level)].append((file_path, level, shortName, value_at_index, time, data_date))

            f.close()
    extracted_values_dict = build_dict

    return extracted_values_dict


def extract_time_info_from_grib_files(all_files):
    VERBOSE = 1  # verbose error reporting
    skip_file_path = "missing_file"
    extracted_time_values = []

    for file_path in all_files:
        if skip_file_path in file_path:
            time = str("Not_Available")
            data_date = str("Not_Available")
        else:
            try:
                f = open(file_path, 'rb')
                gid = codes_grib_new_from_file(f)

                time = codes_get(gid, 'time')
                data_date = codes_get(gid, 'dataDate')

                codes_release(gid)
                f.close()

            except CodesInternalError as err:
                if VERBOSE:
                    traceback.print_exc(file=sys.stderr)
                else:
                    sys.stderr.write(err.msg + '\n')

        extracted_time_values.append((time, data_date))
        print(f"File: {file_path} --> The date is: {data_date} --> The time is: {time}")

    return extracted_time_values

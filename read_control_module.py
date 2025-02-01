# Goal: Read from the input file, called "Control.txt" by default.

import os


def read_control_file(working_directory_main, control_filename):
    control_file_path = os.path.join(working_directory_main, control_filename)
    with open(control_file_path, 'r') as file:
        control_data = {}
        for line in file:
            line = line.strip()

            if '#' in line:
                line = line.split('#', 1)[0].strip()

            if ':' in line:
                key, value = line.split(':', 1)
                control_data[key.strip()] = value.strip()
    return control_data


def process_control_data(control_data):

    lat_str = control_data.get('Latitude', None)
    try:
        lat = float(lat_str)
    except ValueError:
        lat = None

    inputlong = control_data.get('Longitude', None)

    long_str = control_data.get('Longitude', None)
    try:
        calclong = float(long_str)
        if calclong is not None:
            calclong += 360
    except ValueError:
        calclong = None

    processed_data = {
        'main_output': control_data.get('Main output file name', None),
        'Input_Out_File': control_data.get('Inputs Used Outfile Name', None),
        'output_directory': control_data.get('Output Directory', None),
        'GRIB_files_location': control_data.get('GRIB files location', None),
        'latitude': lat,
        'inputlongitude': inputlong,
        'calculatedlongitude': calclong,
        'BoundaryLayerHeight': control_data.get('Boundary Layer Height?',
                                                None),
        'U_and_V_WindComponent': control_data.get('U and V Wind Component?',
                                                  None),
        'WindHeightLevel1': control_data.get('Wind Height Level 1', None),
        'WindHeightLevel2': control_data.get('Wind Height Level 2', None),
        'WindHeightLevel3': control_data.get('Wind Height Level 3', None),
        'WindHeightLevel4': control_data.get('Wind Height Level 4', None),
        'WindHeightLevel5': control_data.get('Wind Height Level 5', None),
        'WindHeightLevel6': control_data.get('Wind Height Level 6', None),
        'WindHeightLevel7': control_data.get('Wind Height Level 7', None),
        'WindHeightLevel8': control_data.get('Wind Height Level 8', None),
        'WindHeightLevel9': control_data.get('Wind Height Level 9', None),
        'WindHeightLevel10': control_data.get('Wind Height Level 10', None),
        'WindHeightLevel11': control_data.get('Wind Height Level 11', None),
        'WindHeightLevel12': control_data.get('Wind Height Level 12', None),
        'Temperature': control_data.get('Temperature?', None),
        'TemperatureHeightLevel1': control_data.get(
            'Temperature Height Level 1', None),
        'TemperatureHeightLevel2': control_data.get(
            'Temperature Height Level 2', None),
        'TemperatureHeightLevel3': control_data.get(
            'Temperature Height Level 3', None),
        'TemperatureHeightLevel4': control_data.get(
            'Temperature Height Level 4', None),
        'TemperatureHeightLevel5': control_data.get(
            'Temperature Height Level 5', None),
        'TemperatureHeightLevel6': control_data.get(
            'Temperature Height Level 6', None),
        'TemperatureHeightLevel7': control_data.get(
            'Temperature Height Level 7', None),
        'TemperatureHeightLevel8': control_data.get(
            'Temperature Height Level 8', None),
        'TemperatureHeightLevel9': control_data.get(
            'Temperature Height Level 9', None),
        'TemperatureHeightLevel10': control_data.get(
            'Temperature Height Level 10', None),
        'TemperatureHeightLevel11': control_data.get(
            'Temperature Height Level 11', None),
        'TemperatureHeightLevel12': control_data.get(
            'Temperature Height Level 12', None),
        'TKE': control_data.get('Turbulent Kinetic Energy?', None),
        'TKEHeightLevel1': control_data.get(
            'Turbulent Kinetic Energy Level 1', None),
        'TKEHeightLevel2': control_data.get(
            'Turbulent Kinetic Energy Level 2', None),
        'TKEHeightLevel3': control_data.get(
            'Turbulent Kinetic Energy Level 3', None),
        'TKEHeightLevel4': control_data.get(
            'Turbulent Kinetic Energy Level 4', None),
        'TKEHeightLevel5': control_data.get(
            'Turbulent Kinetic Energy Level 5', None),
        'TKEHeightLevel6': control_data.get(
            'Turbulent Kinetic Energy Level 6', None),
        'TKEHeightLevel7': control_data.get(
            'Turbulent Kinetic Energy Level 7', None),
        'TKEHeightLevel8': control_data.get(
            'Turbulent Kinetic Energy Level 8', None),
        'TKEHeightLevel9': control_data.get(
            'Turbulent Kinetic Energy Level 9', None),
        'TKEHeightLevel10': control_data.get(
            'Turbulent Kinetic Energy Level 10', None),
        'TKEHeightLevel11': control_data.get(
            'Turbulent Kinetic Energy Level 11', None),
        'TKEHeightLevel12': control_data.get(
            'Turbulent Kinetic Energy Level 12', None),
        'PRES': control_data.get('Pressure?', None),
        'PRESHeightLevel1': control_data.get('Pressure Level 1', None),
        'PRESHeightLevel2': control_data.get('Pressure Level 2', None),
        'PRESHeightLevel3': control_data.get('Pressure Level 3', None),
        'PRESHeightLevel4': control_data.get('Pressure Level 4', None),
        'PRESHeightLevel5': control_data.get('Pressure Level 5', None),
        'PRESHeightLevel6': control_data.get('Pressure Level 6', None),
        'PRESHeightLevel7': control_data.get('Pressure Level 7', None),
        'PRESHeightLevel8': control_data.get('Pressure Level 8', None),
        'PRESHeightLevel9': control_data.get('Pressure Level 9', None),
        'PRESHeightLevel10': control_data.get('Pressure Level 10', None),
        'PRESHeightLevel11': control_data.get('Pressure Level 11', None),
        'PRESHeightLevel12': control_data.get('Pressure Level 12', None),
        'SPFH': control_data.get('Specific Humidity?', None),
        'SPFHHeightLevel1': control_data.get('Specific Humidity Level 1',
                                             None),
        'SPFHHeightLevel2': control_data.get('Specific Humidity Level 2',
                                             None),
        'SPFHHeightLevel3': control_data.get('Specific Humidity Level 3',
                                             None),
        'SPFHHeightLevel4': control_data.get('Specific Humidity Level 4',
                                             None),
        'SPFHHeightLevel5': control_data.get('Specific Humidity Level 5',
                                             None),
        'SPFHHeightLevel6': control_data.get('Specific Humidity Level 6',
                                             None),
        'SPFHHeightLevel7': control_data.get('Specific Humidity Level 7',
                                             None),
        'SPFHHeightLevel8': control_data.get('Specific Humidity Level 8',
                                             None),
        'SPFHHeightLevel9': control_data.get('Specific Humidity Level 9',
                                             None),
        'SPFHHeightLevel10': control_data.get('Specific Humidity Level 10',
                                              None),
        'SPFHHeightLevel11': control_data.get('Specific Humidity Level 11',
                                              None),
        'SPFHHeightLevel12': control_data.get('Specific Humidity Level 12',
                                              None),

        'StartDate': control_data.get('Start Date', None),
        'EndDate': control_data.get('End Date', None),
        'HerbieAlreadyDone': control_data.get('Herbie Already Done?', None)
    }
    return processed_data

from datetime import datetime, timedelta
import re
import os
import sys

import constants
from met_calcs import convert_longitude


def total_file_count(hours_per_folder, dir_file_count):
    x = len(hours_per_folder) / 3

    #print(len(dir_file_count))
    total = x * len(dir_file_count)
    return total


def expected_file_count(processed_data):
    # File count if we only produce nat or prs files.
    dir_file_count = 24
    if processed_data.get('wrf') == "yes":
        dir_file_count = 48

    if processed_data.get('BoundaryLayerHeight') == "yes" and (
            processed_data.get('U_and_V_WindComponent') == "yes" or
            processed_data.get('Temperature') == "yes" or
            processed_data.get('TKE') == "yes" or
            processed_data.get('PRES') == "yes" or
            processed_data.get('SPFH') == "yes"):
        dir_file_count = 48

    return dir_file_count



def files_to_subset(working_directory_grib):
    all_files = []

    # Walk through the directory
    for root, dirs, files in os.walk(working_directory_grib):
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)

            # Get the list of files in the current subdirectory
            files_in_subdir = os.listdir(subdir_path)

            # Add files that do not contain the string "regional" in their name
            for file in files_in_subdir:
                if "regional" not in file:  # Only add files that do NOT contain "regional"
                    all_files.append(os.path.join(subdir_path, file))

    # Sort the files based on directory name and hour extracted from filename
    all_files.sort(
        key=lambda x: (
            os.path.basename(os.path.dirname(x)),  # Sort by subdirectory name
            extract_hour_from_filename(os.path.basename(x))  # Sort by hour
        )
    )

    return all_files








def get_date_range(processed_data):
    """Extracts and validates the start and end dates from processed_data."""
    start_date_str = processed_data.get('StartDate')
    end_date_str = processed_data.get('EndDate')

    if not start_date_str or not end_date_str:
        print("Error: StartDate or EndDate not found in processed_data.")
        return None, None

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        return start_date, end_date
    except ValueError as e:
        print(f"Error: Invalid date format - {e}")
        return None, None


def generate_datetime_range(start_date, end_date):
    current_date = start_date
    datetime_list = []
    while current_date <= end_date:
        for hour in range(24):
            date_str = current_date.replace(hour=hour).strftime("%Y-%m-%d %H")
            datetime_list.append(date_str)
            #print(datetime_list)
        current_date += timedelta(days=1)  # Move to next day

    return datetime_list


def extract_hour_from_filename(file_name):
    # Search for a pattern "tXX" within the file name
    match = re.search(r't(\d{2})', file_name)

    if match:
        return int(match.group(1))
    return -1


def files_to_do_work_for(working_directory_grib, processed_data):
    ForGRIB_StartDate = processed_data.get('StartDate')
    ForGRIB_EndDate = processed_data.get('EndDate')
    all_files_prs = []
    all_files_nat = []
    ForGRIB_StartDateNodash = int(ForGRIB_StartDate.replace("-", ""))
    ForGRIB_EndDateNodash = int(ForGRIB_EndDate.replace("-", ""))

    for root, dirs, files in os.walk(working_directory_grib):

        subdirs_to_remove = []
        for dir_name in dirs:

            if (int(dir_name) > ForGRIB_EndDateNodash or
                    int(dir_name) < ForGRIB_StartDateNodash):
                subdirs_to_remove.append(dir_name)

        for subdir in subdirs_to_remove:
            dirs.remove(subdir)

        for file in files:
            if file.endswith("prsf00.grib2"):
                file_path = os.path.join(root, file)
                all_files_prs.append(file_path)
            if file.endswith("natf00.grib2"):
                file_path = os.path.join(root, file)
                all_files_nat.append(file_path)

        # Sort all files based on the date and hour components in the
        # directory and file names
        all_files_prs.sort(
            key=lambda x: (os.path.basename(os.path.dirname(x)),
                           extract_hour_from_filename(os.path.basename(x))))
        all_files_nat.sort(
            key=lambda x: (os.path.basename(os.path.dirname(x)),
                           extract_hour_from_filename(os.path.basename(x))))
        # Print for debugging
        #print(all_files_prs)
        #print(all_files_nat)

    return all_files_prs, all_files_nat
















def match_strings_and_add_dummy_files(working_directory_grib):
    # Define the strings to match
    strings_to_match = ["t00z", "t01z", "t02z", "t03z", "t04z", "t05z",
                        "t06z", "t07z", "t08z", "t09z", "t10z", "t11z",
                        "t12z", "t13z", "t14z", "t15z", "t16z", "t17z",
                        "t18z", "t19z", "t20z",
                        "t21z", "t22z", "t23z"]

    dummy_files_made = False
    for root, dirs, files in os.walk(working_directory_grib):
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            files_in_subdir = os.listdir(subdir_path)

            # Check if any of the strings are present in the file names
            # using regular expressions
            missing_strings = [string for string in strings_to_match
                               if not any(re.search(rf"{string}", file)
                                          for file in files_in_subdir)]

            # Add missing strings to the subdirectory
            for missing_string in missing_strings:
                # Create a new file with the missing string
                file_name = f"{missing_string.replace(
                    'z', 'NoData')}_missing_file.grib2"
                file_path = os.path.join(subdir_path, file_name)
                with open(file_path, 'w') as dummy_file:
                    dummy_file.write("This is a dummy file that "
                                     "serves as a placeholder "
                                     "for a missing GRIB file.")

                dummy_files_made = True
    if dummy_files_made:
        print("WARNING: DUMMY FILE(S) MADE!\n")
        print("There is currently no way to proceed without having\n"
              "all the required files and/or have them named properly.\n"
              "This likely means Herbie failed to download a file,\n"
              "but I am not sure. It could also mean that you forgot\n"
              "to run Herbie.")
        sys.exit(1)


def write_coordinates_to_file(working_directory_main, all_files,
                              nearest_lat, nearest_lon_converted):
    coordinates_file_path = os.path.join(working_directory_main,
                                         constants.coordinates_filename)

    with open(coordinates_file_path, 'a') as file:
        for f in all_files:
            formatted_line = "{:<10} {:<10} {:<10}".format(
                f, nearest_lat, nearest_lon_converted)
            file.write(formatted_line + '\n')


# This function gives the GRIB coordinates used, and sends them to
# an output file. We can check this output file to see the exact latitude
# and longitude that was chosen for each GRIB file. We would expect this
# value to be the same unless there was a change in the HRRR (or other model)
# grid cell locations or model resolution.
def nearest_coordinates_from_GRIB_files(working_directory_main, all_files,
                                        nearest_lat, nearest_lon):
    nearest_lon_converted = convert_longitude(nearest_lon)
    write_coordinates_to_file(working_directory_main, all_files,
                              nearest_lat, nearest_lon_converted)


def delete_coordinates_file(working_directory_main):
    coordinates_file_path = os.path.join(working_directory_main,
                                         constants.coordinates_filename)

    # Check if the file exists, and if it does, delete it
    if os.path.exists(coordinates_file_path):
        os.remove(coordinates_file_path)


# This function makes all times based on the requested range.
# It makes the "reference" columns.
def make_all_times(processed_data):
    StartDate_Out = processed_data.get('StartDate')
    EndDate_Out = processed_data.get('EndDate')
    StartDate_OutNodash = int(StartDate_Out.replace("-", ""))
    EndDate_OutNodash = int(EndDate_Out.replace("-", ""))

    start_date = datetime.strptime(str(StartDate_OutNodash), "%Y%m%d")
    end_date = datetime.strptime(str(EndDate_OutNodash), "%Y%m%d")

    num_days = (end_date - start_date).days + 1  # +1 to include the start date

    years, months, days, hours, hours_ending = [], [], [], [], []
    current_date = start_date
    while current_date <= end_date:
        for hour in range(24):
            years.append(current_date.year)
            months.append(current_date.month)
            days.append(current_date.day)
            hours.append(hour)
            # Convert to hour ending format
            hours_ending.append(hour + 1 if hour < 23 else 24)
            current_date += timedelta(hours=1)

    return years, months, days, hours, hours_ending, num_days



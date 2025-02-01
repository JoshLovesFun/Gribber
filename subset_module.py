import os
import subprocess
import xarray as xr
import matplotlib.pyplot as plt
from herbie import Herbie

# Manually add user path to PATH for this script's session
user_profile_path = r"C:\Code\Cygwin\bin"  # Backslashes for Windows paths
os.environ['PATH'] = user_profile_path + ";" + os.environ['PATH']

# Define your command with backslashes for Windows
command = [
    r"C:\Code\wgrib2\grib2\wgrib2\wgrib2.exe",  # Use raw strings (r'') to preserve backslashes
    r"C:\Other\GRIB\Test\hrrr\20211231\subset_dbefcf9d__hrrr.t17z.wrfnatf00.grib2",
    "-small_grib",
    "-70:-50",  # Longitude range
    "30:40",    # Latitude range
    r"C:\Other\GRIB\Test\hrrr\20211231\new_subset.grib2"
]

# Run the command using subprocess
try:
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Command executed successfully")
    print(result.stdout.decode())  # Print the standard output
except subprocess.CalledProcessError as e:
    print("Error executing command")
    print(e.stderr.decode())  # Print the error output

# Load the subset data into xarray
grib_file_path = r"C:\Other\GRIB\Test\hrrr\20211231\new_subset.grib2"
# Initialize Herbie with the local file
date = "20211231"


grib_file_path = r"C:\Other\GRIB\Test\hrrr\20211231\new_subset.grib2"


import os
import subprocess


# While this function seems simple, it is very difficult to get
# wgrib2 to work on Windows operating system.
def process_grib_file(wgrib2_path, input_grib, output_grib, lon_range,
                      lat_range, cygwin_path=None):
    """
    Processes a GRIB2 file using wgrib2 by extracting a subset based on
    longitude and latitude range.

    Parameters:
    - wgrib2_path (str): Path to the wgrib2 executable.
    - input_grib (str): Path to the input GRIB2 file.
    - output_grib (str): Path to the output subset GRIB2 file.
    - lon_range (tuple): Longitude range as (min_lon, max_lon).
    - lat_range (tuple): Latitude range as (min_lat, max_lat).
    - cygwin_path (str, optional): Path to Cygwin's
    bin directory (for Windows).

    Returns:
    - str: Standard output from the command execution or an error message.
    """

    # Optionally add Cygwin path to PATH
    if cygwin_path:
        os.environ['PATH'] = cygwin_path + ";" + os.environ['PATH']

    # Construct command
    command = [
        wgrib2_path,
        input_grib,
        "-small_grib",
        f"{lon_range[0]}:{lon_range[1]}",  # Longitude range
        f"{lat_range[0]}:{lat_range[1]}",  # Latitude range
        output_grib
    ]

    # Run command using subprocess
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        return result.stdout.decode()  # Return the standard output
    except subprocess.CalledProcessError as e:
        # Return error message
        return f"Error executing command:\n{e.stderr.decode()}"

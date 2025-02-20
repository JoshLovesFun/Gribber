import os
import subprocess
import pygrib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def process_grib_file(wgrib2_path, input_grib, output_grib, lon_range,
                      lat_range, cygwin_path=None):
    """
    Processes a GRIB2 file using wgrib2 by extracting a subset based on longitude and latitude range.

    Parameters:
    - wgrib2_path (str): Path to the wgrib2 executable.
    - input_grib (str): Path to the input GRIB2 file.
    - output_grib (str): Path to the output subset GRIB2 file.
    - lon_range (tuple): Longitude range as (min_lon, max_lon).
    - lat_range (tuple): Latitude range as (min_lat, max_lat).
    - cygwin_path (str, optional): Path to Cygwin's bin directory (for Windows).

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
        return f"Error executing command:\n{e.stderr.decode()}"  # Return error message


# Automatically run when this script is executed
wgrib2_path = r"C:\Code\wgrib2\grib2\wgrib2\wgrib2.exe"
input_grib = r"C:\Other\GRIB\Test\hrrr\20211231\subset_dbefcf9d__hrrr.t17z.wrfnatf00.grib2"
output_grib = r"C:\Other\GRIB\Test\hrrr\20211231\new_subset.grib2"
lon_range = (-79, -67)
lat_range = (37, 47)
cygwin_path = r"C:\Code\Cygwin\bin"

result = process_grib_file(wgrib2_path, input_grib, output_grib, lon_range,
                           lat_range, cygwin_path)
print(result)

# *****************************************************************************

def plot_grib_temperature(grib_file, variable_name='Temperature', level=1):
    """
    Opens a GRIB file, extracts temperature data at a specified level, and plots it on a map.

    Parameters:
    - grib_file (str): Path to the GRIB file.
    - variable_name (str): Name of the variable to extract (default is 'Temperature').
    - level (int): Level to extract data from (default is 1).

    Returns:
    - None (displays a plot).
    """

    # Open the GRIB file
    grbs = pygrib.open(grib_file)

    # Print the list of variables and their levels
    print("Variables and Levels in the GRIB file:")
    for grb in grbs:
        print(f"{grb.name}: Level {grb.level} (Type: {grb.typeOfLevel})")

    # Select the specified variable at the given level
    try:
        grb = grbs.select(name=variable_name, level=level)[0]
    except IndexError:
        print(
            f"Error: {variable_name} at level {level} not found in the GRIB file.")
        grbs.close()
        return

    # Extract the data and coordinates
    data = grb.values
    lats, lons = grb.latlons()

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6),
                           subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([-130, -60, 20, 60],
                  crs=ccrs.PlateCarree())  # Set the map extent for USA, Canada, Mexico

    # Add map features
    ax.add_feature(cfeature.COASTLINE, linewidth=1)
    ax.add_feature(cfeature.BORDERS, linewidth=1)
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.LAKES, edgecolor='black')
    ax.add_feature(cfeature.STATES, edgecolor='gray')

    # Plot the temperature data
    contour = ax.contourf(lons, lats, data, cmap='coolwarm',
                          transform=ccrs.PlateCarree())
    plt.colorbar(contour, ax=ax, label="Temperature (K)")

    # Add title and labels
    plt.title(f"{variable_name} at Level {level}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Show the plot
    plt.show()

    # Close the GRIB file
    grbs.close()


# Example usage
grib_file = r"C:\Other\GRIB\Test\hrrr\20211231\new_subset.grib2"
plot_grib_temperature(grib_file)


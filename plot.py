import pygrib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature



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
    # Select the specified variable at the given level
    try:
        grb = grbs.select(name=variable_name, level=level)[0]
    except (ValueError, IndexError):  # Catch ValueError instead
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






import os
import subprocess
import pygrib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


# Manually add user path to PATH for this script's session
user_profile_path = r"C:\Code\Cygwin\bin"  # Backslashes for Windows paths
os.environ['PATH'] = user_profile_path + ";" + os.environ['PATH']

# Define your command with backslashes for Windows
command = [
    r"C:\Code\wgrib2\grib2\wgrib2\wgrib2.exe",
    r"C:\Other\GRIB\Test\hrrr\20211231\subset_dbef9b96__hrrr.t17z.wrfnatf00.grib2",
    "-small_grib",
    "-79:-67",  # Longitude range
    "37:47",    # Latitude range
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

# *****************************************************************************

#grib_file = r"C:\Other\GRIB\Test\hrrr\20211231\subset_dbef9b96__hrrr.t17z.wrfnatf00.grib2"
grib_file = r"C:\Other\GRIB\Test\hrrr\20211231\new_subset.grib2"

# Open the GRIB file
grbs = pygrib.open(grib_file)

# Print the list of variables and their levels
print("Variables and Levels in the GRIB file:")
for grb in grbs:
    print(f"{grb.name}: Level {grb.level} (Type: {grb.typeOfLevel})")

# Select the temperature at level 1 (adjust the name as needed)
grb = grbs.select(name='Temperature')[0]

# Extract the data and coordinates
data = grb.values
lats, lons = grb.latlons()

# Plotting the temperature with a basemap
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([-130, -60, 20, 60], crs=ccrs.PlateCarree())  # Set the map extent for USA, Canada, Mexico

# Add features like coastlines and state borders
ax.add_feature(cfeature.COASTLINE, linewidth=1)
ax.add_feature(cfeature.BORDERS, linewidth=1)
ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.LAKES, edgecolor='black')

# Add state boundaries (USA states)
ax.add_feature(cfeature.STATES, edgecolor='gray')

# Plot the data
contour = ax.contourf(lons, lats, data, cmap='coolwarm', transform=ccrs.PlateCarree())
plt.colorbar(contour, ax=ax, label="Temperature (K)")

# Title and labels
plt.title("Temperature at Level 1")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# Show the plot
plt.show()

# Close the GRIB file
grbs.close()

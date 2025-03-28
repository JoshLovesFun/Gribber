# All constants used are defined here.

default_control_filename = "Control.txt"
coordinates_filename = "GRIB_Nearest_Coordinates_Used.txt"
KELVIN_TO_CELSIUS_OFFSET = 273.15
MISSING_VALUE = -9999.999
DEGREES_IN_A_CIRCLE = 360.0
HALF_CIRCLE_IN_DEGREES = 180.0
BASE_DIRECTION = 270.0
MINIMUM_SPECIFIC_HUMIDITY = 0.000001
Mw_over_Md = 0.622  # The ratio of the molecular weight of water vapor
One_Minus_Mw_over_Md = 0.378  # One minus the ratio of the molecular
# weight of water vapor to the molecular weight of dry air.

# Related to relative humidity and dew point calculations:
ScaleFactor = 6.1094  # No units but serves to adjust the formula's
# output to match the desired units (hectopascals in this case).
ScaleTempFactor1 = 17.625  # No units but used to account for the
# temperature dependence of the saturation vapor pressure.
ScaleTempFactor2 = 243.04  # No units but used to account for the
# temperature dependence of the saturation vapor pressure.

MAX_LVL = 12

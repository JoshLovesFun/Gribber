import math



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
        # v before u but the opposite in Excel???
        math_wind_direction_rad = math.atan2(v, u)

        met_wind_dir = round(
            (270 - (math_wind_direction_rad * 180.0 / math.pi)) % 360, 3)
        # In Excel: =MOD((270-($Q2)*(180/PI())),360)

        return wind_speed, met_wind_dir
    else:
        return -9999.999, -9999.999


def calculate_relative_humidity(q, t, p):
    # This if statement is used to prevent an error when specific
    # humidity is requested for a particular level, but either the temperature
    # or pressure at that level was not requested.
    if ((q is None or q == -9999.999)
            or (t is None or t == -9999.999)
            or (p is None or p == -9999.999)):
        return -9999.999

    if (q == 0.0):  # Rare. Do this to avoid error for dew point calculation.
        return 0.000001

    if (isinstance(q, float) and
            isinstance(t, float) and
            isinstance(p, float)):

        # We need specific humidity, temperature, and pressure
        # at the level of interest.
        # Input arguments:
        # q: Specific Humidity [kg/kg]
        # t: Temperature [K]
        # p: Pressure [Pa]

        # Info: https://earthscience.stackexchange.com/questions/2360/
        # how-do-i-convert-specific-humidity-to-relative-humidity
        # Info: https://en.wikipedia.org/wiki/
        # Clausius%E2%80%93Clapeyron_relation
        # Info: https://cran.r-project.org/web/packages/humidity/
        # vignettes/humidity-measures.html

        # First calculate e (vapor pressure)
        # Then calculate e_sub_s (saturation vapor pressure)

        Mw_over_Md = 0.622  # The ratio of the molecular weight of water vapor
        # to the molecular weight of dry air.
        One_Minus_Mw_over_Md = 0.378  # One minus the ratio of the molecular
        # weight of water vapor to the molecular weight of dry air.

        # Equation 6: https://cran.r-project.org/web/packages/humidity/
        # vignettes/humidity-measures.html
        e = (q * p) / (Mw_over_Md + (One_Minus_Mw_over_Md * q))  # Result in Pa

        # August–Roche–Magnus formula: We can use this to calculate
        # saturation vapor pressure.
        # https://en.wikipedia.org/wiki/Clausius%E2%80%93Clapeyron_relation
        # Input temperature for this formula is in Celsius.

        t_C = t - 273.15

        ScaleFactor = 6.1094  # No units but serves to adjust the formula's
        # output to match the desired units (hectopascals in this case).
        ScaleTempFactor1 = 17.625  # No units but used to account for the
        # temperature dependence of the saturation vapor pressure.
        ScaleTempFactor2 = 243.04  # No units but used to account for the
        # temperature dependence of the saturation vapor pressure.

        e_sub_s = ScaleFactor * math.exp((
            ScaleTempFactor1 * t_C)/(t_C + ScaleTempFactor2))  # Result in hPa

        e_sub_s_Pa = e_sub_s * 100.0  # Convert to Pa

        # Finally, to get RH:
        RH = (e / e_sub_s_Pa) * 100.0  # Pa/Pa * 100%
        RH_cap = RH

        if RH > 100.0:  # This should be rare. It shouldn't be
            # that much over 100%.
            RH_cap = 100.0

        # https://www.processsensing.com/en-us/humidity-calculator/rotronic/
        # The above link can be used to check results. Results should be close,
        # but we can't expect them to be identical!
        return RH_cap
    else:
        return -9999.999


def calculate_dew_point(t, RH_cap):
    # This if statement is used to prevent an error when specific humidity
    # is requested for a particular level, but either the temperature or
    # pressure at that level was not requested.
    if ((t is None or t == -9999.999) or
            (RH_cap is None or RH_cap == -9999.999)):
        return -9999.999

    if isinstance(t, float) and isinstance(RH_cap, float):

        # Formula: https://bmcnoldy.earth.miami.edu/Humidity.html

        # Input temperature is in Kelvin.
        # We want the output temperature to be in Celsius. So:
        t_C = t - 273.15

        numerator = 243.04 * (math.log(RH_cap/100.0) +
                              ((17.625 * t_C) / (243.04 + t_C)))
        denominator = (17.625 - math.log(RH_cap/100.0) -
                       ((17.625 * t_C) / (243.04 + t_C)))
        Dew_Point = round((numerator / denominator), 3)

        # Verify the results:
        # https://bmcnoldy.earth.miami.edu/Humidity.html
        # https://www.calculator.net/dew-point-calculator.html
        return Dew_Point
    else:
        return -9999.999
import math

import constants


def convert_longitude(nearest_lon):
    if nearest_lon == -999:
        return nearest_lon
    else:
        return nearest_lon - 360.0


def kelvin_to_celsius(kelvin):
    if isinstance(kelvin, float):
        celsius = kelvin - constants.KELVIN_TO_CELSIUS_OFFSET
        rounded_celsius = round(celsius, 3)
        return rounded_celsius
    else:
        return constants.MISSING_VALUE


def calculate_wind_speed_and_direction(u, v):
    if isinstance(u, float) and isinstance(v, float):

        # Calculate the wind speed
        wind_speed = round(math.sqrt(u**2 + v**2), 3)

        # Calculate the math wind direction
        # v before u but the opposite in Excel???
        math_wind_direction_rad = math.atan2(v, u)

        met_wind_dir = round(
            (constants.BASE_DIRECTION - (
                    math_wind_direction_rad *
                    constants.HALF_CIRCLE_IN_DEGREES / math.pi)) %
            constants.DEGREES_IN_A_CIRCLE, 3)
        # In Excel: =MOD((270-($Q2)*(180/PI())),360)

        return wind_speed, met_wind_dir
    else:
        return constants.MISSING_VALUE, constants.MISSING_VALUE


def calculate_relative_humidity(q, t, p):
    # This if statement is used to prevent an error when specific
    # humidity is requested for a particular level, but either the temperature
    # or pressure at that level was not requested.
    if ((q is None or q == constants.MISSING_VALUE)
            or (t is None or t == constants.MISSING_VALUE)
            or (p is None or p == constants.MISSING_VALUE)):
        return constants.MISSING_VALUE

    if q == 0.0:  # Rare. Do this to avoid error for dew point calculation.
        return constants.MINIMUM_SPECIFIC_HUMIDITY

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

        # Equation 6: https://cran.r-project.org/web/packages/humidity/
        # vignettes/humidity-measures.html
        # Result in Pa
        e = (q * p) / (constants.Mw_over_Md +
                       (constants.One_Minus_Mw_over_Md * q))

        # August–Roche–Magnus formula: We can use this to calculate
        # saturation vapor pressure.
        # https://en.wikipedia.org/wiki/Clausius%E2%80%93Clapeyron_relation
        # Input temperature for this formula is in Celsius.

        t_cel = t - constants.KELVIN_TO_CELSIUS_OFFSET

        e_sub_s = constants.ScaleFactor * math.exp((
            constants.ScaleTempFactor1 * t_cel)/(
                t_cel + constants.ScaleTempFactor2))  # Result in hPa

        e_sub_s_pa = e_sub_s * 100.0  # Convert to Pa

        # Finally, to get RH:
        rh = (e / e_sub_s_pa) * 100.0  # Pa/Pa * 100%
        rh_cap = rh

        if rh > 100.0:  # This should be rare. It shouldn't be
            # that much over 100%.
            rh_cap = 100.0

        # https://www.processsensing.com/en-us/humidity-calculator/rotronic/
        # The above link can be used to check results. Results should be close,
        # but we can't expect them to be identical!
        return rh_cap
    else:
        return constants.MISSING_VALUE


def calculate_dew_point(t, rh_cap):
    # This if statement is used to prevent an error when specific humidity
    # is requested for a particular level, but either the temperature or
    # pressure at that level was not requested.
    if ((t is None or t == constants.MISSING_VALUE) or
            (rh_cap is None or rh_cap == constants.MISSING_VALUE)):
        return constants.MISSING_VALUE

    if isinstance(t, float) and isinstance(rh_cap, float):

        # Formula: https://bmcnoldy.earth.miami.edu/Humidity.html

        # Input temperature is in Kelvin.
        # We want the output temperature to be in Celsius. So:
        t_cel = t - constants.KELVIN_TO_CELSIUS_OFFSET

        numerator = (constants.ScaleTempFactor2 *
                     (math.log(rh_cap / 100.0) +
                      ((constants.ScaleTempFactor1 * t_cel) / (
                              constants.ScaleTempFactor2 + t_cel))))
        denominator = (constants.ScaleTempFactor1 -
                       math.log(rh_cap / 100.0) -
                       ((constants.ScaleTempFactor1 * t_cel) / (
                               constants.ScaleTempFactor2 + t_cel)))
        dew_point = round((numerator / denominator), 3)

        # Verify the results:
        # https://bmcnoldy.earth.miami.edu/Humidity.html
        # https://www.calculator.net/dew-point-calculator.html
        return dew_point
    else:
        return constants.MISSING_VALUE

# This file lists all the GRIB codes we may want.
# Also try to store the codes in a dictionary.

# Note: The surface files are a subset of the pressure files,
# so we only need to retrieve the pressure files.
# GRIB codes obtained from the pressure file will hereafter be called
# "Surface" or "SFC" since the only thing we will take from the pressure
# file will be either surface parameters or parameters associated with
# the surface layer.

# List of codes:

# HRRR - Surface:
# par1
# par2
# par3
# par4

# HRRR - Native:
# par1
# par2
# par3

# Example (not finished)
def create_grib_code_dict():
    levels = list(range(1, 51))
    temp_grib_codes = [f":TMP:{level}" for level in levels]
    uv_grib_codes = [f":[U|V]GRD:{level}" for level in levels]

    grib_dict = {
        "SFC": {
            "skin_temp": ":TMP:1013.2 mb",
            "ground": ":SOILW:0.01-0.01",
            "soil": ":TSOIL:1",
            "snow": ":SNOWH:0",
        },
        "NAT": {
            "UV": {
                "levels": levels,
                "grib_codes": uv_grib_codes
            },
            "Temp": {
                "levels": levels,
                "grib_codes": temp_grib_codes
            }
        }
    }

    return grib_dict


grib_dict_call = create_grib_code_dict()

print(grib_dict_call["NAT"]["UV"]["grib_codes"][49])
print(grib_dict_call["SFC"]["ground"])

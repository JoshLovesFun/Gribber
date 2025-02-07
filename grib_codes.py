# This file lists all the GRIB codes we may want.
# Also try to store the codes in a dictionary.

# Note: The surface files are a subset of the pressure files,
# so we only need to retrieve the pressure files.
# GRIB codes obtained from the pressure file will hereafter be called
# "Surface" or "SFC" since the only thing we will take from the pressure
# file will be either surface parameters or parameters associated with
# the surface/near surface layer.

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
    hgt_grib_codes = [f":HGT:{level} hybrid level" for level in levels]
    pres_grib_codes = [f":PRES:{level} hybrid level" for level in levels]
    temp_grib_codes = [f":TMP:{level} hybrid level" for level in levels]

    grib_dict = {
        "SFC": {
            "2m_temp": ":TMP:2 m above ground",
            "2m_spfh": ":SPFH:2 m above ground",
            "2m_rh": ":RH:2 m above ground",
            "10m_u_and_v": ":[U|V]GRD:10 m above ground",
        },
        "NAT": {
            "hgt": {
                "levels": levels,
                "grib_codes": hgt_grib_codes,
            },
            "pres": {
                "levels": levels,
                "grib_codes": pres_grib_codes,
            },
            "temp": {
                "levels": levels,
                "grib_codes": temp_grib_codes,
            },
        }
    }

    return grib_dict


grib_dict_call = create_grib_code_dict()

print(grib_dict_call["SFC"]["2m_temp"])
print(grib_dict_call["SFC"]["2m_rh"])
print(grib_dict_call["NAT"]["hgt"]["grib_codes"][49])
print(grib_dict_call["NAT"]["pres"]["grib_codes"][49])
print(grib_dict_call["NAT"]["temp"]["grib_codes"][49])

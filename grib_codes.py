# This file stores all the GRIB codes we may want.

# Note: The HRRR GRIB surface files are a subset of the pressure files,
# so we only need to retrieve the pressure files.
# GRIB codes obtained from the pressure files will hereafter be called
# "Surface" or "SFC" since the only thing we will take from the pressure
# files will be either surface parameters or parameters associated with
# the surface/near surface layer.


def create_grib_code_dict():
    levels = list(range(1, 51))
    hybrid = " hybrid"
    hgt_grib_codes = [f":HGT:{level}{hybrid}" for level in levels]
    pres_grib_codes = [f":PRES:{level}{hybrid}" for level in levels]
    temp_grib_codes = [f":TMP:{level}{hybrid}" for level in levels]
    spfh_grib_codes = [f":SPFH:{level}{hybrid}" for level in levels]
    u_v_grib_codes = [f":[U|V]GRD:{level}{hybrid}" for level in levels]
    clwmr_grib_codes = [f":CLWMR:{level}{hybrid}" for level in levels]
    rwmr_grib_codes = [f":RWMR:{level}{hybrid}" for level in levels]
    cimixr_grib_codes = [f":CIMIXR:{level}{hybrid}" for level in levels]
    snmr_grib_codes = [f":SNMR:{level}{hybrid}" for level in levels]
    grle_grib_codes = [f":GRLE:{level}{hybrid}" for level in levels]
    tke_grib_codes = [f":TKE:{level}{hybrid}" for level in levels]

    grib_dict = {
        "SFC": {
            "2m_temp": ":TMP:2 m above ground",
            "2m_spfh": ":SPFH:2 m above ground",
            "2m_rh": ":RH:2 m above ground",
            "10m_u_and_v": ":[U|V]GRD:10 m above ground",
            "sfc_pres": ":PRES:surface",
            "mslp": ":MSLMA:mean sea level",
            "water_equiv_sd": ":WEASD:surface",
            "snow_depth": ":SNOD:surface",
            "skin_temp": ":TMP:surface",
            "plant": ":CNWAT:surface",
            "soil_moist_0": ":SOILW:0-0 m below ground",
            "soil_moist_1": ":SOILW:0.01-0.01 m below ground",
            "soil_moist_2": ":SOILW:0.04-0.04 m below ground",
            "soil_moist_3": ":SOILW:0.1-0.1 m below ground",
            "soil_moist_4": ":SOILW:0.3-0.3 m below ground",
            "soil_moist_5": ":SOILW:0.6-0.6 m below ground",
            "soil_moist_6": ":SOILW:1-1 m below ground",
            "soil_moist_7": ":SOILW:1.6-1.6 m below ground",
            "soil_moist_8": ":SOILW:3-3 m below ground",
            "soil_temp_0": ":TSOIL:0-0 m below ground",
            "soil_temp_1": ":TSOIL:0.01-0.01 m below ground",
            "soil_temp_2": ":TSOIL:0.04-0.04 m below ground",
            "soil_temp_3": ":TSOIL:0.1-0.1 m below ground",
            "soil_temp_4": ":TSOIL:0.3-0.3 m below ground",
            "soil_temp_5": ":TSOIL:0.6-0.6 m below ground",
            "soil_temp_6": ":TSOIL:1-1 m below ground",
            "soil_temp_7": ":TSOIL:1.6-1.6 m below ground",
            "soil_temp_8": ":TSOIL:3-3 m below ground",
            "ice_flag": ":ICEC:surface",
            "land_sea_flag": ":LAND:surface",
            "soil_height": ":HGT:surface",
            "bound_lyr_hgt": ":HPBL:surface",
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
            "spfh": {
                "levels": levels,
                "grib_codes": spfh_grib_codes,
            },
            "u_v": {
                "levels": levels,
                "grib_codes": u_v_grib_codes,
            },
            "clwmr": {
                "levels": levels,
                "grib_codes": clwmr_grib_codes,
            },
            "rwmr": {
                "levels": levels,
                "grib_codes": rwmr_grib_codes,
            },
            "cimixr": {
                "levels": levels,
                "grib_codes": cimixr_grib_codes,
            },
            "snmr": {
                "levels": levels,
                "grib_codes": snmr_grib_codes,
            },
            "grle": {
                "levels": levels,
                "grib_codes": grle_grib_codes,
            },
            "tke": {
                "levels": levels,
                "grib_codes": tke_grib_codes,
            },
        }
    }

    return grib_dict

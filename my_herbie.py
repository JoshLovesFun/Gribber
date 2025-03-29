# Goal: Download GRIB files into working directory using Herbie.

from herbie import Herbie

from file_and_time_control import get_date_range, generate_datetime_range
# TODO We should think about using FastHerbie in the future.
from grib_codes import create_grib_code_dict


def fetch_herbie_data(date_str, processed_data):
    str_u_and_v = str_tmp = str_tke = str_pres = str_spfh = "no"

    if processed_data.get('U_and_V_WindComponent') == "yes":
        str_u_and_v = "yes"

    if processed_data.get('Temperature') == "yes":
        str_tmp = "yes"

    if processed_data.get('TKE') == "yes":
        str_tke = "yes"

    if processed_data.get('PRES') == "yes":
        str_pres = "yes"

    if processed_data.get('SPFH') == "yes":
        str_spfh = "yes"

    # For WRF prs
    _2m_temp, _2m_spfh, _2m_rh = None, None, None
    _10m_u_and_v = None
    sfc_pres, mslp, water_equiv_sd, snow_depth = None, None, None, None
    skin_temp, plant = None, None

    soil_moist_0, soil_moist_1, soil_moist_2 = None, None, None
    soil_moist_3, soil_moist_4, soil_moist_5 = None, None, None
    soil_moist_6, soil_moist_7, soil_moist_8 = None, None, None

    soil_temp_0, soil_temp_1, soil_temp_2 = None, None, None
    soil_temp_3, soil_temp_4, soil_temp_5 = None, None, None
    soil_temp_6, soil_temp_7, soil_temp_8 = None, None, None

    ice_flag, land_sea_flag, soil_height = None, None, None
    # End WRF prs

    # For WRF nat
    hgt, clmr, rwmr, cimixr, snmr, grle = {}, {}, {}, {}, {}, {}
    # End WRF nat

    lblh = None

    lpreshgt, lthgt, lspfhhgt, lwhgt, ltkehgt, = {}, {}, {}, {}, {}

    grib_dict = create_grib_code_dict()

    if processed_data.get('wrf') == "yes":
        _2m_temp = grib_dict["SFC"]["2m_temp"]
        _2m_spfh = grib_dict["SFC"]["2m_spfh"]
        _2m_rh = grib_dict["SFC"]["2m_rh"]
        _10m_u_and_v = grib_dict["SFC"]["10m_u_and_v"]
        sfc_pres = grib_dict["SFC"]["sfc_pres"]
        mslp = grib_dict["SFC"]["mslp"]
        water_equiv_sd = grib_dict["SFC"]["water_equiv_sd"]
        snow_depth = grib_dict["SFC"]["snow_depth"]
        skin_temp = grib_dict["SFC"]["skin_temp"]
        plant = grib_dict["SFC"]["plant"]

        soil_moist_0 = grib_dict["SFC"]["soil_moist_0"]
        soil_moist_1 = grib_dict["SFC"]["soil_moist_1"]
        soil_moist_2 = grib_dict["SFC"]["soil_moist_2"]
        soil_moist_3 = grib_dict["SFC"]["soil_moist_3"]
        soil_moist_4 = grib_dict["SFC"]["soil_moist_4"]
        soil_moist_5 = grib_dict["SFC"]["soil_moist_5"]
        soil_moist_6 = grib_dict["SFC"]["soil_moist_6"]
        soil_moist_7 = grib_dict["SFC"]["soil_moist_7"]
        soil_moist_8 = grib_dict["SFC"]["soil_moist_8"]

        soil_temp_0 = grib_dict["SFC"]["soil_temp_0"]
        soil_temp_1 = grib_dict["SFC"]["soil_temp_1"]
        soil_temp_2 = grib_dict["SFC"]["soil_temp_2"]
        soil_temp_3 = grib_dict["SFC"]["soil_temp_3"]
        soil_temp_4 = grib_dict["SFC"]["soil_temp_4"]
        soil_temp_5 = grib_dict["SFC"]["soil_temp_5"]
        soil_temp_6 = grib_dict["SFC"]["soil_temp_6"]
        soil_temp_7 = grib_dict["SFC"]["soil_temp_7"]
        soil_temp_8 = grib_dict["SFC"]["soil_temp_8"]

        ice_flag = grib_dict["SFC"]["ice_flag"]
        land_sea_flag = grib_dict["SFC"]["land_sea_flag"]
        soil_height = grib_dict["SFC"]["soil_height"]

    if processed_data.get('wrf') == "yes":
        for level in range(1, 4):
            hgt[f'hgt{level}'] = (
                grib_dict["NAT"]["hgt"]["grib_codes"][level - 1])
            lpreshgt[f'LPRESHGT{level}'] = (
                grib_dict["NAT"]["pres"]["grib_codes"][level - 1])
            lthgt[f'LTHGT{level}'] = (
                grib_dict["NAT"]["temp"]["grib_codes"][level - 1])
            lspfhhgt[f'LSPFHHGT{level}'] = (
                grib_dict["NAT"]["spfh"]["grib_codes"][level - 1])
            lwhgt[f'LWHGT{level}'] = (
                grib_dict["NAT"]["u_v"]["grib_codes"][level - 1])
            clmr[f'clmr{level}'] = (
                grib_dict["NAT"]["clmr"]["grib_codes"][level - 1])
            rwmr[f'rwmr{level}'] = (
                grib_dict["NAT"]["rwmr"]["grib_codes"][level - 1])
            cimixr[f'cimixr{level}'] = (
                grib_dict["NAT"]["cimixr"]["grib_codes"][level - 1])
            snmr[f'snmr{level}'] = (
                grib_dict["NAT"]["snmr"]["grib_codes"][level - 1])
            grle[f'grle{level}'] = (
                grib_dict["NAT"]["grle"]["grib_codes"][level - 1])

    if processed_data.get('BoundaryLayerHeight') == "yes":
        lblh = grib_dict["SFC"]["bound_lyr_hgt"]

    if str_pres == "yes" and processed_data.get('wrf') != "yes":
        for level in range(1, 13):
            if processed_data.get(f'PRESHeightLevel{level}') == "yes":
                lpreshgt[f'LPRESHGT{level}'] = (
                    grib_dict["NAT"]["pres"]["grib_codes"][level - 1])

    if str_tmp == "yes" and processed_data.get('wrf') != "yes":
        for level in range(1, 13):
            if processed_data.get(f'TemperatureHeightLevel{level}') == "yes":
                lthgt[f'LTHGT{level}'] = (
                    grib_dict["NAT"]["temp"]["grib_codes"][level - 1])

    if str_spfh == "yes" and processed_data.get('wrf') != "yes":
        for level in range(1, 13):
            if processed_data.get(f'SPFHHeightLevel{level}') == "yes":
                lspfhhgt[f'LSPFHHGT{level}'] = (
                    grib_dict["NAT"]["spfh"]["grib_codes"][level - 1])

    if str_u_and_v == "yes" and processed_data.get('wrf') != "yes":
        for level in range(1, 13):
            if processed_data.get(f'WindHeightLevel{level}') == "yes":
                lwhgt[f'LWHGT{level}'] = (
                    grib_dict["NAT"]["u_v"]["grib_codes"][level - 1])

    if str_tke == "yes":
        for level in range(1, 13):
            if processed_data.get(f'TKEHeightLevel{level}') == "yes":
                ltkehgt[f'LTKEHGT{level}'] = (
                    grib_dict["NAT"]["tke"]["grib_codes"][level - 1])

    search_patterns = [
        lblh, _2m_temp, _2m_spfh, _2m_rh, _10m_u_and_v, sfc_pres, mslp,
        water_equiv_sd, snow_depth, skin_temp, plant,

        soil_moist_0, soil_moist_1, soil_moist_2, soil_moist_3,  soil_moist_4,
        soil_moist_5, soil_moist_6, soil_moist_7, soil_moist_8,

        soil_temp_0, soil_temp_1, soil_temp_2, soil_temp_3, soil_temp_4,
        soil_temp_5, soil_temp_6, soil_temp_7, soil_temp_8,

        ice_flag, land_sea_flag, soil_height,

        *[hgt[f'hgt{level}'] for level in range(1, 21) if
          f'hgt{level}' in hgt],

        *[lthgt[f'LTHGT{level}'] for level in range(1, 21) if
          f'LTHGT{level}' in lthgt],

        *[lwhgt[f'LWHGT{level}'] for level in range(1, 13) if
          f'LWHGT{level}' in lwhgt],

        *[lpreshgt[f'LPRESHGT{level}'] for level in range(1, 21) if
          f'LPRESHGT{level}' in lpreshgt],

        *[lspfhhgt[f'LSPFHHGT{level}'] for level in range(1, 13) if
          f'LSPFHHGT{level}' in lspfhhgt],

        *[ltkehgt[f'LTKEHGT{level}'] for level in range(1, 13) if
          f'LTKEHGT{level}' in ltkehgt],

        *[clmr[f'clmr{level}'] for level in range(1, 21) if
          f'clmr{level}' in clmr],

        *[rwmr[f'rwmr{level}'] for level in range(1, 21) if
          f'rwmr{level}' in rwmr],

        *[cimixr[f'cimixr{level}'] for level in range(1, 21) if
          f'cimixr{level}' in cimixr],

        *[snmr[f'snmr{level}'] for level in range(1, 21) if
          f'snmr{level}' in snmr],

        *[grle[f'grle{level}'] for level in range(1, 21) if
          f'grle{level}' in grle],
    ]

    # Note there is an important file here:
    # /home/joshua/.config/herbie/config.toml
    # It has the following contents (as an example):

    # [default]
    # model = "hrrr"
    # fxx = 0
    # save_dir = "/home/joshua/CODE/HerbieOut"
    # overwrite = false
    # verbose = true

    hybrid_patterns = []
    prs_patterns = []
    h_nat = None
    search_string_hybrid = None

    # Loop through each search pattern
    for pattern in search_patterns:
        # Skip None values
        if pattern is None:
            continue

        # Check if the pattern contains 'hybrid' for h_nat
        if 'hybrid' in pattern:
            hybrid_patterns.append(
                pattern)  # Add hybrid variables

        # Check if the pattern contains anything else (for use in h_prs)
        else:
            prs_patterns.append(pattern)

    # Now, download all hybrid patterns using h_nat, if there are any.
    # The goal is to put the hybrid level variables in the nat files.
    if hybrid_patterns:
        h_nat = Herbie(date_str, product="nat", priority="aws")
        search_string_hybrid = '|'.join(hybrid_patterns)
        h_nat.download(search_string_hybrid, verbose=True)

    # Now, download all other (surface) patterns using h_prs, if there are any.
    # The goal is to put the surface level variables in the prs files.
    if prs_patterns:
        h_prs = Herbie(date_str, product="prs", priority="aws")
        search_string_prs = '|'.join(prs_patterns)
        h_prs.download(search_string_prs, verbose=True)

    # if h_nat is not None:
        # invent = h_nat.inventory(searchString=search_string_hybrid)
        # print(invent)  # Trust me bro :) I got your inventory ;)


def fetch_herbie_data_in_range(processed_data):
    """Fetches Herbie data for each generated date-time."""
    start_date, end_date = get_date_range(processed_data)
    if start_date is None or end_date is None:
        return  # Stop execution if dates are invalid

    datetime_list = generate_datetime_range(start_date, end_date)

    for date_str in datetime_list:
        try:
            fetch_herbie_data(date_str, processed_data)
        except Exception as e:
            print(f"Error fetching Herbie data for {date_str}: {e}")

    print("\n\n")  # Maintain output formatting

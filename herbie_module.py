# Goal: Download GRIB files into working directory using Herbie.

from datetime import datetime, timedelta
from herbie import Herbie
# We should think about using FastHerbie in the future.
from grib_codes import create_grib_code_dict


def fetch_herbie_data(date_str, processed_data):
    strUandV = strTMP = strTKE = strPRES = strSPFH = "no"

    if processed_data.get('U_and_V_WindComponent') == "yes":
        strUandV = "yes"

    if processed_data.get('Temperature') == "yes":
        strTMP = "yes"

    if processed_data.get('TKE') == "yes":
        strTKE = "yes"

    if processed_data.get('PRES') == "yes":
        strPRES = "yes"

    if processed_data.get('SPFH') == "yes":
        strSPFH = "yes"

    LBLH = None

    LPRESHGT, LTHGT, LSPFHHGT, LWHGT, LTKEHGT, = {}, {}, {}, {}, {}

    grib_dict = create_grib_code_dict()



    if processed_data.get('BoundaryLayerHeight') == "yes":
        LBLH = grib_dict["SFC"]["bound_lyr_hgt"]



    if strPRES == "yes":
        for level in range(1, 13):
            if processed_data.get(f'PRESHeightLevel{level}') == "yes":
                LPRESHGT[f'LPRESHGT{level}'] = (
                    grib_dict["NAT"]["pres"]["grib_codes"][level - 1])

    if strTMP == "yes":
        for level in range(1, 13):
            if processed_data.get(f'TemperatureHeightLevel{level}') == "yes":
                LTHGT[f'LTHGT{level}'] = (
                    grib_dict["NAT"]["temp"]["grib_codes"][level - 1])

    if strSPFH == "yes":
        for level in range(1, 13):
            if processed_data.get(f'SPFHHeightLevel{level}') == "yes":
                LSPFHHGT[f'LSPFHHGT{level}'] = (
                    grib_dict["NAT"]["spfh"]["grib_codes"][level - 1])

    if strUandV == "yes":
        for level in range(1, 13):
            if processed_data.get(f'WindHeightLevel{level}') == "yes":
                LWHGT[f'LWHGT{level}'] = (
                    grib_dict["NAT"]["u_v"]["grib_codes"][level - 1])

    if strTKE == "yes":
        for level in range(1, 13):
            if processed_data.get(f'TKEHeightLevel{level}') == "yes":
                LTKEHGT[f'LTKEHGT{level}'] = (
                    grib_dict["NAT"]["tke"]["grib_codes"][level - 1])

    search_patterns = [
        LBLH,

        *[LTHGT[f'LTHGT{level}'] for level in range(1, 13) if
          f'LTHGT{level}' in LTHGT],

        *[LWHGT[f'LWHGT{level}'] for level in range(1, 13) if
          f'LWHGT{level}' in LWHGT],

        *[LPRESHGT[f'LPRESHGT{level}'] for level in range(1, 13) if
          f'LPRESHGT{level}' in LPRESHGT],

        *[LSPFHHGT[f'LSPFHHGT{level}'] for level in range(1, 13) if
          f'LSPFHHGT{level}' in LSPFHHGT],

        *[LTKEHGT[f'LTKEHGT{level}'] for level in range(1, 13) if
          f'LTKEHGT{level}' in LTKEHGT],
    ]



    # Note there is an important file here: /home/joshua/.config/herbie/config.toml
    # It has the following contents (as an example):

    # [default]
    # model = "hrrr"
    # fxx = 0
    # save_dir = "/home/joshua/CODE/HerbieOut"
    # overwrite = false
    # verbose = true

    H = Herbie(
        date_str,
        product="nat",
        priority="aws",
    )

    searchString = '|'.join(pattern for pattern in search_patterns if pattern)

    # invent = H.inventory(searchString=searchString)
    H.download(searchString, verbose=True)
    # print(invent) # Trust me bro :) I got your inventory ;)




def fetch_herbie_data_in_range(processed_data):
    start_date_str = processed_data.get('StartDate', None)
    end_date_str = processed_data.get('EndDate', None)

    if start_date_str is None or end_date_str is None:
        print("Error: StartDate or EndDate not found in processed_data.")
        return

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError as e:
        print(f"Error: Invalid date format - {e}")
        return

    current_date = start_date

    while current_date <= end_date:
        # Loop through hours from 0 to 23
        for hour in range(24):
            date_str = current_date.replace(hour=hour).strftime("%Y-%m-%d %H")
            try:
                fetch_herbie_data(date_str, processed_data)
            except Exception as e:
                print(f"Error fetching Herbie data for {date_str}: {e}")

        # Move to the next day
        current_date += timedelta(days=1)
    print("")
    print("")

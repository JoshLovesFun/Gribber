# Goal: Download GRIB files into working directory using Herbie.

from datetime import datetime, timedelta
from herbie import Herbie
# We should think about using FastHerbie in the future.
from grib_codes import create_grib_code_dict


def fetch_herbie_data(date_str, processed_data):
    BoundaryLayerHeight = processed_data.get('BoundaryLayerHeight')
    U_and_V_WindComponent = processed_data.get('U_and_V_WindComponent')
    Temperature = processed_data.get('Temperature')
    TKE = processed_data.get('TKE')
    PRES = processed_data.get('PRES')
    SPFH = processed_data.get('SPFH')
    WindHeightLevel1 = processed_data.get('WindHeightLevel1')
    WindHeightLevel2 = processed_data.get('WindHeightLevel2')
    WindHeightLevel3 = processed_data.get('WindHeightLevel3')
    WindHeightLevel4 = processed_data.get('WindHeightLevel4')
    WindHeightLevel5 = processed_data.get('WindHeightLevel5')
    WindHeightLevel6 = processed_data.get('WindHeightLevel6')
    WindHeightLevel7 = processed_data.get('WindHeightLevel7')
    WindHeightLevel8 = processed_data.get('WindHeightLevel8')
    WindHeightLevel9 = processed_data.get('WindHeightLevel9')
    WindHeightLevel10 = processed_data.get('WindHeightLevel10')
    WindHeightLevel11 = processed_data.get('WindHeightLevel11')
    WindHeightLevel12 = processed_data.get('WindHeightLevel12')
    TemperatureHeightLevel1 = processed_data.get('TemperatureHeightLevel1')
    TemperatureHeightLevel2 = processed_data.get('TemperatureHeightLevel2')
    TemperatureHeightLevel3 = processed_data.get('TemperatureHeightLevel3')
    TemperatureHeightLevel4 = processed_data.get('TemperatureHeightLevel4')
    TemperatureHeightLevel5 = processed_data.get('TemperatureHeightLevel5')
    TemperatureHeightLevel6 = processed_data.get('TemperatureHeightLevel6')
    TemperatureHeightLevel7 = processed_data.get('TemperatureHeightLevel7')
    TemperatureHeightLevel8 = processed_data.get('TemperatureHeightLevel8')
    TemperatureHeightLevel9 = processed_data.get('TemperatureHeightLevel9')
    TemperatureHeightLevel10 = processed_data.get('TemperatureHeightLevel10')
    TemperatureHeightLevel11 = processed_data.get('TemperatureHeightLevel11')
    TemperatureHeightLevel12 = processed_data.get('TemperatureHeightLevel12')
    TKEHeightLevel1 = processed_data.get('TKEHeightLevel1')
    TKEHeightLevel2 = processed_data.get('TKEHeightLevel2')
    TKEHeightLevel3 = processed_data.get('TKEHeightLevel3')
    TKEHeightLevel4 = processed_data.get('TKEHeightLevel4')
    TKEHeightLevel5 = processed_data.get('TKEHeightLevel5')
    TKEHeightLevel6 = processed_data.get('TKEHeightLevel6')
    TKEHeightLevel7 = processed_data.get('TKEHeightLevel7')
    TKEHeightLevel8 = processed_data.get('TKEHeightLevel8')
    TKEHeightLevel9 = processed_data.get('TKEHeightLevel9')
    TKEHeightLevel10 = processed_data.get('TKEHeightLevel10')
    TKEHeightLevel11 = processed_data.get('TKEHeightLevel11')
    TKEHeightLevel12 = processed_data.get('TKEHeightLevel12')
    PRESHeightLevel1 = processed_data.get('PRESHeightLevel1')
    PRESHeightLevel2 = processed_data.get('PRESHeightLevel2')
    PRESHeightLevel3 = processed_data.get('PRESHeightLevel3')
    PRESHeightLevel4 = processed_data.get('PRESHeightLevel4')
    PRESHeightLevel5 = processed_data.get('PRESHeightLevel5')
    PRESHeightLevel6 = processed_data.get('PRESHeightLevel6')
    PRESHeightLevel7 = processed_data.get('PRESHeightLevel7')
    PRESHeightLevel8 = processed_data.get('PRESHeightLevel8')
    PRESHeightLevel9 = processed_data.get('PRESHeightLevel9')
    PRESHeightLevel10 = processed_data.get('PRESHeightLevel10')
    PRESHeightLevel11 = processed_data.get('PRESHeightLevel11')
    PRESHeightLevel12 = processed_data.get('PRESHeightLevel12')
    SPFHHeightLevel1 = processed_data.get('SPFHHeightLevel1')
    SPFHHeightLevel2 = processed_data.get('SPFHHeightLevel2')
    SPFHHeightLevel3 = processed_data.get('SPFHHeightLevel3')
    SPFHHeightLevel4 = processed_data.get('SPFHHeightLevel4')
    SPFHHeightLevel5 = processed_data.get('SPFHHeightLevel5')
    SPFHHeightLevel6 = processed_data.get('SPFHHeightLevel6')
    SPFHHeightLevel7 = processed_data.get('SPFHHeightLevel7')
    SPFHHeightLevel8 = processed_data.get('SPFHHeightLevel8')
    SPFHHeightLevel9 = processed_data.get('SPFHHeightLevel9')
    SPFHHeightLevel10 = processed_data.get('SPFHHeightLevel10')
    SPFHHeightLevel11 = processed_data.get('SPFHHeightLevel11')
    SPFHHeightLevel12 = processed_data.get('SPFHHeightLevel12')

    BoundaryLayerHeight_Herbie = BoundaryLayerHeight
    U_and_V_WindComponent_Herbie = U_and_V_WindComponent
    Temperature_Herbie = Temperature
    TKE_Herbie = TKE
    PRES_Herbie = PRES
    SPFH_Herbie = SPFH












    if U_and_V_WindComponent_Herbie == "yes":
        strUandV = "yes"
    else:
        strUandV = "no"

    if Temperature_Herbie == "yes":
        strTMP = "yes"
    else:
        strTMP = "no"

    if TKE_Herbie == "yes":
        strTKE = "yes"
    else:
        strTKE = "no"

    if PRES_Herbie == "yes":
        strPRES = "yes"
    else:
        strPRES = "no"

    if SPFH_Herbie == "yes":
        strSPFH = "yes"
    else:
        strSPFH = "no"



    LBLH = None

    LWHGT1 = LWHGT2 = LWHGT3 = LWHGT4 = LWHGT5 = LWHGT6 = None
    LWHGT7 = LWHGT8 = LWHGT9 = LWHGT10 = LWHGT11 = LWHGT12 = None

    LTHGT1 = LTHGT2 = LTHGT3 = LTHGT4 = LTHGT5 = LTHGT6 = None
    LTHGT7 = LTHGT8 = LTHGT9 = LTHGT10 = LTHGT11 = LTHGT12 = None

    LTKEHGT1 = LTKEHGT2 = LTKEHGT3 = LTKEHGT4 = LTKEHGT5 = LTKEHGT6 = None
    LTKEHGT7 =LTKEHGT8 = LTKEHGT9 = LTKEHGT10 = LTKEHGT11 = LTKEHGT12 = None

    LPRESHGT1 = LPRESHGT2 = LPRESHGT3 = LPRESHGT4 = None
    LPRESHGT5 = LPRESHGT6 = LPRESHGT7 = LPRESHGT8 = None
    LPRESHGT9 = LPRESHGT10 = LPRESHGT11 = LPRESHGT12 = None

    LSPFHHGT1 = LSPFHHGT2 = LSPFHHGT3 = LSPFHHGT4 = None
    LSPFHHGT5 = LSPFHHGT6 = LSPFHHGT7 = LSPFHHGT8 = None
    LSPFHHGT9 = LSPFHHGT10 = LSPFHHGT11 = LSPFHHGT12 = None


    grib_dict = create_grib_code_dict()

    if BoundaryLayerHeight_Herbie == "yes":
        LBLH = ":HPBL:surface"

    if WindHeightLevel1 == "yes" and strUandV == "yes":
        LWHGT1 = ":[U|V]GRD:[1] hybrid"

    if WindHeightLevel2 == "yes" and strUandV == "yes":
        LWHGT2 = ":[U|V]GRD:[2] hybrid"

    if WindHeightLevel3 == "yes" and strUandV == "yes":
        LWHGT3 = ":[U|V]GRD:[3] hybrid"

    if WindHeightLevel4 == "yes" and strUandV == "yes":
        LWHGT4 = ":[U|V]GRD:[4] hybrid"

    if WindHeightLevel5 == "yes" and strUandV == "yes":
        LWHGT5 = ":[U|V]GRD:[5] hybrid"

    if WindHeightLevel6 == "yes" and strUandV == "yes":
        LWHGT6 = ":[U|V]GRD:[6] hybrid"

    if WindHeightLevel7 == "yes" and strUandV == "yes":
        LWHGT7 = ":[U|V]GRD:[7] hybrid"

    if WindHeightLevel8 == "yes" and strUandV == "yes":
        LWHGT8 = ":[U|V]GRD:[8] hybrid"

    if WindHeightLevel9 == "yes" and strUandV == "yes":
        LWHGT9 = ":[U|V]GRD:[9] hybrid"

    if WindHeightLevel10 == "yes" and strUandV == "yes":
        LWHGT10 = ":[U|V]GRD:10 hybrid"

    if WindHeightLevel11 == "yes" and strUandV == "yes":
        LWHGT11 = ":[U|V]GRD:11 hybrid"

    if WindHeightLevel12 == "yes" and strUandV == "yes":
        LWHGT12 = ":[U|V]GRD:12 hybrid"

    if TemperatureHeightLevel1 == "yes" and strTMP == "yes":
        LTHGT1 = grib_dict["NAT"]["temp"]["grib_codes"][0]

    if TemperatureHeightLevel2 == "yes" and strTMP == "yes":
        LTHGT2 = grib_dict["NAT"]["temp"]["grib_codes"][1]

    if TemperatureHeightLevel3 == "yes" and strTMP == "yes":
        LTHGT3 = grib_dict["NAT"]["temp"]["grib_codes"][2]

    if TemperatureHeightLevel4 == "yes" and strTMP == "yes":
        LTHGT4 = grib_dict["NAT"]["temp"]["grib_codes"][3]

    if TemperatureHeightLevel5 == "yes" and strTMP == "yes":
        LTHGT5 = grib_dict["NAT"]["temp"]["grib_codes"][4]

    if TemperatureHeightLevel6 == "yes" and strTMP == "yes":
        LTHGT6 = grib_dict["NAT"]["temp"]["grib_codes"][5]

    if TemperatureHeightLevel7 == "yes" and strTMP == "yes":
        LTHGT7 = grib_dict["NAT"]["temp"]["grib_codes"][6]

    if TemperatureHeightLevel8 == "yes" and strTMP == "yes":
        LTHGT8 = grib_dict["NAT"]["temp"]["grib_codes"][7]

    if TemperatureHeightLevel9 == "yes" and strTMP == "yes":
        LTHGT9 = grib_dict["NAT"]["temp"]["grib_codes"][8]

    if TemperatureHeightLevel10 == "yes" and strTMP == "yes":
        LTHGT10 = grib_dict["NAT"]["temp"]["grib_codes"][9]

    if TemperatureHeightLevel11 == "yes" and strTMP == "yes":
        LTHGT11 = grib_dict["NAT"]["temp"]["grib_codes"][10]

    if TemperatureHeightLevel12 == "yes" and strTMP == "yes":
        LTHGT12 = grib_dict["NAT"]["temp"]["grib_codes"][11]


    if TKEHeightLevel1 == "yes" and strTKE == "yes":
        LTKEHGT1 = ":TKE:[1] hybrid level"

    if TKEHeightLevel2 == "yes" and strTKE == "yes":
        LTKEHGT2 = ":TKE:[2] hybrid level"

    if TKEHeightLevel3 == "yes" and strTKE == "yes":
        LTKEHGT3 = ":TKE:[3] hybrid level"

    if TKEHeightLevel4 == "yes" and strTKE == "yes":
        LTKEHGT4 = ":TKE:[4] hybrid level"

    if TKEHeightLevel5 == "yes" and strTKE == "yes":
        LTKEHGT5 = ":TKE:[5] hybrid level"

    if TKEHeightLevel6 == "yes" and strTKE == "yes":
        LTKEHGT6 = ":TKE:[6] hybrid level"

    if TKEHeightLevel7 == "yes" and strTKE == "yes":
        LTKEHGT7 = ":TKE:[7] hybrid level"

    if TKEHeightLevel8 == "yes" and strTKE == "yes":
        LTKEHGT8 = ":TKE:[8] hybrid level"

    if TKEHeightLevel9 == "yes" and strTKE == "yes":
        LTKEHGT9 = ":TKE:[9] hybrid level"

    if TKEHeightLevel10 == "yes" and strTKE == "yes":
        LTKEHGT10 = ":TKE:10 hybrid level"

    if TKEHeightLevel11 == "yes" and strTKE == "yes":
        LTKEHGT11 = ":TKE:11 hybrid level"

    if TKEHeightLevel12 == "yes" and strTKE == "yes":
        LTKEHGT12 = ":TKE:12 hybrid level"

    if PRESHeightLevel1 == "yes" and strPRES == "yes":
        LPRESHGT1 = ":PRES:[1] hybrid level"

    if PRESHeightLevel2 == "yes" and strPRES == "yes":
        LPRESHGT2 = ":PRES:[2] hybrid level"

    if PRESHeightLevel3 == "yes" and strPRES == "yes":
        LPRESHGT3 = ":PRES:[3] hybrid level"

    if PRESHeightLevel4 == "yes" and strPRES == "yes":
        LPRESHGT4 = ":PRES:[4] hybrid level"

    if PRESHeightLevel5 == "yes" and strPRES == "yes":
        LPRESHGT5 = ":PRES:[5] hybrid level"

    if PRESHeightLevel6 == "yes" and strPRES == "yes":
        LPRESHGT6 = ":PRES:[6] hybrid level"

    if PRESHeightLevel7 == "yes" and strPRES == "yes":
        LPRESHGT7 = ":PRES:[7] hybrid level"

    if PRESHeightLevel8 == "yes" and strPRES == "yes":
        LPRESHGT8 = ":PRES:[8] hybrid level"

    if PRESHeightLevel9 == "yes" and strPRES == "yes":
        LPRESHGT9 = ":PRES:[9] hybrid level"

    if PRESHeightLevel10 == "yes" and strPRES == "yes":
        LPRESHGT10 = ":PRES:10 hybrid level"

    if PRESHeightLevel11 == "yes" and strPRES == "yes":
        LPRESHGT11 = ":PRES:11 hybrid level"

    if PRESHeightLevel12 == "yes" and strPRES == "yes":
        LPRESHGT12 = ":PRES:12 hybrid level"

    if SPFHHeightLevel1 == "yes" and strSPFH == "yes":
        LSPFHHGT1 = ":SPFH:[1] hybrid level"

    if SPFHHeightLevel2 == "yes" and strSPFH == "yes":
        LSPFHHGT2 = ":SPFH:[2] hybrid level"

    if SPFHHeightLevel3 == "yes" and strSPFH == "yes":
        LSPFHHGT3 = ":SPFH:[3] hybrid level"

    if SPFHHeightLevel4 == "yes" and strSPFH == "yes":
        LSPFHHGT4 = ":SPFH:[4] hybrid level"

    if SPFHHeightLevel5 == "yes" and strSPFH == "yes":
        LSPFHHGT5 = ":SPFH:[5] hybrid level"

    if SPFHHeightLevel6 == "yes" and strSPFH == "yes":
        LSPFHHGT6 = ":SPFH:[6] hybrid level"

    if SPFHHeightLevel7 == "yes" and strSPFH == "yes":
        LSPFHHGT7 = ":SPFH:[7] hybrid level"

    if SPFHHeightLevel8 == "yes" and strSPFH == "yes":
        LSPFHHGT8 = ":SPFH:[8] hybrid level"

    if SPFHHeightLevel9 == "yes" and strSPFH == "yes":
        LSPFHHGT9 = ":SPFH:[9] hybrid level"

    if SPFHHeightLevel10 == "yes" and strSPFH == "yes":
        LSPFHHGT10 = ":SPFH:10 hybrid level"

    if SPFHHeightLevel11 == "yes" and strSPFH == "yes":
        LSPFHHGT11 = ":SPFH:11 hybrid level"

    if SPFHHeightLevel12 == "yes" and strSPFH == "yes":
        LSPFHHGT12 = ":SPFH:12 hybrid level"


    search_patterns = [
    LBLH, LWHGT1, LWHGT2, LWHGT3, LWHGT4, LWHGT5, LWHGT6, LWHGT7, LWHGT8, LWHGT9, LWHGT10, LWHGT11, LWHGT12,
    LTHGT1, LTHGT2, LTHGT3, LTHGT4, LTHGT5, LTHGT6, LTHGT7, LTHGT8, LTHGT9, LTHGT10, LTHGT11, LTHGT12,
    LTKEHGT1, LTKEHGT2, LTKEHGT3, LTKEHGT4, LTKEHGT5, LTKEHGT6, LTKEHGT7, LTKEHGT8, LTKEHGT9, LTKEHGT10, LTKEHGT11, LTKEHGT12,
    LPRESHGT1, LPRESHGT2, LPRESHGT3, LPRESHGT4, LPRESHGT5, LPRESHGT6, LPRESHGT7, LPRESHGT8, LPRESHGT9, LPRESHGT10, LPRESHGT11, LPRESHGT12,
    LSPFHHGT1, LSPFHHGT2, LSPFHHGT3, LSPFHHGT4, LSPFHHGT5, LSPFHHGT6, LSPFHHGT7, LSPFHHGT8, LSPFHHGT9, LSPFHHGT10, LSPFHHGT11, LSPFHHGT12
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


def check_herbie_condition(processed_data):
    if processed_data.get('HerbieAlreadyDone') != 'yes':
        return True
    else:
        return False


def fetch_herbie_data_in_range(processed_data):
    if check_herbie_condition(processed_data):
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

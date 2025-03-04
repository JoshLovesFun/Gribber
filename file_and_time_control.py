def expected_file_count(processed_data):
    # File count if we only produce nat or prs files.
    dir_file_count = 24

    if processed_data.get('wrf') == "yes":
        dir_file_count = 48

    if processed_data.get('BoundaryLayerHeight') == "yes" and (
            processed_data.get('U_and_V_WindComponent') == "yes" or
            processed_data.get('Temperature') == "yes" or
            processed_data.get('TKE') == "yes" or
            processed_data.get('PRES') == "yes" or
            processed_data.get('SPFH') == "yes"):
        dir_file_count = 48

    return dir_file_count

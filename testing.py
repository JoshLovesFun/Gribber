
import pprint
import grib


def run_test():
    prs_files = ["file1.prs", "file2.prs", "file3.prs"]
    sub_files = ["file1.sub", "file2.sub", "file3.sub"]
    nat_files = ["file1.nat", "file2.nat", "file3.nat"]

    shortnames_for_prs = ["blh", "t", "t", "t", "other"]
    grid_cell_for_prs = [150, 150, 175]
    level_for_prs = ["0", "1", "2", "11", "7"]
    hour_date_for_prs = [(11, 202501), (12, 202501), (13, 202501)]

    shortnames_for_nat = ["blh", "test"]
    grid_cell_for_nat = [140, 119, 140]
    level_for_nat = ["0", "15"]
    hour_date_for_nat = [(5, 202502), (6, 202502), (7, 202502)]

    shortnames_for_sub = ["v", "v", "v"]
    grid_cell_for_sub = [133, 130, 130]
    level_for_sub = ["5", "6", "9"]
    hour_date_for_sub = [(1, 202507), (2, 202507), (3, 202507)]

    test = grib.populate_files(
        prs_files, sub_files, nat_files,
        shortnames_for_prs, level_for_prs, grid_cell_for_prs,
        hour_date_for_prs,
        shortnames_for_nat, level_for_nat, grid_cell_for_nat,
        hour_date_for_nat,
        shortnames_for_sub, level_for_sub, grid_cell_for_sub, hour_date_for_sub
    )

    pprint.pprint(test)


if __name__ == "__main__":
    run_test()

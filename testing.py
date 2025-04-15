import pprint
import grib


def run_test():
    prs_files = ["file1.prs", "file2.prs", "file3.prs"]
    nat_files = ["file1.nat", "file2.nat", "file3.nat"]

    shortnames_for_prs = ["blh", "t", "t", "t", "other"]
    grid_cell_for_prs = [150, 150, 175]
    level_for_prs = ["0", "1", "2", "11", "7"]
    hour_date_for_prs = [(11, 202501), (12, 202501), (13, 202501)]

    shortnames_for_nat = ["blh", "test"]
    grid_cell_for_nat = [140, 119, 140]
    level_for_nat = ["0", "15"]
    hour_date_for_nat = [(5, 202502), (6, 202502), (7, 202502)]

    test = grib.populate_files(
        prs_files, nat_files,
        shortnames_for_prs, level_for_prs, grid_cell_for_prs,
        hour_date_for_prs,
        shortnames_for_nat, level_for_nat, grid_cell_for_nat,
        hour_date_for_nat
    )

    pprint.pprint(test)


if __name__ == "__main__":
    run_test()

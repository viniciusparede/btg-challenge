import os

from utils.bln_reader import read_contour_file
from utils.dat_reader import read_data_file


FILE_DIR: str = os.path.dirname(os.path.abspath(__file__))
DATA_DIR: str = os.path.join(FILE_DIR, "data")


def main() -> None:
    df = read_contour_file(file_path=os.path.join(DATA_DIR, "PSATCMG_CAMARGOS.bln"))
    df = read_data_file(file_path=os.path.join(DATA_DIR, "ETA40_p011221a021221.dat"))

if __name__ == "__main__":
    main()

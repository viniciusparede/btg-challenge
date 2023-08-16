import os

from utils.bln_reader import read_contour_file
from utils.dat_reader import multithreading_reader_data_file


FILE_DIR: str = os.path.dirname(os.path.abspath(__file__))
DATA_DIR: str = os.path.join(FILE_DIR, "data")


def main() -> None:
    forecast_df = multithreading_reader_data_file(folder_path=DATA_DIR)
    print(forecast_df)


if __name__ == "__main__":
    main()

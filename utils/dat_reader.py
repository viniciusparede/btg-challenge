import pandas as pd


def read_data_file(file_path: str) -> pd.DataFrame:
    with open(file_path, "r") as f:
        raw_file = f.readlines()

    list_dados = [line.split() for line in raw_file]
    float_raw_lines = [list(map(float, raw_line)) for raw_line in list_dados]
    return pd.DataFrame(float_raw_lines, columns=["lat", "long", "data_value"])

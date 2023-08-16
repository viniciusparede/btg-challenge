import re
import pandas as pd


def read_contour_file(file_path: str) -> pd.DataFrame:
    line_split_comp = re.compile(r"\s*,")

    with open(file_path, "r") as f:
        raw_file = f.readlines()

    l_raw_lines = [
        line_split_comp.split(raw_file_line.strip()) for raw_file_line in raw_file
    ]
    l_raw_lines = list(filter(lambda item: bool(item[0]), l_raw_lines))
    float_raw_lines = [list(map(float, raw_line))[:2] for raw_line in l_raw_lines]
    header_line = float_raw_lines.pop(0)
    assert len(float_raw_lines) == int(header_line[0])
    return pd.DataFrame(float_raw_lines, columns=["lat", "long"])

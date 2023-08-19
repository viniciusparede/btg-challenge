import os
import re
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

import pandas as pd


def read_contour_file(file_path: str) -> pd.DataFrame:
    """
    Lê um arquivo de contorno e extrai as coordenadas de latitude e longitude.

    Args:
        file_path (str): O caminho para o arquivo de contorno.

    Returns:
        pd.DataFrame: Um DataFrame contendo as coordenadas de latitude e longitude.

    Raises:
        AssertionError: Se o número de linhas no arquivo não corresponder ao valor especificado no cabeçalho.
    """
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


def read_dat_file_to_dataframe(file_path: str) -> pd.DataFrame:
    """
    Lê um arquivo de dados do tipo .dat e cria um DataFrame com as colunas "lat", "long", "data_value" e "file_path".

    Args:
        file_path (str): Caminho do arquivo a ser lido.

    Returns:
        pd.DataFrame: DataFrame contendo os dados do arquivo.
    """
    if file_path[-4:] == ".dat":
        with open(file_path, "r") as f:
            raw_file = f.readlines()

        list_dados = [line.split() for line in raw_file]
        float_raw_lines = [list(map(float, raw_line)) for raw_line in list_dados]
        df = pd.DataFrame(float_raw_lines, columns=["lat", "long", "data_value"])
        df["file_path"] = file_path
        return df


def multithreading_reader_dat_file(folder_path: str) -> pd.DataFrame:
    """
    Lê vários arquivos de dados do tipo .dat em paralelo utilizando threads e cria um DataFrame combinado.

    Args:
        folder_path (str): Caminho da pasta contendo os arquivos de dados.

    Returns:
        pd.DataFrame: DataFrame combinado contendo os dados de todos os arquivos.
    """
    file_paths = [
        os.path.join(folder_path, filename) for filename in os.listdir(folder_path)
    ]
    num_files = len(file_paths)
    num_cpus = multiprocessing.cpu_count()
    num_workers = min(num_files, num_cpus)

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        dfs = executor.map(read_dat_file_to_dataframe, file_paths)

    combined_df = pd.concat(list(dfs), ignore_index=True)
    return combined_df

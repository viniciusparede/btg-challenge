import os

import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point


from bln_reader import read_contour_file

from typing import Optional, List


FILE_DIR: str = os.path.dirname(os.path.abspath(__file__))
BASE_DIR: str = os.path.dirname(FILE_DIR)
DATA_DIR: str = os.path.join(BASE_DIR, "data")


def _create_geometry_column(df: pd.DataFrame, precision: int) -> List[Point]:
    """
    Cria uma lista de objetos Point do módulo shapely.geometry a partir das colunas "lat" e "long" de um DataFrame.

    Args:
        df (pd.DataFrame): O DataFrame contendo as colunas "lat" e "long" que representam as coordenadas.

    Returns:
        List[Point]: Uma lista de objetos Point criados a partir das coordenadas.

    Raises:
        ValueError: Se as colunas "lat" ou "long" não estiverem presentes no DataFrame.

    Example:
        df = pd.DataFrame({
            "lat": [latitude_1, latitude_2, latitude_3],
            "long": [longitude_1, longitude_2, longitude_3]
        })
        geometry_list = _create_geometry_column(df)
    """
    columns = df.columns
    if not "lat" in columns:
        raise ValueError(
            "O dataframe repassado como argumento não contém a coluna latitude 'lat'"
        )

    if not "long" in columns:
        raise ValueError(
            "O dataframe repassado como argumento não contém a coluna longitude 'long'"
        )

    return [
        Point(xy)
        for xy in zip(round(df["lat"], precision), round(df["long"], precision))
    ]


def preprocess_routine(
    contour_file_path: str, forecast_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Realiza uma rotina de pré-processamento que inclui a leitura do arquivo de contorno
    da bacia hidrográfica, a conversão de DataFrames em GeoDataFrames, a junção por proximidade e ajustes nas colunas.

    Args:
        contour_file_path (str): O caminho para o arquivo de contorno.
        forecast_df (pd.DataFrame): O DataFrame contendo os dados de previsão.

    Returns:
        pd.DataFrame: O DataFrame resultante após a junção e ajustes.

    Raises:
        ValueError: Se o arquivo de contorno não existir.

    Example:
        contour_path = "PSATCMG_CAMARGOS.bln"
        forecast_data = pd.DataFrame(...)  # Seus dados de previsão
        preprocessed_data = preprocess_routine(contour_path, forecast_data)
    """
    if not os.path.exists(contour_file_path):
        raise ValueError(f"O arquivo {contour_file_path} não existe")

    # dataframe da bacia hidrográfica
    contour_df: pd.DataFrame = read_contour_file(
        file_path=os.path.join(DATA_DIR, contour_file_path)
    )

    # Converter 'pandas.DataFrame' em 'GeoDataFrame'
    gcontour_df = gpd.GeoDataFrame(
        contour_df, geometry=_create_geometry_column(contour_df, precision=1)
    )
    gforecast_df = gpd.GeoDataFrame(
        forecast_df, geometry=_create_geometry_column(forecast_df, precision=1)
    )

    # Realizar a junção usando o método sjoin_nearest com base na coluna rounded_geometry
    result = gpd.sjoin_nearest(
        left_df=gcontour_df, right_df=gforecast_df, how="inner", distance_col="distance"
    )

    # renomear colunas
    result.rename(
        columns={
            "lat_left": "lat_referencia",
            "long_left": "long_referencia",
            "lat_right": "lat_aproximacao",
            "long_right": "long_aproximacao",
        },
        inplace=True,
    )

    # retirar colunas não utilizadas
    result.drop(columns="index_right", inplace=True)

    return result


if __name__ == "__main__":
    import os

    from dat_reader import multithreading_reader_data_file

    preprocess_routine(
        contour_file_path="/home/viniciusparede/repositories/personal/btg-challenge/data/PSATCMG_CAMARGOS.bln",
        forecast_df=multithreading_reader_data_file(folder_path=DATA_DIR),
    )

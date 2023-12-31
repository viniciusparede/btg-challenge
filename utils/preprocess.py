import os
import sys
from datetime import datetime
from typing import List, Optional

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Varíaveis globais
FILE_DIR: str = os.path.dirname(os.path.abspath(__file__))
BASE_DIR: str = os.path.dirname(FILE_DIR)
DATA_DIR: str = os.path.join(BASE_DIR, "data")

# Dados obetidos através do estudo de contorno, conforme a image 'contorno.png'
POLYGONAL_ORDER = [
    (-44.6, -22.2),
    (-44.6, -21.8),
    (-44.6, -21.4),
    (-44.2, -21.4),
    (-43.8, -21.4),
    (-43.8, -21.8),
    (-44.2, -21.8),
    (-44.2, -22.2),
]


def _create_geometry_column(df: pd.DataFrame) -> List[Point]:
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

    return [Point(xy) for xy in zip(df["lat"], df["long"])]


def _format_date(string):
    # Função para extrair e formatar a data

    # Extrai a parte da string com a data (061221)
    date_part = string[-10:-4]

    # Converte a string em objeto de data
    date_object = datetime.strptime(date_part, "%d%m%y")

    # Formata a data como '06/12/21'
    formatted_date = date_object.strftime("%d/%m/%y")
    return formatted_date


def apply_contour(
    contour_df: pd.DataFrame,
    forecast_df: pd.DataFrame,
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

        # Seus dados de previsão
        forecast_data = pd.DataFrame(...)

        preprocessed_data = preprocess_routine(contour_path, forecast_data)
    """

    # Converter 'pandas.DataFrame' em 'GeoDataFrame'
    gcontour_df = gpd.GeoDataFrame(
        contour_df, geometry=_create_geometry_column(contour_df)
    )
    gforecast_df = gpd.GeoDataFrame(
        forecast_df, geometry=_create_geometry_column(forecast_df)
    )

    # Realizar a junção usando o método sjoin_nearest com base na coluna rounded_geometry
    result = gpd.sjoin_nearest(
        left_df=gcontour_df,
        right_df=gforecast_df,
        how="left",
        distance_col="distance",
        max_distance=sys.maxsize,
    )

    # Renomear colunas
    result.rename(
        columns={
            "lat_left": "lat_referencia",
            "long_left": "long_referencia",
            "lat_right": "lat_aproximacao",
            "long_right": "long_aproximacao",
        },
        inplace=True,
    )

    # Aplica a função para criar uma nova coluna 'formatted_date'
    result["data_previsao"] = result["file_path"].apply(_format_date)

    # retirar colunas não utilizadas
    result.drop(columns=["index_right", "file_path"], inplace=True)

    # Converter o GeoDataFrame para um DataFrame do pandas
    # Remover a coluna de geometria
    df_without_geometry = result.drop("geometry", axis=1)
    pandas_df = df_without_geometry.copy()

    return pandas_df


def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    """Realiza transformações específicas nos dados"""

    # Cópia do dataframe para variável 'df'
    df = data.copy()

    # Seleção apenas das colunas que interessam
    df = df.loc[
        :, ["lat_aproximacao", "long_aproximacao", "data_value", "data_previsao"]
    ].copy()

    # Retirada de linhas duplicadas em um determinado ponto com os
    # mesmos valores de precipitação
    df.drop_duplicates(
        subset=["lat_aproximacao", "long_aproximacao", "data_value"], inplace=True
    )

    # Ordena o dataframe com base nas localizações e a data de previsão
    df.sort_values(
        by=["lat_aproximacao", "long_aproximacao", "data_previsao"], inplace=True
    )

    # Resetar os índices
    df.reset_index(drop=True, inplace=True)

    # Criar uma coluna que represente a ordem específica do polígono
    df["ordem"] = df.apply(
        lambda row: POLYGONAL_ORDER.index(
            (row["lat_aproximacao"], row["long_aproximacao"])
        ),
        axis=1,
    )

    # Ordenar o DataFrame pela coluna 'ordem' e, em seguida, remover a coluna 'ordem'
    df_ordenado = df.sort_values(by="ordem").drop("ordem", axis=1)

    # df assume a ordenação
    df = df_ordenado.copy()

    return df

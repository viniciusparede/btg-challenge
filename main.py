import os
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from scipy.integrate import cumulative_trapezoid

# Módulos auxiliares
from utils.data_reader import multithreading_reader_dat_file, read_contour_file
from utils.preprocess import apply_contour
from utils.predict import predict_precipitation
from utils.plotter import result_figure

# Variáveis globais
FILE_DIR = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(FILE_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")

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


def load_data() -> pd.DataFrame:
    """Carrega os dados dos arquivos"""

    # DataFrame com os dados
    contour = (
        read_contour_file(
            file_path="/home/viniciusparede/repositories/personal/btg-challenge/data/PSATCMG_CAMARGOS.bln"
        ),
    )[0]

    # DataFrame com as previsões de precitações
    forecast = multithreading_reader_dat_file(folder_path=DATA_DIR)

    # DataFrame com previsões e dados da área da bacia
    df = apply_contour(contour, forecast)

    return df


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


def main() -> None:
    # Dataframe base
    df = load_data().pipe(transform_data)

    # Datas de predição
    dates = df["data_previsao"].sort_values().unique()

    # Resultado de predição para cada data
    result = [predict_precipitation(df.copy(), date) for date in dates]

    # Calculando o resultado acumulado
    acumulado = np.cumsum(result)

    print(f"Precipitação acumulada: {np.round(np.max(acumulado), 2)} mm")

    # Figura do resultado - /images/result.png
    result_figure(result)


if __name__ == "__main__":
    main()

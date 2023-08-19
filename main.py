import os
import numpy as np
import pandas as pd


# Módulos auxiliares
from utils.data_reader import multithreading_reader_dat_file, read_contour_file
from utils.preprocess import apply_contour, transform_data
from utils.model import PrecipitationModel
from utils.plotter import result_figure

# Variáveis globais
FILE_DIR = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(FILE_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")


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


def main() -> None:
    # Dataframe base
    df: pd.DataFrame = load_data().pipe(transform_data)

    # Datas de predição
    dates = df["data_previsao"].sort_values().unique()

    # Resultado de predição para cada data
    model = PrecipitationModel(data=df.copy())
    result = [model.predict(date) for date in dates]

    # Calculando o resultado acumulado
    cumulative_result = np.cumsum(result)

    print(f"Precipitação acumulada: {np.round(np.max(cumulative_result), 2)} mm")

    # Figura do resultado - /images/result.png
    result_figure(result)
    result_dir = os.path.join(os.path.join(DATA_DIR, "images"), "result.png")
    print(f"Resultado na pasta: {result_dir}")


if __name__ == "__main__":
    main()

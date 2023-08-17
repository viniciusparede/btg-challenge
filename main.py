import os
import click

from scipy.integrate import trapz

from utils.bln_reader import read_contour_file
from utils.dat_reader import multithreading_reader_data_file
from utils.preprocess import preprocess_routine

FILE_DIR: str = os.path.dirname(os.path.abspath(__file__))
DATA_DIR: str = os.path.join(FILE_DIR, "data")


def main() -> None:
    # DataFrame c/ coordenadas da Bacia Hidrográfica
    contour_df = read_contour_file(
        file_path=os.path.join(DATA_DIR, "PSATCMG_CAMARGOS.bln")
    )

    # DataFrame c/ coordenadas e precipitação
    forecast_df = multithreading_reader_data_file(folder_path=DATA_DIR)

    # DataFrame completo
    df = preprocess_routine(contour_df, forecast_df)

    # Dados de precipitação
    precipitacao = df["data_value"].values

    # Cálculo da média da precipitação usando a integral de linha (regra do trapézio)
    caminho_length = len(precipitacao)
    integral_precipitacao = trapz(precipitacao, dx=1)
    precipitacao_media = integral_precipitacao / caminho_length

    print(f"Precipitação média acumulada: {round(precipitacao_media, 0)} mm")


if __name__ == "__main__":
    main()

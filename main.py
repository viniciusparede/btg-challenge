import os

import numpy as np
from scipy.interpolate import griddata
from scipy.integrate import cumulative_trapezoid


# Módulos auxiliaries
from utils.bln_reader import read_contour_file
from utils.dat_reader import multithreading_reader_data_file
from utils.preprocess import preprocess_routine

FILE_DIR = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(FILE_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")

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


def main() -> None:
    contour_df = (
        read_contour_file(
            file_path="/home/viniciusparede/repositories/personal/btg-challenge/data/PSATCMG_CAMARGOS.bln"
        ),
    )[0]

    forecast_df = multithreading_reader_data_file(folder_path=DATA_DIR)

    df = preprocess_routine(contour_df, forecast_df)

    df = df.loc[
        :, ["lat_aproximacao", "long_aproximacao", "data_value", "data_previsao"]
    ].copy()

    df.drop_duplicates(
        subset=["lat_aproximacao", "long_aproximacao", "data_value"], inplace=True
    )

    df.sort_values(
        by=["lat_aproximacao", "long_aproximacao", "data_previsao"], inplace=True
    )
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

    z = 0
    dates = df["data_previsao"].sort_values().unique()
    result = list()
    for _ in range(2):
        for _ in range(5):
            data = list(
                df.loc[df["data_previsao"] == dates[z]]
                .copy()
                .itertuples(index=False, name=None)
            )

            # latitude, longitude e valores de precipitação
            latitude = [d[0] for d in data]
            longitude = [d[1] for d in data]
            precipitacao = [d[2] for d in data]

            # Definindo Intervalos
            latitude_linspace = np.linspace(min(latitude), max(latitude), 1000)
            longitude_linspace = np.linspace(min(longitude), max(longitude), 1000)

            # Definir a mesgrid para a interpolação
            grid_x, grid_y = np.meshgrid(
                latitude_linspace,
                longitude_linspace,
            )

            # Interpolação
            grid_precipitacao = griddata(
                (latitude, longitude), precipitacao, (grid_x, grid_y), method="cubic"
            )

            # Calcular a integral da precipitação interpolada
            integral_precipitacao = cumulative_trapezoid(grid_precipitacao, x=grid_x)

            # Criar uma máscara booleana para identificar valores não NaN
            mascara = ~np.isnan(integral_precipitacao)

            # Aplicar a máscara para selecionar elementos não NaN
            vetor_sem_nan = integral_precipitacao[mascara]

            result.append(np.max(vetor_sem_nan))

            z += 1

    # Calculando o resultado acumulado
    acumulado = np.cumsum(result)

    print(f"Precipitação acumulada: {np.round(np.max(acumulado), 2)} mm")


if __name__ == "__main__":
    main()

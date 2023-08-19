import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from scipy.integrate import cumulative_trapezoid


def predict_precipitation(df: pd.DataFrame, date: str) -> float:
    data = list(
        df.loc[df["data_previsao"] == date].copy().itertuples(index=False, name=None)
    )

    # latitude, longitude e valores de precipitação
    latitude = [d[0] for d in data]
    longitude = [d[1] for d in data]
    precipitation = [d[2] for d in data]

    # Definindo Intervalos
    latitude_linspace = np.linspace(min(latitude), max(latitude), 1000)
    longitude_linspace = np.linspace(min(longitude), max(longitude), 1000)

    # Definir a mesgrid para a interpolação
    grid_x, grid_y = np.meshgrid(
        latitude_linspace,
        longitude_linspace,
    )

    # Interpolação
    precipation_grid = griddata(
        (latitude, longitude), precipitation, (grid_x, grid_y), method="cubic"
    )

    # Calcular a integral da precipitação interpolada
    precipitation_integral = cumulative_trapezoid(precipation_grid, x=grid_x)

    # Criar uma máscara booleana para identificar valores não NaN
    mask = ~np.isnan(precipitation_integral)

    # Aplicar a máscara para selecionar elementos não NaN
    result = np.max(precipitation_integral[mask])

    return result

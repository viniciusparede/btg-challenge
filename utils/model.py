import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from scipy.integrate import cumulative_trapezoid


class PrecipitationModel(object):
    """
    Uma classe para modelar previsões de precipitação e calcular integrais cumulativas.

    Args:
        data (pd.DataFrame): Um DataFrame contendo os dados de previsão de precipitação com
                            as colunas 'latitude', 'longitude', 'data_previsao' e 'precipitacao'.

    Attributes:
        df (pd.DataFrame): O DataFrame contendo os dados de previsão de precipitação.
        latitude_linspace (np.ndarray): Um array 1D representando a interpolação das latitudes.
        longitude_linspace (np.ndarray): Um array 1D representando a interpolação das longitudes.
        grid_x (np.ndarray): A malha de coordenadas X para interpolação.
        grid_y (np.ndarray): A malha de coordenadas Y para interpolação.
        precipitation_grid (np.ndarray): Uma matriz 2D contendo os valores interpolados de precipitação.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        """
        Inicializa a classe com os dados de previsão de precipitação.
        """
        self.df = data.copy()

    def interpolation(self) -> np.ndarray:
        """
        Realiza a interpolação dos dados de previsão de precipitação.

        Returns:
            np.ndarray: Uma matriz 2D contendo os valores interpolados de precipitação.
        """
        self.latitude_linspace = np.linspace(
            min(self.latitude), max(self.latitude), 1000
        )

        self.longitude_linspace = np.linspace(
            min(self.longitude), max(self.longitude), 1000
        )

        # Definir a mesgrid para a interpolação
        grid_x, grid_y = np.meshgrid(
            self.latitude_linspace,
            self.longitude_linspace,
        )
        self.grid_x = grid_x
        self.grid_y = grid_y

        # Interpolação
        self.precipitation_grid = griddata(
            (self.latitude, self.longitude),
            self.precipitation,
            (self.grid_x, self.grid_y),
            method="cubic",
        )
        return self.precipitation_grid

    def predict(self, date: str):
        """
        Calcula a integral cumulativa da precipitação interpolada para uma data específica.

        Args:
            date (str): A data para a qual a previsão de precipitação será calculada.

        Returns:
            float: A integral cumulativa máxima da precipitação interpolada.
        """
        self.date = date
        self.data = list(
            self.df.loc[self.df["data_previsao"] == self.date]
            .copy()
            .itertuples(index=False, name=None)
        )

        self.latitude = [d[0] for d in self.data]
        self.longitude = [d[1] for d in self.data]
        self.precipitation = [d[2] for d in self.data]

        # Calcular a integral da precipitação interpolada
        precipitation_integral = cumulative_trapezoid(
            self.interpolation(), x=self.grid_x
        )

        # Criar uma máscara booleana para identificar valores não NaN
        mask = ~np.isnan(precipitation_integral)

        # Aplicar a máscara para selecionar elementos não NaN
        result = np.max(precipitation_integral[mask])

        return result

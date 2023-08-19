import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


from matplotlib.figure import Figure
from typing import List

# Varíaveis globais
FILE_DIR: str = os.path.dirname(os.path.abspath(__file__))
BASE_DIR: str = os.path.dirname(FILE_DIR)
DATA_DIR: str = os.path.join(BASE_DIR, "data")
IMAGES_DIR: str = os.path.join(BASE_DIR, "images")

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
    (-44.6, -22.2),
]


def contour_figure(data: pd.DataFrame) -> Figure:
    """
    Cria um gráfico de contorno para a Bacia do Rio Grande.

    Este método gera um gráfico de contorno que exibe a Bacia do Rio Grande
    usando as coordenadas de latitude e longitude fornecidas nos dados.

    Parâmetros:
        data (pd.DataFrame): DataFrame contendo as coordenadas de latitude e longitude.

    Retorna:
        Figure: O objeto Figure do matplotlib contendo o gráfico de contorno.

    Exemplo:
        Suponha que 'data' seja um DataFrame contendo as colunas 'lat' e 'long'
        que representam as coordenadas de latitude e longitude da Bacia do Rio Grande.
        Você pode chamar o método da seguinte forma:

        >>> fig = contour_figure(data)
        >>> fig.show()  # Mostra a figura interativamente

    """
    fig, ax = plt.subplots()

    ax.plot(data["lat"], data["long"], color="#0A1E8C")
    ax.set_title("Bacia Rio do Grande")
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Longitude")

    fig.savefig(os.path.join(IMAGES_DIR, "bacia_rio_grande.png"))
    return fig


def apply_contour_figure(data: pd.DataFrame) -> Figure:
    """
    Cria uma figura que ilustra a estratégia de contorno aplicada aos dados.

    Este método gera uma figura que apresenta os resultados da estratégia de contorno
    aplicada aos dados de aproximação e de referência. As trajetórias de contorno
    são plotadas usando as coordenadas de latitude e longitude dos pontos.

    Parâmetros:
        data (pd.DataFrame): DataFrame contendo as coordenadas de latitude e longitude
                             dos pontos de aproximação e referência.

    Retorna:
        Figure: O objeto Figure do matplotlib contendo a figura com a estratégia de contorno.

    Exemplo:
        Suponha que 'data' seja um DataFrame contendo as colunas 'lat_aproximacao',
        'long_aproximacao', 'lat_referencia' e 'long_referencia' que representam
        as coordenadas de latitude e longitude dos pontos de aproximação e referência.
        Você pode chamar o método da seguinte forma:

        >>> fig = apply_contour_figure(data)
        >>> fig.show()  # Mostra a figura interativamente

    """

    fig, ax = plt.subplots()

    ax.plot(
        data["lat_aproximacao"],
        data["long_aproximacao"],
        color="#0A1E8C",
        label="Aproximação",
    )
    ax.plot(
        data["lat_referencia"],
        data["long_referencia"],
        color="#5C88DA",
        label="Referência",
    )

    ax.set_title("Contorno de Aproximação")
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Longitude")
    ax.legend()

    fig.savefig(os.path.join(IMAGES_DIR, "contorno.png"))
    return fig


def interpolation_figure(data: pd.DataFrame) -> Figure:
    from model import PrecipitationModel

    model = PrecipitationModel(data.copy())

    z = 0
    dates = data["data_previsao"].sort_values().unique()

    # Criar uma figura com 5 colunas e 1 linha
    fig, axs = plt.subplots(nrows=2, ncols=5, figsize=(18, 5))

    for i in range(2):
        for j in range(5):
            model.predict(date=dates[z])
            # Plot dos resultados
            axs[i][j].contourf(
                model.grid_x,
                model.grid_y,
                model.precipitation_grid,
                levels=20,
                cmap="Blues",
            )

            axs[i][j].plot(
                [p[0] for p in POLYGONAL_ORDER],
                [p[1] for p in POLYGONAL_ORDER],
                color="red",
            )

            # Ajustar os limites dos eixos
            axs[i][j].set_xlim(-45, -43.5)
            axs[i][j].set_ylim(-22.4, -21.2)

            z += 1

    plt.savefig(os.path.join(IMAGES_DIR, "interpolacao.png"))

    return fig


def result_figure(result: List[float]) -> Figure:
    """Cria a figura do resultado final"""
    # Strings para o eixo X
    labels = [
        "02/dez",
        "03/dez",
        "04/dez",
        "05/dez",
        "06/dez",
        "07/dez",
        "08/dez",
        "09/dez",
        "10/dez",
        "11/dez",
    ]

    # Criar Figura
    fig, ax1 = plt.subplots(figsize=(13.5, 6))

    # Gráfico de barras
    bars = ax1.bar(labels, result, color="#0A1E8C", label="Previsão Diária")

    # Labels
    ax1.set_xlabel("Data de Previsão")
    ax1.set_ylabel("Precipitação [mm]")
    ax1.tick_params(axis="y")

    # Adicionar valores nas barras
    for bar in bars:
        yval = bar.get_height()

        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            yval + 0.7,
            f"{int(round(yval, 1))} mm",
            va="center",
            ha="center",
        )

    # Segundo eixo y para a linha acumulada
    ax2 = ax1.twinx()

    # Resultado acumulado
    cumulative_result = np.cumsum(result)

    # Linha de resultado acumulado
    ax2.plot(
        labels,
        cumulative_result,
        color="#5C88DA",
        marker="o",
        label="Acumulado",
    )

    # Escrita do resultado final acumulado
    offset = 0.1
    ax2.tick_params(axis="y")
    ax2.text(
        offset + bar.get_x() + bar.get_width() / 2.0,
        cumulative_result[-1],
        str(int(cumulative_result[-1])) + " mm",
    )

    # Labels
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc="upper left")

    plt.title("Previsão de precipitação - Bacia Rio Grande")

    # Coordenadas para posicionar a imagem no centro
    img_x = 615
    img_y = 475

    # BTG Logo
    img = mpimg.imread(os.path.join(IMAGES_DIR, "btg.png"))
    plt.figimage(img, xo=img_x, yo=img_y, alpha=0.7)

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, "result.png"))
    return fig


def figures_to_readme() -> None:
    from data_reader import read_contour_file, multithreading_reader_dat_file
    from preprocess import apply_contour, transform_data

    contour = (
        read_contour_file(
            file_path="/home/viniciusparede/repositories/personal/btg-challenge/data/PSATCMG_CAMARGOS.bln"
        ),
    )[0]
    forecast = multithreading_reader_dat_file(folder_path=DATA_DIR)

    df = apply_contour(contour, forecast)

    df_transformed = transform_data(df)

    contour_figure(data=contour)
    apply_contour_figure(data=df)
    interpolation_figure(data=df_transformed)


if __name__ == "__main__":
    figures_to_readme()

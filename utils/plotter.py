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
]


def contour_figure(self, data: pd.DataFrame, file_name: str) -> Figure:
    fig, ax = plt.subplots()

    ax.plot(data["lat"], data["long"], color="#0A1E8C")
    ax.set_title("Bacia Rio do Grande")
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Longitude")

    fig.savefig(os.path.join(IMAGES_DIR, f"{file_name}.png"))
    return fig


def apply_contour_figure(data: pd.DataFrame) -> Figure:
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


def predict_figure(
    grid_x: np.ndarray, grid_y: np.ndarray, precipation_grid: np.ndarray, date: str
) -> Figure:
    rows = 2
    cols = 5

    # Limites de precipitação
    cbar_min = 0
    cbar_max = 100

    fig, axs = plt.subplots(nrows=rows, ncols=cols, figsize=(18, 5))
    for i in range(rows):
        for j in range(cols):
            ax = axs[i][j]

            # Plot dos resultados de predição
            contour = ax.contourf(
                grid_x, grid_y, precipation_grid, levels=20, cmap="Blues"
            )

            # Adicionar uma colorbar
            cbar = fig.colorbar(contour, ax=ax, label="Precipitação [mm]")
            cbar.set_clim(cbar_min, cbar_max)

            # Plotagem do polígono
            ax.plot(
                [p[0] for p in POLYGONAL_ORDER],
                [p[1] for p in POLYGONAL_ORDER],
                color="red",
            )

            # Ajustar os limites dos eixos
            ax.set_ylim(-22.4, -21.2)

            # Data de cada subplot
            ax.set_title(f"{date}")

    fig.savefig(os.path.join(IMAGES_DIR, "modelagem.png"))
    return fig


def result_figure(result: List[float]) -> Figure:
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
    from utils.data_reader import read_contour_file, multithreading_reader_dat_file
    from utils.preprocess import apply_contour
    from utils.predict import predict_precipitation


if __name__ == "__main__":
    figures_to_readme()

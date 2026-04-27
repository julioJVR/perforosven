import base64
import matplotlib.pyplot as plt
from io import BytesIO


def grafico_lineal(labels, valores, titulo=""):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(labels, valores, marker="o")
    ax.set_title(titulo)
    ax.grid(True)

    buffer = BytesIO()
    plt.tight_layout()
    fig.savefig(buffer, format="png")
    plt.close(fig)

    return base64.b64encode(buffer.getvalue()).decode("utf-8")

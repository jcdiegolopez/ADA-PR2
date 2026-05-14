import csv
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def load_data(path: str) -> dict:
    """Read results/times.csv into a dict of column-name -> list of values.

    Uses csv.DictReader (no pandas). Numeric columns are cast to float.
    """
    data = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key, val in row.items():
                if key not in data:
                    data[key] = []
                try:
                    data[key].append(float(val))
                except ValueError:
                    data[key].append(val)
    return data


def _average_by_n(data: dict, col: str) -> tuple:
    """Return (unique_ns, mean_per_n) for the given column."""
    ns = np.array(data["n"], dtype=float)
    vals = np.array(data[col], dtype=float)
    unique_ns = np.unique(ns)
    means = np.array([vals[ns == n].mean() for n in unique_ns])
    return unique_ns, means


def polynomial_regression(x, y, max_degree: int = 5) -> tuple:
    """Fit polynomials of degree 1..max_degree; pick the one with lowest RMSE.

    Returns (best_degree, coefficients, rmse).
    """
    best_degree, best_coeffs, best_rmse = 1, None, float("inf")
    max_degree = min(max_degree, len(x) - 1)
    for degree in range(1, max_degree + 1):
        coeffs = np.polyfit(x, y, degree)
        y_pred = np.polyval(coeffs, x)
        rmse = float(np.sqrt(np.mean((y - y_pred) ** 2)))
        if rmse < best_rmse:
            best_degree, best_coeffs, best_rmse = degree, coeffs, rmse
    return best_degree, best_coeffs, best_rmse


def plot_scatter(data: dict, output_path: str):
    """Log-log scatter of average operations per n for each algorithm.

    Saves a PNG with regression curves overlaid.
    """
    algorithms = {
        "DP":    ("steps_dp",    "blue",   "o"),
        "EDF":   ("steps_edf",   "orange", "s"),
        "HVF":   ("steps_hvf",   "red",    "^"),
        "RATIO": ("steps_ratio", "green",  "D"),
    }

    fig, ax = plt.subplots(figsize=(9, 6))

    for label, (col, color, marker) in algorithms.items():
        ns, means = _average_by_n(data, col)
        ax.loglog(ns, means, marker=marker, color=color, label=label,
                  linestyle="None", markersize=7)

        # regression curve on log-log data for a smoother fit
        log_ns = np.log(ns)
        log_means = np.log(means)
        degree, coeffs, _ = polynomial_regression(log_ns, log_means, max_degree=3)
        ns_fine = np.linspace(ns.min(), ns.max(), 300)
        log_fine = np.log(ns_fine)
        log_pred = np.polyval(coeffs, log_fine)
        ax.loglog(ns_fine, np.exp(log_pred), color=color, linestyle="--",
                  linewidth=1.2, alpha=0.7)

    ax.set_xlabel("Tamaño de entrada (n)")
    ax.set_ylabel("Operaciones básicas (promedio)")
    ax.set_title("Operaciones básicas: DP vs. Greedy")
    ax.legend()
    ax.grid(True, which="both", linestyle=":", linewidth=0.5)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Gráfica guardada: {output_path}")


def plot_quality(data: dict, output_path: str):
    """Plot greedy/DP quality ratio per n. Saves results/quality_plot.png."""
    greedy_variants = {
        "EDF":   ("ratio_edf",   "orange", "s"),
        "HVF":   ("ratio_hvf",   "red",    "^"),
        "RATIO": ("ratio_ratio", "green",  "D"),
    }

    fig, ax = plt.subplots(figsize=(9, 6))

    for label, (col, color, marker) in greedy_variants.items():
        ns, means = _average_by_n(data, col)
        ax.plot(ns, means, marker=marker, color=color, label=label,
                markersize=7, linewidth=1.5)

    ax.axhline(y=1.0, color="black", linestyle="--", linewidth=1.2,
               label="Óptimo DP")
    ax.set_xlabel("Tamaño de entrada (n)")
    ax.set_ylabel("val_greedy / val_dp")
    ax.set_title("Calidad de solución greedy vs. óptimo DP")
    ax.legend()
    ax.grid(True, linestyle=":", linewidth=0.5)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Gráfica guardada: {output_path}")


def generate_report(data: dict, output_path: str):
    """Write regression summary + quality averages to a plain-text file."""
    algorithms = [
        ("DP",    "steps_dp"),
        ("EDF",   "steps_edf"),
        ("HVF",   "steps_hvf"),
        ("RATIO", "steps_ratio"),
    ]
    quality_cols = {
        "EDF":   "ratio_edf",
        "HVF":   "ratio_hvf",
        "RATIO": "ratio_ratio",
    }

    lines = ["Reporte de regresión polinomial — Weighted Interval Scheduling", "=" * 60]

    for label, col in algorithms:
        ns, means = _average_by_n(data, col)
        degree, coeffs, rmse = polynomial_regression(ns, means)

        lines.append(f"\n[{label}]")
        lines.append(f"  Grado del polinomio de mejor ajuste : {degree}")
        coeffs_str = ", ".join(f"{c:.4e}" for c in coeffs)
        lines.append(f"  Coeficientes (mayor a menor grado)  : [{coeffs_str}]")
        lines.append(f"  RMSE                                : {rmse:.4e}")

        if label in quality_cols:
            avg_ratio = float(np.mean(data[quality_cols[label]]))
            lines.append(f"  Ratio de calidad promedio vs. DP    : {avg_ratio:.4f}")

    lines.append("\n" + "=" * 60)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Reporte guardado: {output_path}")


if __name__ == "__main__":
    data = load_data("results/times.csv")
    plot_scatter(data, "results/scatter_plot.png")
    plot_quality(data, "results/quality_plot.png")
    generate_report(data, "results/regression_report.txt")
    print("Análisis completo. Ver carpeta results/")

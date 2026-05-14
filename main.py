import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from src.models import Job
from src.dp import weighted_interval_dp
from src.greedy import greedy_edf, greedy_hvf


def _print_jobs_table(jobs: list):
    print(f"  {'ID':>4}  {'Start':>6}  {'Finish':>6}  {'Weight':>8}")
    print(f"  {'----':>4}  {'------':>6}  {'------':>6}  {'--------':>8}")
    for j in sorted(jobs, key=lambda x: x.job_id):
        print(f"  {j.job_id:>4}  {j.start:>6}  {j.finish:>6}  {j.weight:>8.1f}")


def _print_result(label: str, value: float, selected: list, dp_value: float):
    ids = [j.job_id for j in selected]
    ratio = value / dp_value if dp_value > 0 else 1.0
    print(f"\n--- {label} ---")
    print(f"  Valor obtenido  : {value}")
    print(f"  Jobs elegidos   : {ids}")
    if label != "Programación Dinámica (DP)":
        print(f"  Ratio vs optimo : {ratio:.4f}")


def main():
    print("=" * 62)
    print("  Weighted Interval Scheduling — Proyecto 2, ADA")
    print("  Diego López (23242)  ·  Diego Rosales (23258)")
    print("=" * 62)

    # Ejemplo del documento
    jobs = [
        Job(job_id=0, start=0, finish=3, weight=3),
        Job(job_id=1, start=1, finish=4, weight=5),
        Job(job_id=2, start=3, finish=6, weight=4),
        Job(job_id=3, start=2, finish=7, weight=6),
    ]

    print("\nEjemplo del documento (4 trabajos):")
    _print_jobs_table(jobs)

    dp_val,  dp_sel  = weighted_interval_dp(jobs)
    edf_val, edf_sel = greedy_edf(jobs)
    hvf_val, hvf_sel = greedy_hvf(jobs)

    _print_result("Programación Dinámica (DP)", dp_val,  dp_sel,  dp_val)
    _print_result("Greedy EDF",                 edf_val, edf_sel, dp_val)
    _print_result("Greedy HVF",                 hvf_val, hvf_sel, dp_val)

    # Benchmark opcional
    print()
    try:
        respuesta = input("¿Correr benchmark completo? Puede tardar varios minutos (s/n): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        respuesta = "n"

    if respuesta == "s":
        print("\nEjecutando benchmark...")
        from benchmark.runner import run_benchmark, export_csv
        results = run_benchmark()
        export_csv(results, "results/times.csv")
        print("  CSV guardado en results/times.csv")

        print("\nGenerando gráficas y reporte...")
        from benchmark.analysis import load_data, plot_scatter, plot_quality, generate_report
        data = load_data("results/times.csv")
        plot_scatter(data, "results/scatter_plot.png")
        plot_quality(data, "results/quality_plot.png")
        generate_report(data, "results/regression_report.txt")
        print("  Resultados en la carpeta results/")

    # Tests automáticos
    print("\n" + "=" * 62)
    print("  Tests automáticos")
    print("=" * 62)
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()

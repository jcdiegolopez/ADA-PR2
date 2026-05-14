import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import Job
from src.utils import generate_random_instance, latest_compatible

SIZES = [10, 50, 100, 250, 500, 1000, 2500, 5000, 10000]
REPETITIONS = 10


# --- Versiones instrumentadas (cuentan operaciones básicas) ---

def _dp_counted(jobs: list) -> tuple:
    """Retorna (valor, jobs_seleccionados, pasos)."""
    if not jobs:
        return 0.0, [], 0

    steps = 0
    sorted_jobs = sorted(jobs, key=lambda j: j.finish)
    n = len(sorted_jobs)

    p = [latest_compatible(sorted_jobs, i) for i in range(n)]

    dp_table = [0.0] * (n + 1)
    for i in range(1, n + 1):
        job = sorted_jobs[i - 1]
        include = job.weight + dp_table[p[i - 1] + 1]
        exclude = dp_table[i - 1]
        dp_table[i] = max(include, exclude)
        steps += 1  # una comparación include vs exclude por iteración

    selected = []
    i = n
    while i >= 1:
        job = sorted_jobs[i - 1]
        include_val = job.weight + dp_table[p[i - 1] + 1]
        if include_val >= dp_table[i - 1]:
            selected.append(job)
            i = p[i - 1] + 1
        else:
            i -= 1
        steps += 1  # una decisión por paso de backtracking

    return dp_table[n], sorted(selected, key=lambda j: j.start), steps


def _edf_counted(jobs: list) -> tuple:
    """Retorna (valor, jobs_seleccionados, pasos)."""
    if not jobs:
        return 0.0, [], 0

    steps = 0
    sorted_jobs = sorted(jobs, key=lambda j: j.finish)
    selected = []
    last_finish = 0

    for job in sorted_jobs:
        steps += 1  # comparación start >= last_finish
        if job.start >= last_finish:
            selected.append(job)
            last_finish = job.finish

    total = sum(j.weight for j in selected)
    return total, sorted(selected, key=lambda j: j.start), steps


def _hvf_counted(jobs: list) -> tuple:
    """Retorna (valor, jobs_seleccionados, pasos)."""
    if not jobs:
        return 0.0, [], 0

    steps = 0
    sorted_jobs = sorted(jobs, key=lambda j: j.weight, reverse=True)
    selected = []

    for job in sorted_jobs:
        for s in selected:
            steps += 1  # cada is_compatible es una operación básica
        if all(job.is_compatible(s) for s in selected):
            selected.append(job)

    total = sum(j.weight for j in selected)
    return total, sorted(selected, key=lambda j: j.start), steps


def _ratio_counted(jobs: list) -> tuple:
    """Retorna (valor, jobs_seleccionados, pasos)."""
    if not jobs:
        return 0.0, [], 0

    steps = 0
    sorted_jobs = sorted(
        jobs, key=lambda j: j.weight / (j.finish - j.start), reverse=True
    )
    selected = []

    for job in sorted_jobs:
        for s in selected:
            steps += 1
        if all(job.is_compatible(s) for s in selected):
            selected.append(job)

    total = sum(j.weight for j in selected)
    return total, sorted(selected, key=lambda j: j.start), steps


# --- Runner principal ---

def run_benchmark() -> list:
    results = []
    for size in SIZES:
        print(f"  n={size}...")
        for rep in range(REPETITIONS):
            jobs = generate_random_instance(size, seed=rep)

            val_dp, _, steps_dp = _dp_counted(jobs)
            val_edf, _, steps_edf = _edf_counted(jobs)
            val_hvf, _, steps_hvf = _hvf_counted(jobs)
            val_ratio, _, steps_ratio = _ratio_counted(jobs)

            results.append({
                "n": size,
                "rep": rep,
                "steps_dp": steps_dp,
                "steps_edf": steps_edf,
                "steps_hvf": steps_hvf,
                "steps_ratio": steps_ratio,
                "val_dp": val_dp,
                "val_edf": val_edf,
                "val_hvf": val_hvf,
                "val_ratio": val_ratio,
                "ratio_edf": round(val_edf / val_dp, 4) if val_dp > 0 else 1.0,
                "ratio_hvf": round(val_hvf / val_dp, 4) if val_dp > 0 else 1.0,
                "ratio_ratio": round(val_ratio / val_dp, 4) if val_dp > 0 else 1.0,
            })
    return results


def export_csv(results: list, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = [
        "n", "rep",
        "steps_dp", "steps_edf", "steps_hvf", "steps_ratio",
        "val_dp", "val_edf", "val_hvf", "val_ratio",
        "ratio_edf", "ratio_hvf", "ratio_ratio",
    ]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    print("Corriendo benchmark...")
    results = run_benchmark()
    export_csv(results, "results/times.csv")
    print("Benchmark completo. Ver results/times.csv")

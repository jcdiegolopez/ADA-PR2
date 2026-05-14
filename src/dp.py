from src.models import Job
from src.utils import latest_compatible


def weighted_interval_dp(jobs: list) -> tuple:
    """DP bottom-up para Weighted Interval Scheduling.

    Tiempo: O(n log n) — ordenamiento + n llamadas a búsqueda binaria.
    Espacio: O(n) — dp_table, arreglo p, lista de seleccionados.

    Args:
        jobs: lista de Job en cualquier orden (la lista original no se modifica)
    Returns:
        (peso_total, jobs_seleccionados) donde jobs_seleccionados está ordenado
        por start time y todos sus elementos son mutuamente compatibles
    """
    if not jobs:
        return (0.0, [])

    sorted_jobs = sorted(jobs, key=lambda j: j.finish)
    n = len(sorted_jobs)

    # p[i] = posición (índice 0-based) del último job compatible con sorted_jobs[i], o -1
    p = [latest_compatible(sorted_jobs, i) for i in range(n)]

    # dp_table[i] = peso óptimo considerando solo los primeros i jobs (indexado desde 1)
    dp_table = [0.0] * (n + 1)

    for i in range(1, n + 1):
        job = sorted_jobs[i - 1]
        include = job.weight + dp_table[p[i - 1] + 1]
        exclude = dp_table[i - 1]
        dp_table[i] = max(include, exclude)

    # Recuperación iterativa de la solución (evita stack overflow en n grande)
    selected = []
    i = n
    while i >= 1:
        job = sorted_jobs[i - 1]
        include_val = job.weight + dp_table[p[i - 1] + 1]
        if include_val >= dp_table[i - 1]:
            selected.append(job)
            # p[i-1] es 0-based; se suma 1 para convertir al espacio 1-based del bucle
            i = p[i - 1] + 1
        else:
            i -= 1

    return (dp_table[n], sorted(selected, key=lambda j: j.start))

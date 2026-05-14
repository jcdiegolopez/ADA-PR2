from src.models import Job


def greedy_edf(jobs: list) -> tuple:
    """Earliest Deadline First greedy for Weighted Interval Scheduling.

    O(n log n) tiempo, O(n) espacio.

    Args:
        jobs: Lista de Job en cualquier orden
    Returns:
        (peso_total, jobs_seleccionados) ordenados por start time
    """
    if not jobs:
        return (0.0, [])

    sorted_jobs = sorted(jobs, key=lambda j: j.finish)
    selected = []
    last_finish = 0

    for job in sorted_jobs:
        if job.start >= last_finish:
            selected.append(job)
            last_finish = job.finish

    total = sum(j.weight for j in selected)
    return (total, sorted(selected, key=lambda j: j.start))


def greedy_hvf(jobs: list) -> tuple:
    """Highest Value First greedy for Weighted Interval Scheduling.

    O(n^2) tiempo peor caso, O(n) espacio.

    Args:
        jobs: Lista de Job en cualquier orden
    Returns:
        (peso_total, jobs_seleccionados) ordenados por start time
    """
    if not jobs:
        return (0.0, [])

    sorted_jobs = sorted(jobs, key=lambda j: j.weight, reverse=True)
    selected = []

    for job in sorted_jobs:
        if all(job.is_compatible(s) for s in selected):
            selected.append(job)

    total = sum(j.weight for j in selected)
    return (total, sorted(selected, key=lambda j: j.start))


def greedy_ratio(jobs: list) -> tuple:
    """Weight/duration ratio greedy for Weighted Interval Scheduling.

    O(n^2) tiempo, O(n) espacio.

    Args:
        jobs: Lista de Job en cualquier orden
    Returns:
        (peso_total, jobs_seleccionados) ordenados por start time
    """
    if not jobs:
        return (0.0, [])

    sorted_jobs = sorted(
        jobs, key=lambda j: j.weight / (j.finish - j.start), reverse=True
    )
    selected = []

    for job in sorted_jobs:
        if all(job.is_compatible(s) for s in selected):
            selected.append(job)

    total = sum(j.weight for j in selected)
    return (total, sorted(selected, key=lambda j: j.start))

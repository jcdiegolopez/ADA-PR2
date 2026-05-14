import bisect
import random

from src.models import Job


def latest_compatible(jobs: list, j: int) -> int:
    """Return the largest index i < j where jobs[i].finish <= jobs[j].start.

    jobs must be sorted by finish time. Returns -1 if no compatible job exists.
    """
    finish_times = [job.finish for job in jobs]
    target = jobs[j].start
    idx = bisect.bisect_right(finish_times, target, 0, j) - 1
    return idx


def generate_random_instance(n: int, seed: int = 42) -> list:
    """Generate n random Jobs. List is NOT sorted (each algorithm sorts its own copy)."""
    random.seed(seed)
    jobs = []
    for i in range(n):
        start = random.randint(0, 1000)
        duration = random.randint(1, 100)
        finish = start + duration
        weight = random.randint(1, 100)
        jobs.append(Job(job_id=i, start=start, finish=finish, weight=weight))
    return jobs


def generate_worst_case_greedy(n: int) -> list:
    """Generate an instance where EDF clearly fails compared to DP.

    Pattern: n-1 small jobs packed tightly plus one high-weight job spanning them all.
    EDF picks all small jobs (total weight = n-1); DP picks the big job (weight = n).
    """
    jobs = []
    for i in range(n - 1):
        start = i * 2
        jobs.append(Job(job_id=i, start=start, finish=start + 2, weight=1))
    jobs.append(
        Job(job_id=n - 1, start=0, finish=(n - 1) * 2, weight=float(n))
    )
    return jobs

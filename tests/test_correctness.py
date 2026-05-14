import unittest

from src.models import Job
from src.utils import generate_random_instance
from src.dp import weighted_interval_dp


def brute_force(jobs: list) -> float:
    """Optimal solution by exhaustive search over all 2^n subsets. Only use for n <= 20."""
    n = len(jobs)
    best = 0.0
    for mask in range(1 << n):
        subset = [jobs[i] for i in range(n) if mask & (1 << i)]
        compatible = all(
            subset[i].is_compatible(subset[j])
            for i in range(len(subset))
            for j in range(i + 1, len(subset))
        )
        if compatible:
            best = max(best, sum(j.weight for j in subset))
    return best


class TestCorrectness(unittest.TestCase):

    def test_small_random(self):
        for seed in range(50):
            n = (seed % 14) + 2  # n in [2, 15]
            jobs = generate_random_instance(n, seed=seed)
            dp_value, _ = weighted_interval_dp(jobs)
            bf_value = brute_force(jobs)
            self.assertAlmostEqual(
                dp_value, bf_value, places=6,
                msg=f"Mismatch on seed={seed}, n={n}: dp={dp_value}, bf={bf_value}"
            )

    def test_known_example(self):
        jobs = [
            Job(job_id=0, start=0, finish=3, weight=3),
            Job(job_id=1, start=1, finish=4, weight=5),
            Job(job_id=2, start=3, finish=6, weight=4),
            Job(job_id=3, start=2, finish=7, weight=6),
        ]
        dp_value, selected = weighted_interval_dp(jobs)
        self.assertAlmostEqual(dp_value, 7.0, places=6)
        selected_ids = {j.job_id for j in selected}
        self.assertEqual(selected_ids, {0, 2})

    def test_no_overlap(self):
        jobs = [
            Job(job_id=i, start=i * 10, finish=i * 10 + 5, weight=float(i + 1))
            for i in range(8)
        ]
        dp_value, _ = weighted_interval_dp(jobs)
        self.assertAlmostEqual(dp_value, sum(j.weight for j in jobs), places=6)

    def test_all_overlap(self):
        jobs = [
            Job(job_id=i, start=0, finish=10, weight=float(i + 1))
            for i in range(6)
        ]
        dp_value, _ = weighted_interval_dp(jobs)
        self.assertAlmostEqual(dp_value, max(j.weight for j in jobs), places=6)


if __name__ == "__main__":
    unittest.main()

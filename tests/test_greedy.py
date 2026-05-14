import unittest

from src.models import Job
from src.dp import weighted_interval_dp
from src.greedy import greedy_edf, greedy_hvf, greedy_ratio


class TestGreedy(unittest.TestCase):

    def test_edf_counterexample(self):
        # EDF picks A and C (cheapest), DP picks B (most valuable)
        # A:w=1, B:w=10, C:w=1
        # B overlaps both A and C; A and C are compatible
        jobs = [
            Job(0, start=0, finish=3, weight=1),   # A
            Job(1, start=1, finish=10, weight=10),  # B
            Job(2, start=4, finish=7, weight=1),   # C
        ]
        edf_val, _ = greedy_edf(jobs)
        dp_val, _ = weighted_interval_dp(jobs)
        self.assertLess(edf_val, dp_val)
        self.assertEqual(edf_val, 2)
        self.assertEqual(dp_val, 10)

    def test_hvf_counterexample(self):
        # HVF picks A (highest weight=11), misses B+C=12
        # A:w=11, B:w=6, C:w=6
        # A overlaps B and C; B and C are compatible
        jobs = [
            Job(0, start=1, finish=9, weight=11),   # A
            Job(1, start=0, finish=5, weight=6),    # B
            Job(2, start=6, finish=10, weight=6),   # C
        ]
        hvf_val, _ = greedy_hvf(jobs)
        dp_val, _ = weighted_interval_dp(jobs)
        self.assertLess(hvf_val, dp_val)
        self.assertEqual(hvf_val, 11)
        self.assertEqual(dp_val, 12)

    def test_no_overlap_edf(self):
        jobs = [
            Job(0, start=0, finish=2, weight=3),
            Job(1, start=3, finish=5, weight=7),
            Job(2, start=6, finish=9, weight=4),
        ]
        edf_val, _ = greedy_edf(jobs)
        dp_val, _ = weighted_interval_dp(jobs)
        self.assertEqual(edf_val, dp_val)
        self.assertEqual(edf_val, sum(j.weight for j in jobs))

    def test_edf_compatible_output(self):
        from src.utils import generate_random_instance
        jobs = generate_random_instance(20, seed=7)
        _, selected = greedy_edf(jobs)
        for i in range(len(selected)):
            for k in range(i + 1, len(selected)):
                self.assertTrue(selected[i].is_compatible(selected[k]))

    def test_hvf_compatible_output(self):
        from src.utils import generate_random_instance
        jobs = generate_random_instance(20, seed=7)
        _, selected = greedy_hvf(jobs)
        for i in range(len(selected)):
            for k in range(i + 1, len(selected)):
                self.assertTrue(selected[i].is_compatible(selected[k]))

    def test_empty(self):
        self.assertEqual(greedy_edf([]), (0.0, []))
        self.assertEqual(greedy_hvf([]), (0.0, []))
        self.assertEqual(greedy_ratio([]), (0.0, []))


if __name__ == "__main__":
    unittest.main()

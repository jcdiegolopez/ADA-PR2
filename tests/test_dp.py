import unittest

from src.models import Job
from src.utils import latest_compatible
from src.dp import weighted_interval_dp


class TestDP(unittest.TestCase):

    def test_p_array(self):
        # Jobs sorted by finish: [0,2), [1,3), [2,5), [4,7)
        jobs = [
            Job(job_id=0, start=0, finish=2, weight=1),
            Job(job_id=1, start=1, finish=3, weight=1),
            Job(job_id=2, start=2, finish=5, weight=1),
            Job(job_id=3, start=4, finish=7, weight=1),
        ]
        # latest_compatible(jobs, 0): no job before index 0 -> -1
        self.assertEqual(latest_compatible(jobs, 0), -1)
        # latest_compatible(jobs, 1): jobs[0].finish=2 > jobs[1].start=1 -> -1
        self.assertEqual(latest_compatible(jobs, 1), -1)
        # latest_compatible(jobs, 2): jobs[0].finish=2 <= jobs[2].start=2 -> 0
        self.assertEqual(latest_compatible(jobs, 2), 0)
        # latest_compatible(jobs, 3): jobs[2].finish=5 > jobs[3].start=4,
        #   jobs[1].finish=3 <= jobs[3].start=4 -> 1
        self.assertEqual(latest_compatible(jobs, 3), 1)

    def test_backtrack(self):
        jobs = [
            Job(job_id=0, start=0, finish=3, weight=3),
            Job(job_id=1, start=1, finish=4, weight=5),
            Job(job_id=2, start=3, finish=6, weight=4),
            Job(job_id=3, start=2, finish=7, weight=6),
        ]
        dp_value, selected = weighted_interval_dp(jobs)
        # Selected jobs must be mutually compatible
        for i in range(len(selected)):
            for j in range(i + 1, len(selected)):
                self.assertTrue(
                    selected[i].is_compatible(selected[j]),
                    msg=f"Jobs {selected[i]} and {selected[j]} are not compatible"
                )
        # Sum of selected weights must equal dp_value
        self.assertAlmostEqual(
            sum(j.weight for j in selected), dp_value, places=6
        )

    def test_empty_input(self):
        value, selected = weighted_interval_dp([])
        self.assertAlmostEqual(value, 0.0, places=6)
        self.assertEqual(selected, [])

    def test_single_job(self):
        job = Job(job_id=0, start=1, finish=5, weight=42.0)
        value, selected = weighted_interval_dp([job])
        self.assertAlmostEqual(value, 42.0, places=6)
        self.assertEqual(selected, [job])


if __name__ == "__main__":
    unittest.main()

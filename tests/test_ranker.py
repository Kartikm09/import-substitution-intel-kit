import unittest

from import_intel.ranker import Candidate, rank_candidates


class ImportIntelTests(unittest.TestCase):
    def test_high_capability_candidate_ranks_first(self):
        candidates = [
            Candidate("Hard regulated", "x", "China", 100, 3, 8, 9, 9, 9),
            Candidate("Simple product", "y", "China", 30, 9, 8, 3, 7, 2),
        ]
        ranked = rank_candidates(candidates)
        self.assertEqual(ranked[0].product, "Simple product")
        self.assertEqual(ranked[0].status, "research-now")
        self.assertTrue(ranked[0].next_actions)


if __name__ == "__main__":
    unittest.main()


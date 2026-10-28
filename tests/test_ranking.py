import unittest

from ranking import combine_scores, interest_scoring


class RankingTests(unittest.TestCase):
    def test_interest_scoring_returns_full_score_when_no_filter_is_selected(self):
        self.assertEqual(interest_scoring([], [1, 2]), 1.0)

    def test_interest_scoring_counts_matches_without_mutating_inputs(self):
        selected = [3, 1]
        club_tags = [2, 3, 1]

        self.assertEqual(interest_scoring(selected, club_tags), 1.0)
        self.assertEqual(selected, [3, 1])
        self.assertEqual(club_tags, [2, 3, 1])

    def test_combine_scores_uses_documented_weights(self):
        self.assertAlmostEqual(combine_scores(0.8, 0.5), 0.71)

    def test_combine_scores_rejects_invalid_weights(self):
        for weight in (-0.1, 1.1):
            with self.subTest(weight=weight):
                with self.assertRaises(ValueError):
                    combine_scores(0.8, 0.5, semantic_weight=weight)


if __name__ == "__main__":
    unittest.main()

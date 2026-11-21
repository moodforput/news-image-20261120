import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from news_image.news import DATE, STORIES


class TestNews(unittest.TestCase):
    def test_date_is_20_november_2026(self):
        self.assertEqual(DATE, "20 NOVEMBER 2026")

    def test_six_stories(self):
        self.assertEqual(len(STORIES), 6)

    def test_each_story_has_headline_body_icon(self):
        for story in STORIES:
            self.assertTrue(story["headline"])
            self.assertTrue(story["body"])
            self.assertTrue(story["icon"])
            self.assertTrue(story["accent"])

    def test_headline_lines_are_short(self):
        for story in STORIES:
            self.assertLessEqual(len(story["headline"]), 2)
            for line in story["headline"]:
                self.assertLessEqual(len(line), 22, line)

    def test_body_lines_are_short(self):
        for story in STORIES:
            self.assertLessEqual(len(story["body"]), 2)
            for line in story["body"]:
                self.assertLessEqual(len(line), 26, line)

    def test_no_other_dates_in_text(self):
        all_text = " ".join(
            line for story in STORIES for line in story["headline"] + story["body"]
        )
        for bad in ("19 NOV", "19 NOVEMBER", "21 NOV", "18 NOV", "2017", "2025"):
            self.assertNotIn(bad, all_text)

    def test_gta_labelled_as_announced_not_released(self):
        gta = STORIES[5]
        joined = " ".join(gta["headline"] + gta["body"])
        self.assertIn("ANNOUNCED", joined)
        self.assertNotIn("RELEASED", joined)
        self.assertIn("$3.79BN", joined)
        self.assertIn("32.5M", joined)

    def test_no_hype_words(self):
        all_text = " ".join(
            line for story in STORIES for line in story["headline"] + story["body"]
        ).upper()
        for word in ("AMAZING", "INCREDIBLE", "SHOCKING", "BEST EVER", "HUGE"):
            self.assertNotIn(word, all_text)

    def test_facts_present(self):
        joined = " ".join(
            line for story in STORIES for line in story["headline"] + story["body"]
        )
        for fragment in ("MYANMAR", "KYIV", "POLAND", "SHENZHEN", "COP31", "-3.7%", "-5.06%"):
            self.assertIn(fragment, joined)


if __name__ == "__main__":
    unittest.main()

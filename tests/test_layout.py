import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from news_image.layout import (
    IMAGE_SIZE,
    masthead_boxes,
    panel_rects,
    wrap_text,
)
from news_image.news import STORIES


def rects_overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax + aw <= bx or bx + bw <= ax or ay + ah <= by or by + bh <= ay)


class TestLayout(unittest.TestCase):
    def test_image_size_is_1024(self):
        self.assertEqual(IMAGE_SIZE, 1024)

    def test_six_panels_no_overlap(self):
        rects = panel_rects()
        self.assertEqual(len(rects), 6)
        for rect in rects:
            x, y, w, h = rect
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(x + w, 1024)
            self.assertLessEqual(y + h, 1024)
        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                self.assertFalse(rects_overlap(rects[i], rects[j]), (i, j))

    def test_panels_in_two_by_three_grid(self):
        rects = panel_rects()
        rows = [sorted({r[1] for r in rects})]
        self.assertEqual(len(rows[0]), 3)
        cols = sorted({r[0] for r in rects})
        self.assertEqual(len(cols), 2)

    def test_masthead_boxes_inside_image(self):
        for box in masthead_boxes():
            x, y, w, h = box
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(x + w, 1024)
            self.assertLessEqual(y + h, 220)

    def test_wrap_text_respects_limit(self):
        lines = wrap_text("ONE TWO THREE FOUR FIVE SIX", 10)
        for line in lines:
            self.assertLessEqual(len(line), 10)

    def test_all_story_text_fits_panel(self):
        rects = panel_rects()
        for story, rect in zip(STORIES, rects):
            _, _, panel_w, _ = rect
            from news_image.font import text_width

            for line in story["headline"]:
                self.assertLessEqual(text_width(line, 4), panel_w - 168, line)
            for line in story["body"]:
                self.assertLessEqual(text_width(line, 4), panel_w - 32, line)


if __name__ == "__main__":
    unittest.main()

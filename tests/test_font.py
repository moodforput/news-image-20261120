import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from news_image.canvas import Canvas
from news_image.font import GLYPHS, draw_text, text_width

USED_TEXT = (
    "FRIDAY - 20 NOVEMBER 2026 THE WORLD IN ONE DAY "
    "MYANMAR GENOCIDE RULING ICJ FINDS MYANMAR RESPONSIBLE "
    "KYIV UNDER ATTACK RUSSIAN MISSILES HIT POLAND TOO "
    "SHENZHEN SUMMIT TRUMP, XI, PUTIN JOINT DECLARATION "
    "COP31 DROPS FOSSIL FUELS CLIMATE DEAL OMITS THE WORDS "
    "STOCKS FALL US STOCKS -3.7% NIKKEI -5.06% IN AI ROUT "
    "GTA 6: $3.79BN DAY ONE 32.5M COPIES SALES ANNOUNCED 20 NOV "
    "WORLD NEWS 0123456789.,:%$/() "
)


class TestFont(unittest.TestCase):
    def test_glyph_shape_is_5_by_7(self):
        for char, rows in GLYPHS.items():
            self.assertEqual(len(rows), 7, char)
            for row in rows:
                self.assertEqual(len(row), 5, char)
                self.assertTrue(set(row) <= {"0", "1"}, char)

    def test_all_used_chars_have_glyphs(self):
        missing = sorted(set(USED_TEXT) - set(GLYPHS))
        self.assertEqual(missing, [])

    def test_text_width_scales(self):
        self.assertEqual(text_width("A", 1), 5)
        self.assertEqual(text_width("A", 2), 10)
        self.assertEqual(text_width("AB", 2), 22)
        self.assertEqual(text_width("A B", 3), 3 * 5 + 3 * 1 + 3 * 5 + 3 * 1 + 3 * 5)

    def test_draw_text_marks_pixels(self):
        canvas = Canvas(100, 30)
        canvas.fill((255, 255, 255))
        draw_text(canvas, 2, 2, "A", (0, 0, 0), 3)
        dark = sum(1 for y in range(30) for x in range(100) if canvas.get_pixel(x, y) == (0, 0, 0))
        self.assertGreater(dark, 20)

    def test_draw_text_clips_at_edge(self):
        canvas = Canvas(20, 20)
        canvas.fill((255, 255, 255))
        draw_text(canvas, 15, 15, "WIDE", (0, 0, 0), 4)
        self.assertEqual(canvas.width, 20)

    def test_digits_render(self):
        for digit in "0123456789":
            canvas = Canvas(30, 30)
            canvas.fill((255, 255, 255))
            draw_text(canvas, 2, 2, digit, (0, 0, 0), 2)
            dark = sum(1 for y in range(30) for x in range(30) if canvas.get_pixel(x, y) == (0, 0, 0))
            self.assertGreater(dark, 5, digit)


if __name__ == "__main__":
    unittest.main()

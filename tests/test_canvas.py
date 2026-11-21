import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from news_image.canvas import Canvas


class TestCanvas(unittest.TestCase):
    def test_fill_and_pixel(self):
        canvas = Canvas(10, 10)
        canvas.fill((7, 8, 9))
        self.assertEqual(canvas.get_pixel(0, 0), (7, 8, 9))
        self.assertEqual(canvas.get_pixel(9, 9), (7, 8, 9))

    def test_fill_rect_inside_and_clipped(self):
        canvas = Canvas(10, 10)
        canvas.fill((255, 255, 255))
        canvas.fill_rect(2, 2, 4, 3, (255, 0, 0))
        self.assertEqual(canvas.get_pixel(2, 2), (255, 0, 0))
        self.assertEqual(canvas.get_pixel(5, 4), (255, 0, 0))
        self.assertEqual(canvas.get_pixel(6, 5), (255, 255, 255))
        canvas.fill_rect(-2, -2, 5, 5, (0, 0, 255))
        self.assertEqual(canvas.get_pixel(0, 0), (0, 0, 255))

    def test_circle_draws_centre(self):
        canvas = Canvas(21, 21)
        canvas.fill((255, 255, 255))
        canvas.circle(10, 10, 5, (0, 0, 0))
        self.assertEqual(canvas.get_pixel(10, 10), (0, 0, 0))
        self.assertEqual(canvas.get_pixel(10, 5), (0, 0, 0))
        self.assertEqual(canvas.get_pixel(0, 0), (255, 255, 255))

    def test_line_draws_diagonal(self):
        canvas = Canvas(10, 10)
        canvas.fill((255, 255, 255))
        canvas.line(0, 0, 9, 9, (0, 0, 0))
        self.assertEqual(canvas.get_pixel(0, 0), (0, 0, 0))
        self.assertEqual(canvas.get_pixel(5, 5), (0, 0, 0))
        self.assertEqual(canvas.get_pixel(9, 9), (0, 0, 0))

    def test_polygon_fills_triangle(self):
        canvas = Canvas(20, 20)
        canvas.fill((255, 255, 255))
        canvas.polygon([(5, 5), (15, 5), (10, 15)], (0, 128, 0))
        self.assertEqual(canvas.get_pixel(10, 8), (0, 128, 0))
        self.assertEqual(canvas.get_pixel(0, 0), (255, 255, 255))

    def test_to_bytes_length(self):
        canvas = Canvas(3, 2)
        self.assertEqual(len(canvas.to_bytes()), 3 * 2 * 3)


if __name__ == "__main__":
    unittest.main()

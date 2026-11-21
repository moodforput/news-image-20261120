import os
import struct
import sys
import unittest
import zlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from news_image.png import encode_png


class TestPng(unittest.TestCase):
    def test_signature_and_ihdr(self):
        data = encode_png(4, 3, bytes([255, 0, 0] * 12))
        self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(struct.unpack(">I", data[8:12])[0], 13)
        self.assertEqual(data[12:16], b"IHDR")
        width, height, depth, ctype, comp, filt, inter = struct.unpack(
            ">IIBBBBB", data[16:29]
        )
        self.assertEqual((width, height), (4, 3))
        self.assertEqual(depth, 8)
        self.assertEqual(ctype, 2)
        self.assertEqual(inter, 0)

    def test_crc_valid_for_every_chunk(self):
        data = encode_png(2, 2, bytes([0, 0, 0] * 4))
        pos = 8
        while pos < len(data):
            length = struct.unpack(">I", data[pos:pos + 4])[0]
            ctype = data[pos + 4:pos + 8]
            chunk_data = data[pos + 8:pos + 8 + length]
            stored = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
            self.assertEqual(zlib.crc32(ctype + chunk_data) & 0xFFFFFFFF, stored)
            pos += 12 + length
        self.assertEqual(data[-8:-4], b"IEND")

    def test_deterministic_bytes(self):
        pixels = bytes(range(256)) * 3
        first = encode_png(8, 8, bytes([10, 20, 30] * 64))
        second = encode_png(8, 8, bytes([10, 20, 30] * 64))
        self.assertEqual(first, second)
        self.assertEqual(len(pixels), 768)

    def test_wrong_pixel_length_rejected(self):
        with self.assertRaises(ValueError):
            encode_png(2, 2, bytes([0] * 10))

    def test_1024_image_encodes(self):
        pixels = bytes([247, 243, 232] * 1024 * 1024)
        data = encode_png(1024, 1024, pixels)
        self.assertLessEqual(len(data), 1048576)
        self.assertGreater(len(data), 100)


if __name__ == "__main__":
    unittest.main()

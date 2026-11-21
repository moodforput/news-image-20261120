import hashlib
import os
import struct
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")


def _read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


class TestIntegration(unittest.TestCase):
    def _run_main(self, out_dir):
        env = dict(os.environ)
        env["MAKEFUN_OUTPUT_DIR"] = out_dir
        result = subprocess.run(
            [sys.executable, os.path.join(ROOT, "main.py")],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return os.path.join(out_dir, "entry.png")

    def test_main_writes_valid_1024_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._run_main(tmp)
            self.assertTrue(os.path.exists(path))
            data = _read_bytes(path)
            self.assertLessEqual(len(data), 1048576)
            self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))
            width, height = struct.unpack(">II", data[16:24])
            self.assertEqual((width, height), (1024, 1024))
            mode = os.stat(path).st_mode & 0o777
            self.assertEqual(mode, 0o644)

    def test_two_runs_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_path = self._run_main(first)
            second_path = self._run_main(second)
            first_hash = hashlib.sha256(_read_bytes(first_path)).hexdigest()
            second_hash = hashlib.sha256(_read_bytes(second_path)).hexdigest()
            self.assertEqual(first_hash, second_hash)

    def test_output_is_not_starter_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._run_main(tmp)
            data = _read_bytes(path)
            starter = os.path.join(
                os.path.dirname(__file__), "..", "..",
                "news-image-20261120-kit", "starter", "entry.png",
            )
            if os.path.exists(starter):
                self.assertNotEqual(data, _read_bytes(starter))


if __name__ == "__main__":
    unittest.main()

"""Entry point for the make.fun bounty news-image-20261120.

Writes one image to /output/entry.png, or to the directory named by
MAKEFUN_OUTPUT_DIR outside the grader. Standard library only.
"""

import os
import stat

from news_image.render import render_png_bytes

OUTPUT_NAME = "entry.png"


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    data = render_png_bytes()
    path = os.path.join(output_dir, OUTPUT_NAME)
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()

# The World in One Day — 20 November 2026

A program that writes one image summing up the world news of Friday
20 November 2026, for the make.fun bounty `news-image-20261120`.

## What it makes

A 1024 by 1024 PNG newspaper front page, `entry.png`, with the date
`FRIDAY - 20 NOVEMBER 2026` in the masthead and six stories in a
2 by 3 grid:

1. ICJ finds Myanmar responsible for genocide against the Rohingya.
2. Russia attacks Kyiv overnight; Russian missiles fall in Poland.
3. US, China and Russia issue a joint declaration at Shenzhen.
4. The COP31 final document drops all references to fossil fuels.
5. Global markets slide: US stocks down 3.7%, Nikkei down 5.06%.
6. GTA 6 day-one sales announced: $3.79 billion, 32.5 million copies.

The image is drawn entirely in code with the Python standard library.
There are no downloaded images, no fonts on disk, and no network
access at run time.

## Setup

Python 3.13 is required. There are no dependencies to install.

```sh
python3 --version
```

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes `out/entry.png` (1024 by 1024, under 1 MiB, mode 0644).
Running it twice writes byte-identical files.

## Test

```sh
python3 -m unittest discover -s tests -v
```

The suite has 35 tests: PNG encoding, canvas drawing, the bitmap
font, the news data, the layout geometry, and an end-to-end run of
`main.py` that checks the output file, its dimensions, its size,
its file mode, and that two runs are byte-identical.

## Layout

- `main.py` — entry point only. It reads `MAKEFUN_OUTPUT_DIR`
  (or `/output`) and writes `entry.png`.
- `news_image/news.py` — the six stories and the date.
- `news_image/canvas.py` — the RGB canvas and shape drawing.
- `news_image/font.py` — the 5 by 7 bitmap font.
- `news_image/png.py` — the deterministic PNG encoder.
- `news_image/icons.py` — the six flat pictograms.
- `news_image/layout.py` — the masthead and grid geometry.
- `news_image/render.py` — assembles the front page.
- `tests/` — the unit and integration tests.

## Submission notes

This repository is the entry program only. It is not a submission
yet. To submit it to make.fun:

1. Create a public GitHub repository after the competition opened,
   with an MIT license, and push this code to it.
2. In the make.fun kit, run the kit `init` step with your keypair
   to write `.makefun/freshness.json` and the owner claim.
3. Submit with the kit CLI, naming the repository, the commit,
   and the transcript bundle of the sessions that built it.
4. Do not put a keypair, an API key, or any credential in the
   repository. The owner claim names a wallet address only.

The GTA 6 figures were announced on 20 November 2026, after the
game was released on 19 November, so the image says ANNOUNCED
and never says the game was released on 20 November.

"""Deterministic PNG encoder, standard library only.

Encodes RGB pixel data as a non-interlaced PNG with 8-bit colour depth,
colour type 2, filter 0 on every scanline, and zlib level 9. The output
depends only on the input pixels, so the same pixels always give the
same bytes.
"""

import struct
import zlib


def _chunk(chunk_type, data):
    body = chunk_type + data
    return struct.pack(">I", len(data)) + body + struct.pack(
        ">I", zlib.crc32(body) & 0xFFFFFFFF
    )


def encode_png(width, height, pixels):
    """Encode RGB pixels to PNG bytes.

    Pixels must be exactly width * height * 3 bytes in row-major order.
    """
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    if len(pixels) != width * height * 3:
        raise ValueError("pixel data has the wrong length")
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw.extend(pixels[y * stride:(y + 1) * stride])
    idat = zlib.compress(bytes(raw), 9)
    return (
        signature
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"IDAT", idat)
        + _chunk(b"IEND", b"")
    )

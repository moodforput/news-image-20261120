"""Flat vector pictograms, drawn only with canvas shapes.

Each icon is drawn inside a square of the given size at (x, y) using
the story accent colour on a light disc. No faces and no photographs.
"""

from news_image.canvas import Canvas

INK = (17, 24, 39)
PAPER = (247, 243, 232)
WHITE = (255, 255, 255)


def _disc(canvas, x, y, size, accent):
    cx = x + size // 2
    cy = y + size // 2
    canvas.circle(cx, cy, size // 2, (226, 232, 240))
    canvas.ring(cx, cy, size // 2, 4, accent)


def draw_scales(canvas, x, y, size, accent):
    _disc(canvas, x, y, size, accent)
    cx = x + size // 2
    top = y + size // 5
    canvas.line(cx, top, cx, y + size * 4 // 5, INK, 5)
    canvas.line(x + size // 5, top + 6, x + size * 4 // 5, top + 6, INK, 5)
    canvas.polygon(
        [(x + size // 5 - 14, top + 34), (x + size // 5 + 14, top + 34), (x + size // 5, top + 12)],
        accent,
    )
    canvas.polygon(
        [(x + size * 4 // 5 - 14, top + 34), (x + size * 4 // 5 + 14, top + 34), (x + size * 4 // 5, top + 12)],
        accent,
    )
    canvas.fill_rect(cx - 16, y + size * 4 // 5, 32, 6, INK)


def draw_missile(canvas, x, y, size, accent):
    _disc(canvas, x, y, size, accent)
    cx = x + size // 2
    cy = y + size // 2
    canvas.polygon(
        [(cx + 30, cy - 34), (cx + 44, cy - 8), (cx + 18, cy - 14)],
        accent,
    )
    canvas.line(cx - 34, cy + 28, cx + 22, cy - 22, INK, 7)
    for dx, dy in ((-38, -6), (-28, 14), (-44, 18), (-18, -34), (6, -40)):
        canvas.circle(cx + dx, cy + dy, 5, (245, 158, 11))


def draw_flags(canvas, x, y, size, accent):
    _disc(canvas, x, y, size, accent)
    base = y + size * 3 // 4
    canvas.fill_rect(x + size // 5, base, size * 3 // 5, 6, INK)
    colours = [(185, 28, 28), (30, 64, 175), (15, 118, 110)]
    for i, colour in enumerate(colours):
        fx = x + size // 5 + i * (size // 5 + 8)
        canvas.line(fx, base, fx, y + size // 5, INK, 4)
        canvas.fill_rect(fx + 4, y + size // 5, 30, 22, colour)


def draw_climate(canvas, x, y, size, accent):
    _disc(canvas, x, y, size, accent)
    cx = x + size // 2
    cy = y + size // 2
    canvas.circle(cx, cy, 30, (147, 197, 253))
    canvas.polygon([(cx - 22, cy - 6), (cx - 2, cy - 22), (cx + 10, cy + 2), (cx - 8, cy + 18)], (34, 197, 94))
    canvas.polygon([(cx + 4, cy + 22), (cx + 22, cy + 6), (cx + 26, cy + 22)], (34, 197, 94))
    canvas.line(cx - 34, cy + 34, cx + 34, cy - 34, (185, 28, 28), 6)


def draw_chart(canvas, x, y, size, accent):
    _disc(canvas, x, y, size, accent)
    ox = x + size // 5
    oy = y + size * 4 // 5
    canvas.line(ox, y + size // 5, ox, oy, INK, 4)
    canvas.line(ox, oy, x + size * 4 // 5, oy, INK, 4)
    points = [(ox + 6, y + 34), (ox + 30, y + 46), (ox + 54, y + 40), (ox + 78, y + 62), (ox + 100, y + 78)]
    for i in range(len(points) - 1):
        canvas.line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], accent, 6)
    canvas.polygon(
        [(points[-1][0] - 12, points[-1][1] - 2), (points[-1][0] + 10, points[-1][1] - 2), (points[-1][0], points[-1][1] + 14)],
        accent,
    )


def draw_controller(canvas, x, y, size, accent):
    _disc(canvas, x, y, size, accent)
    cx = x + size // 2
    cy = y + size // 2
    canvas.fill_rect(cx - 32, cy - 16, 64, 32, INK)
    canvas.circle(cx - 32, cy, 16, INK)
    canvas.circle(cx + 32, cy, 16, INK)
    canvas.fill_rect(cx - 22, cy - 3, 14, 6, WHITE)
    canvas.fill_rect(cx - 18, cy - 8, 5, 16, WHITE)
    canvas.circle(cx + 18, cy - 6, 4, accent)
    canvas.circle(cx + 26, cy + 2, 4, accent)
    canvas.circle(cx + 10, cy + 2, 4, (245, 158, 11))


ICONS = {
    "scales": draw_scales,
    "missile": draw_missile,
    "flags": draw_flags,
    "climate": draw_climate,
    "chart": draw_chart,
    "controller": draw_controller,
}


def draw_icon(canvas, name, x, y, size, accent):
    func = ICONS.get(name)
    if func is None:
        raise ValueError("unknown icon: " + name)
    func(canvas, x, y, size, accent)

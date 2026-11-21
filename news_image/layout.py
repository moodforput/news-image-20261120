"""Geometry for the 1024x1024 newspaper front page.

Masthead at the top, then a 2 column by 3 row grid. Every rect is
computed from constants, so panels never overlap and every text box
stays inside its panel.
"""

IMAGE_SIZE = 1024
MARGIN = 24
GUTTER = 20
MASTHEAD_HEIGHT = 212
PANEL_HEIGHT = 246


def panel_rects():
    """Return six (x, y, width, height) rects in story order."""
    grid_top = MASTHEAD_HEIGHT + 16
    grid_width = IMAGE_SIZE - 2 * MARGIN
    panel_width = (grid_width - GUTTER) // 2
    rects = []
    for row in range(3):
        for col in range(2):
            x = MARGIN + col * (panel_width + GUTTER)
            y = grid_top + row * (PANEL_HEIGHT + GUTTER)
            rects.append((x, y, panel_width, PANEL_HEIGHT))
    return rects


def masthead_boxes():
    """Return the masthead text boxes as (x, y, width, height)."""
    return [
        (MARGIN, 18, IMAGE_SIZE - 2 * MARGIN, 42),
        (MARGIN, 62, IMAGE_SIZE - 2 * MARGIN, 56),
        (MARGIN, 128, IMAGE_SIZE - 2 * MARGIN, 40),
    ]


def wrap_text(text, max_chars):
    """Wrap text to lines of at most max_chars, splitting on spaces."""
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= max_chars:
            current = current + " " + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

"""Assemble the 1024x1024 front page and encode it as PNG bytes."""

from news_image.canvas import Canvas
from news_image.font import draw_text, draw_text_centred, text_width
from news_image.icons import draw_icon
from news_image.layout import IMAGE_SIZE, panel_rects
from news_image.news import DATE, DAY_LINE, STORIES, TITLE
from news_image.png import encode_png

PAPER = (247, 243, 232)
INK = (17, 24, 39)
RED = (185, 28, 28)
WHITE = (255, 255, 255)
PANEL_BG = (255, 255, 255)
MUTED = (75, 85, 99)


def build_canvas():
    canvas = Canvas(IMAGE_SIZE, IMAGE_SIZE)
    canvas.fill(PAPER)
    _draw_masthead(canvas)
    _draw_panels(canvas)
    return canvas


def _draw_masthead(canvas):
    draw_text_centred(canvas, IMAGE_SIZE // 2, 20, TITLE, INK, 5)
    draw_text_centred(canvas, IMAGE_SIZE // 2, 66, DAY_LINE, INK, 6)
    canvas.fill_rect(24, 132, IMAGE_SIZE - 48, 6, RED)
    footer = "SIX STORIES - ONE DAY - READ IT IN ONE IMAGE"
    draw_text_centred(canvas, IMAGE_SIZE // 2, 152, footer, MUTED, 3)
    canvas.fill_rect(24, 200, IMAGE_SIZE - 48, 3, INK)


def _draw_panels(canvas):
    for story, rect in zip(STORIES, panel_rects()):
        _draw_panel(canvas, story, rect)


def _draw_panel(canvas, story, rect):
    x, y, width, height = rect
    canvas.fill_rect(x, y, width, height, PANEL_BG)
    canvas.fill_rect(x, y, width, 8, story["accent"])
    canvas.fill_rect(x, y, 4, height, story["accent"])
    canvas.fill_rect(x + width - 4, y, 4, height, story["accent"])
    canvas.fill_rect(x, y + height - 4, width, 4, story["accent"])
    icon_size = 108
    icon_x = x + 20
    icon_y = y + 24
    draw_icon(canvas, story["icon"], icon_x, icon_y, icon_size, story["accent"])
    text_x = icon_x + icon_size + 20
    text_y = icon_y + 12
    for i, line in enumerate(story["headline"]):
        if line:
            draw_text(canvas, text_x, text_y + i * 32, line, story["accent"], 4)
    body_y = y + 152
    canvas.fill_rect(x + 20, body_y - 10, width - 40, 2, (226, 232, 240))
    for i, line in enumerate(story["body"]):
        draw_text(canvas, x + 20, body_y + i * 32, line, INK, 4)
    number = str(STORIES.index(story) + 1)
    draw_text(canvas, x + width - 36, y + 20, number, story["accent"], 3)


def render_png_bytes():
    canvas = build_canvas()
    return encode_png(canvas.width, canvas.height, canvas.to_bytes())

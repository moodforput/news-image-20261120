"""A simple RGB canvas backed by a bytearray.

All drawing is done with integer arithmetic so the result is identical
on every run and on every machine.
"""


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = bytearray(width * height * 3)

    def fill(self, color):
        r, g, b = color
        for i in range(0, len(self.pixels), 3):
            self.pixels[i] = r
            self.pixels[i + 1] = g
            self.pixels[i + 2] = b

    def set_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            offset = (y * self.width + x) * 3
            self.pixels[offset] = color[0]
            self.pixels[offset + 1] = color[1]
            self.pixels[offset + 2] = color[2]

    def get_pixel(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            offset = (y * self.width + x) * 3
            return (
                self.pixels[offset],
                self.pixels[offset + 1],
                self.pixels[offset + 2],
            )
        return (0, 0, 0)

    def fill_rect(self, x, y, width, height, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.width, x + width)
        y1 = min(self.height, y + height)
        for py in range(y0, y1):
            for px in range(x0, x1):
                self.set_pixel(px, py, color)

    def circle(self, cx, cy, radius, color):
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    self.set_pixel(cx + dx, cy + dy, color)

    def ring(self, cx, cy, radius, thickness, color):
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                dist2 = dx * dx + dy * dy
                if (radius - thickness) * (radius - thickness) <= dist2 <= radius * radius:
                    self.set_pixel(cx + dx, cy + dy, color)

    def line(self, x0, y0, x1, y1, color, thickness=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            half = thickness // 2
            for oy in range(-half, half + 1):
                for ox in range(-half, half + 1):
                    self.set_pixel(x + ox, y + oy, color)
            if x == x1 and y == y1:
                break
            err2 = 2 * err
            if err2 >= dy:
                err += dy
                x += sx
            if err2 <= dx:
                err += dx
                y += sy

    def polygon(self, points, color):
        if len(points) < 3:
            return
        min_y = max(0, min(p[1] for p in points))
        max_y = min(self.height - 1, max(p[1] for p in points))
        for y in range(min_y, max_y + 1):
            intersections = []
            count = len(points)
            for i in range(count):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % count]
                if (y1 <= y < y2) or (y2 <= y < y1):
                    if y2 != y1:
                        x = x1 + (y - y1) * (x2 - x1) // (y2 - y1)
                        intersections.append(x)
            intersections.sort()
            for i in range(0, len(intersections) - 1, 2):
                for x in range(intersections[i], intersections[i + 1] + 1):
                    self.set_pixel(x, y, color)

    def to_bytes(self):
        return bytes(self.pixels)

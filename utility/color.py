from django.db import models


class Color:
    """A 24-bit color, defined by its RGB values"""

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return f"Color({self.red}, {self.green}, {self.blue})"

    __str__ = __repr__


def parse_color(combined_int):
    blue = combined_int % 256
    green = (combined_int // 256) % 256
    red = (combined_int // (256 * 256)) % 256
    return Color(red, green, blue)


class ColorField(models.IntegerField):
    description = "A 24-bit color"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return parse_color(value)

    def to_python(self, value):
        if isinstance(value, Color):
            return value
        if value is None:
            return value
        return parse_color(value)

    def get_prep_value(self, value: Color):
        if value is None:
            return value
        return value.red * (256*256) + value.green * 256 + value.blue

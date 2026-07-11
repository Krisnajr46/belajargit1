"""Fungsi bantu format tampilan."""
from config import CATEGORY_EMOJI, DEFAULT_EMOJI, MARKETPLACE_COLORS, PRIMARY_COLOR


def format_rupiah(value):
    try:
        n = int(round(float(value)))
    except (ValueError, TypeError):
        return "Rp-"
    return "Rp" + format(n, ",").replace(",", ".")


def format_number(value):
    try:
        n = int(round(float(value)))
    except (ValueError, TypeError):
        return "0"
    return format(n, ",").replace(",", ".")


def format_sold(value):
    try:
        n = int(value)
    except (ValueError, TypeError):
        return "0 terjual"
    if n >= 1000:
        s = format(n / 1000, ".1f").rstrip("0").rstrip(".").replace(".", ",")
        return s + "rb terjual"
    return str(n) + " terjual"


def render_stars(rating):
    try:
        r = float(rating)
    except (ValueError, TypeError):
        r = 0.0
    full = max(0, min(5, int(round(r))))
    return "\u2605" * full + "\u2606" * (5 - full)


def category_emoji(category):
    return CATEGORY_EMOJI.get(str(category), DEFAULT_EMOJI)


def marketplace_color(marketplace):
    return MARKETPLACE_COLORS.get(str(marketplace), PRIMARY_COLOR)

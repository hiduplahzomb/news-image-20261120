#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: one 1024x1024 image summing up the
world news of Friday 20 November 2026.

Layout (broadsheet front page):
  - navy masthead band with the date (hard gate: the image names its day)
  - one full-width lead story: overnight missile strikes on Kyiv's bridges
  - three briefs: COP31 closing day, Japan inflation, Cyclone Akvan
Each story gets an event-specific illustration drawn from shapes, a short
headline (5-9 words) and a two-line deck. No network, no randomness other
than a fixed seed, so repeated runs produce identical bytes.

Run:  python3 draw.py            (writes entry.png next to this file)
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W, H = 1024, 1024

# ---- palette -----------------------------------------------------------
PAPER = (248, 244, 232, 255)
INK = (20, 32, 43, 255)
NAVY = (18, 38, 58, 255)
NAVY_DEEP = (10, 22, 38, 255)
RED = (192, 57, 43, 255)
RED_DARK = (150, 40, 30, 255)
GREY = (110, 108, 96, 255)
RULE = (206, 198, 176, 255)
WHITE = (255, 255, 255, 255)
SKY_TOP = (8, 18, 34, 255)
SKY_HORIZON = (27, 58, 92, 255)
RIVER = (14, 42, 68, 255)
GOLD = (255, 159, 28, 255)
FLAME = (255, 209, 102, 255)
EMBER = (232, 93, 4, 255)
TEAL_BG = (226, 238, 235, 255)
SEA = (16, 52, 96, 255)
SEA_LIGHT = (38, 96, 158, 255)
SAND = (224, 200, 150, 255)

# ---- fonts -------------------------------------------------------------
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_DATE = font(SERIF_B, 58)
F_SUB = font(SANS_B, 21)
F_KICK = font(SANS_B, 19)
F_KICK_S = font(SANS_B, 17)
F_HEAD = font(SERIF_B, 47)
F_HEAD_S = font(SERIF_B, 30)
F_DECK = font(SANS, 23)
F_DECK_S = font(SANS, 19)
F_FOOT = font(SANS, 15)
F_CHIP = font(SANS_B, 16)
F_BIG_NUM = font(SANS_B, 64)
F_NUM = font(SANS_B, 26)
F_AXIS = font(SANS, 15)
F_AXIS_B = font(SANS_B, 21)


# ---- helpers -----------------------------------------------------------
def vgrad(draw, box, top, bottom):
    """Vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[j] + (bottom[j] - top[j]) * t) for j in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c + (255,))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked_text(draw, xy, text, fnt, fill, tracking=3):
    """Draw text with letter spacing; returns total width."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x - xy[0] - tracking


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def glow_circle(layer, cx, cy, r, color):
    """Soft radial glow: concentric circles fading out."""
    d = ImageDraw.Draw(layer)
    steps = 24
    for i in range(steps, 0, -1):
        a = int(color[3] * (1 - i / steps) ** 2)
        d.ellipse([cx - r * i / steps, cy - r * i / steps,
                   cx + r * i / steps, cy + r * i / steps],
                  fill=color[:3] + (a,))


# ---- lead illustration: Kyiv bridges at night --------------------------
def draw_lead(img):
    """Night scene: Dnipro river, a bridge under missile attack."""
    x0, y0, x1, y1 = 16, 116, 1008, 452
    d = ImageDraw.Draw(img)
    vgrad(d, (x0, y0, x1, y1), SKY_TOP, SKY_HORIZON)

    rng = random.Random(20261120)
    for _ in range(90):  # stars
        sx = rng.randint(x0 + 4, x1 - 4)
        sy = rng.randint(y0 + 4, y0 + 150)
        r = rng.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r],
                  fill=(220, 230, 245, rng.choice([120, 180, 230])))

    # crescent moon
    mx, my, mr = 920, 168, 26
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(240, 236, 210, 255))
    d.ellipse([mx - mr + 12, my - mr - 4, mx + mr + 12, my + mr - 4],
              fill=SKY_TOP)

    # skyline silhouettes
    horizon = 330
    bx = x0 + 10
    while bx < x1 - 60:
        bw = rng.randint(28, 64)
        bh = rng.randint(30, 95)
        d.rectangle([bx, horizon - bh, bx + bw, horizon],
                    fill=(7, 15, 26, 255))
        for _ in range(rng.randint(1, 5)):  # lit windows
            wx = rng.randint(bx + 4, bx + bw - 8)
            wy = rng.randint(horizon - bh + 6, horizon - 10)
            d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 200, 90, 200))
        bx += bw + rng.randint(4, 18)

    # Ukrainian flag on a rooftop pole (left skyline)
    fx, fy = 120, horizon - 88
    d.line([(fx, fy - 34), (fx, fy)], fill=(200, 200, 200, 255), width=3)
    d.rectangle([fx, fy - 34, fx + 34, fy - 23], fill=(0, 91, 187, 255))
    d.rectangle([fx, fy - 23, fx + 34, fy - 12], fill=(255, 213, 0, 255))

    # river
    d.rectangle([x0, horizon, x1, y1], fill=RIVER)
    for i in range(26):  # water streaks
        wy = horizon + 8 + i * 4
        sx = rng.randint(x0 + 10, x1 - 160)
        ln = rng.randint(30, 150)
        d.line([(sx, wy), (sx + ln, wy)],
               fill=(70, 130, 180, rng.choice([40, 70, 100])), width=2)

    # bridge deck + pylons + cables
    deck_y = 372
    d.rectangle([x0, deck_y, x1, deck_y + 10], fill=(6, 12, 20, 255))
    for lx in range(x0 + 24, x1 - 20, 44):  # streetlights along the deck
        d.ellipse([lx - 2, deck_y - 5, lx + 2, deck_y - 1],
                  fill=(255, 214, 130, 220))
    for px in (300, 700):
        d.rectangle([px - 7, deck_y - 118, px + 7, deck_y + 10],
                    fill=(6, 12, 20, 255))
        d.line([(px, deck_y - 118), (x0 + 40, deck_y)], fill=(30, 50, 70, 255),
               width=2)
        d.line([(px, deck_y - 118), (x1 - 40, deck_y)], fill=(30, 50, 70, 255),
               width=2)
        for t in range(1, 6):  # suspenders
            hx = px - 90 + t * 36
            d.line([(hx, deck_y - 118 + abs(hx - px) // 2), (hx, deck_y)],
                   fill=(30, 50, 70, 255), width=1)

    # broken deck section between the pylons (gap + tilted slab)
    d.rectangle([470, deck_y, 540, deck_y + 10], fill=RIVER)
    d.polygon([(470, deck_y + 10), (540, deck_y + 10), (528, deck_y + 26),
               (478, deck_y + 22)], fill=(6, 12, 20, 255))

    # missile streaks
    for (sx, sy, ex, ey) in [(250, 128, 330, 330), (620, 122, 690, 320),
                             (820, 140, 780, 300)]:
        d.line([(sx, sy), (ex, ey)], fill=(255, 240, 180, 255), width=3)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 250, 220, 255))

    # explosions on the deck
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for (ex, ey, r) in [(505, 356, 90), (760, 360, 62)]:
        glow_circle(layer, ex, ey, r + 46, (255, 140, 30, 120))
    img.paste(Image.alpha_composite(img, layer), (0, 0))
    d = ImageDraw.Draw(img)
    for (ex, ey, r) in [(505, 356, 46), (760, 360, 32)]:
        starburst(d, ex, ey, r, r * 0.45, 12, EMBER)
        starburst(d, ex, ey, r * 0.62, r * 0.3, 10, GOLD)
        d.ellipse([ex - r * 0.3, ey - r * 0.3, ex + r * 0.3, ey + r * 0.3],
                  fill=FLAME)
        # smoke plume
        for i, (ox, oy, sr) in enumerate([(-14, -34, 20), (6, -52, 26),
                                          (24, -70, 18)]):
            d.ellipse([ex + ox - sr, ey + oy - sr, ex + ox + sr, ey + oy + sr],
                      fill=(120, 125, 135, 150 - i * 30))
        # fire reflection on the water
        for i in range(8):
            wy = deck_y + 18 + i * 5
            d.line([(ex - 26 + i * 2, wy), (ex + 26 - i * 2, wy)],
                   fill=(255, 150, 50, 140 - i * 14), width=2)

    # caption chip
    d.rounded_rectangle([x0 + 14, y1 - 40, x0 + 196, y1 - 12], radius=6,
                        fill=(6, 12, 20, 200))
    d.text((x0 + 26, y1 - 36), "KYIV  •  THE DNIPRO", font=F_CHIP,
           fill=(240, 236, 210, 255))
    d.rectangle([x0, y0, x1, y1], outline=(10, 20, 32, 255), width=2)


# ---- brief 1: COP31 draft ----------------------------------------------
def draw_cop31(img, x0, y0, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=TEAL_BG)
    # document page
    px, py, pw, ph = x0 + 22, y0 + 16, 150, h - 32
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=6,
                        fill=WHITE, outline=(170, 180, 175, 255), width=2)
    for i in range(3):  # text bars
        d.rectangle([px + 14, py + 16 + i * 18, px + pw - 14, py + 24 + i * 18],
                    fill=(200, 205, 200, 255))
    # oil drop with red strike-through
    cx, cy = px + pw // 2, py + ph - 42
    d.polygon([(cx, cy - 26), (cx + 20, cy + 2), (cx + 20, cy + 10),
               (cx - 20, cy + 10), (cx - 20, cy + 2)], fill=(40, 40, 40, 255))
    d.ellipse([cx - 20, cy - 6, cx + 20, cy + 30], fill=(40, 40, 40, 255))
    d.line([(cx - 30, cy - 34), (cx + 30, cy + 34)], fill=RED, width=7)
    d.line([(cx - 30, cy + 34), (cx + 30, cy - 34)], fill=RED, width=7)
    # thermometer
    tx = x0 + w - 78
    d.rounded_rectangle([tx, y0 + 18, tx + 26, y0 + h - 44], radius=12,
                        fill=WHITE, outline=(150, 160, 155, 255), width=2)
    d.rectangle([tx + 6, y0 + 34, tx + 20, y0 + h - 50], fill=RED)
    d.ellipse([tx - 8, y0 + h - 58, tx + 34, y0 + h - 16],
              fill=RED, outline=(150, 40, 30, 255), width=2)
    # rising sun rays
    sx, sy = x0 + w - 52, y0 + 30
    for a in range(0, 360, 45):
        r1, r2 = 10, 18
        x1 = sx + r1 * math.cos(math.radians(a))
        y1 = sy + r1 * math.sin(math.radians(a))
        x2 = sx + r2 * math.cos(math.radians(a))
        y2 = sy + r2 * math.sin(math.radians(a))
        d.line([(x1, y1), (x2, y2)], fill=GOLD, width=3)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=RULE, width=2)


# ---- brief 2: Japan inflation chart ------------------------------------
def draw_japan(img, x0, y0, w, h):
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=WHITE)
    # faint yen watermark
    d.text((x0 + w - 88, y0 + 6), "¥", font=F_BIG_NUM, fill=(235, 235, 225, 255))
    base = y0 + h - 30
    # target line at 2.0% with label at the right end
    ty = base - int((2.0 / 2.6) * (h - 56))
    for lx in range(x0 + 16, x0 + w - 16, 12):
        d.line([(lx, ty), (lx + 7, ty)], fill=GREY, width=2)
    d.text((x0 + w - 16, ty - 24), "TARGET 2%", font=F_AXIS, fill=GREY,
           anchor="ra")
    # bars: SEP 2.1, OCT 2.2 (values labelled inside the bars)
    scale = (h - 56) / 2.6
    for i, (label, val, col) in enumerate([("SEP", 2.1, (90, 120, 150, 255)),
                                           ("OCT", 2.2, RED)]):
        bx = x0 + 44 + i * 112
        bh = int(val * scale)
        d.rectangle([bx, base - bh, bx + 78, base], fill=col)
        d.text((bx + 10, base - bh + 10), f"{val}%", font=F_AXIS_B,
               fill=WHITE)
        d.text((bx + 14, base + 6), label, font=F_AXIS, fill=GREY)
    # rising arrow
    d.line([(x0 + 60, base - int(2.1 * scale) - 34),
            (x0 + 250, base - int(2.2 * scale) - 52)],
           fill=RED_DARK, width=4)
    d.polygon([(x0 + 250, base - int(2.2 * scale) - 52),
               (x0 + 232, base - int(2.2 * scale) - 52),
               (x0 + 244, base - int(2.2 * scale) - 38)],
              fill=RED_DARK)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=RULE, width=2)


# ---- brief 3: Cyclone Akvan --------------------------------------------
def draw_cyclone(img, x0, y0, w, h):
    d = ImageDraw.Draw(img)
    vgrad(d, (x0, y0, x0 + w, y0 + h), SEA, SEA_LIGHT)
    cx, cy = x0 + w // 2 - 10, y0 + h // 2 - 6
    # spiral bands
    for k, r in enumerate([66, 54, 42, 30, 19]):
        start = k * 55
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 250,
              fill=(235, 242, 250, 235), width=9)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(240, 246, 252, 255))
    # coastline at the bottom
    d.polygon([(x0, y0 + h), (x0, y0 + h - 26), (x0 + 90, y0 + h - 44),
               (x0 + 190, y0 + h - 30), (x0 + w, y0 + h - 48),
               (x0 + w, y0 + h)], fill=SAND)
    d.line([(x0, y0 + h - 26), (x0 + 90, y0 + h - 44),
            (x0 + 190, y0 + h - 30), (x0 + w, y0 + h - 48)],
           fill=(255, 255, 255, 220), width=3)
    # rain streaks
    rng = random.Random(1120)
    for _ in range(46):
        rx = rng.randint(x0 + 6, x0 + w - 6)
        ry = rng.randint(y0 + 6, y0 + h - 40)
        d.line([(rx, ry), (rx - 6, ry + 12)],
               fill=(200, 220, 240, 130), width=2)
    # name chip
    d.rounded_rectangle([x0 + 12, y0 + 10, x0 + 96, y0 + 34], radius=6,
                        fill=(8, 26, 48, 210))
    d.text((x0 + 22, y0 + 13), "AKVAN", font=F_CHIP, fill=WHITE)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=RULE, width=2)


# ---- page assembly ------------------------------------------------------
def build():
    img = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead band
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.rectangle([0, 112, W, 116], fill=RED)
    sub = "WORLD NEWS  •  ONE DAY IN ONE IMAGE"
    sw = sum(d.textlength(c, font=F_SUB) + 3 for c in sub) - 3
    tracked_text(d, ((W - sw) // 2, 14), sub, F_SUB, (200, 210, 225, 255))
    date = "FRIDAY 20 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) // 2, 40), date, font=F_DATE, fill=WHITE)

    # lead illustration + text
    draw_lead(img)
    d = ImageDraw.Draw(img)
    ly = 462
    tracked_text(d, (16, ly), "UKRAINE  •  OVERNIGHT STRIKES", F_KICK,
                 RED)
    head = "Russian missiles strike Kyiv's Dnipro bridges"
    head_lines = wrap(d, head, F_HEAD, 992)
    for i, line in enumerate(head_lines):
        d.text((16, ly + 28 + i * 54), line, font=F_HEAD, fill=INK)
    deck = ("Overnight strikes damage Dnipro crossings; traffic halted "
            "and power cut in parts of the capital.")
    deck_y = ly + 28 + len(head_lines) * 54 + 6
    for i, line in enumerate(wrap(d, deck, F_DECK, 992)):
        d.text((16, deck_y + i * 29), line, font=F_DECK,
               fill=(60, 66, 74, 255))

    # divider
    d.line([(16, 606), (1008, 606)], fill=RULE, width=2)

    # briefs
    briefs = [
        ("CLIMATE  •  ANTALYA",
         "COP31 closing day: fossil fuels erased",
         "Draft drops phase-out pledge and $120bn target; "
         "no agreement yet at deadline.",
         draw_cop31),
        ("ECONOMY  •  TOKYO",
         "Japan inflation hits 2.2%, rate hike looms",
         "Core prices top the 2% target again; Bank of Japan "
         "tipped to raise rates in December.",
         draw_japan),
        ("WEATHER  •  ODISHA",
         "Cyclone Akvan strikes India's Odisha coast",
         "Landfall near Gopalpur; thousands moved to shelters as "
         "third storm hits in a month.",
         draw_cyclone),
    ]
    col_w, gap, top = 316, 16, 622
    for i, (kick, head, deck, painter) in enumerate(briefs):
        x = 16 + i * (col_w + gap)
        painter(img, x, top, col_w, 150)
        d = ImageDraw.Draw(img)
        tracked_text(d, (x, top + 162), kick, F_KICK_S, RED)
        lines = wrap(d, head, F_HEAD_S, col_w)
        for j, line in enumerate(lines[:3]):
            d.text((x, top + 188 + j * 35), line, font=F_HEAD_S,
                   fill=INK)
        dy = top + 188 + min(len(lines), 3) * 35 + 6
        for j, line in enumerate(wrap(d, deck, F_DECK_S, col_w)[:3]):
            d.text((x, dy + j * 24), line, font=F_DECK_S,
                   fill=(60, 66, 74, 255))

    # footer
    d.line([(16, 980), (1008, 980)], fill=RULE, width=2)
    d.text((16, 990),
           "Events of Friday 20 November 2026  •  Sources: Reuters, "
           "en.h.ua, AsiaToday, Particle News",
           font=F_FOOT, fill=GREY)
    d.text((1008, 990), "Drawn by an AI agent", font=F_FOOT,
           fill=GREY, anchor="ra")

    rgb = img.convert("RGB")
    rgb.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    build()

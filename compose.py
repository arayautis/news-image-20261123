#!/usr/bin/env python3
"""Compose the entry image for make.fun news-image-20261123.

Draws a 1024x1024 newspaper front page summing up Monday 23 November
2026, using only Pillow vector drawing (no photographs, no network).
Every story below was checked against same-day reporting (Reuters, AP,
BBC, Al Jazeera, The Hindu, Indian Express, Dawn, IQAir) on 23 November
2026. Output is deterministic: fixed layout, fixed text, no timestamps,
no randomness.

Run:  python3 compose.py            # writes entry.png next to this file
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 247, 238)
INK = (16, 28, 54)
TEAL = (13, 74, 66)          # lead band: climate talks
TEAL_SOFT = (214, 232, 228)
RED = (176, 22, 22)
GOLD = (233, 178, 44)
GREY = (92, 92, 92)
BODY = (38, 38, 38)
GREEN = (24, 108, 60)
ORANGE = (206, 84, 20)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, fnt, fill, leading):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(d, x, y, text, fill=None, size=18):
    f = font(SANS_B, size)
    d.text((x, y), text, font=f, fill=fill or RED)
    return y + size + 6


def headline(d, x, y, text, size, max_w, fill=None):
    f = font(SERIF_B, size)
    return draw_lines(d, wrap(d, text, f, max_w), x, y, f,
                      fill or INK, int(size * 1.08))


def deck(d, x, y, text, size, max_w, fill=None):
    f = font(SANS, size)
    return draw_lines(d, wrap(d, text, f, max_w), x, y, f,
                      fill or BODY, int(size * 1.32))


# ---- pictograms: small vector scenes, drawn with PIL primitives ----

def icon_cracked_globe(d, x0, y0, s):
    """A globe split by a jagged crack: the climate talks collapse."""
    cx, cy = x0 + s // 2, y0 + s // 2
    r = s // 2 - 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL_SOFT,
              outline=TEAL, width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
              outline=TEAL, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=TEAL, width=3)
    d.line([(cx - r * 0.35, cy - r), (cx - r * 0.1, cy - r * 0.25),
            (cx - r * 0.45, cy + r * 0.15), (cx - r * 0.05, cy + r * 0.6),
            (cx - r * 0.3, cy + r)], fill=RED, width=5)


def icon_tanker_mine(d, x0, y0, s):
    """An oil tanker on a swell, a naval mine below it."""
    w = s + 26
    d.rectangle([x0 + 18, y0 + s - 62, x0 + w - 30, y0 + s - 36],
                fill=INK)
    d.rectangle([x0 + w - 40, y0 + s - 84, x0 + w - 28, y0 + s - 62],
                fill=INK)
    d.polygon([(x0, y0 + s - 36), (x0 + w, y0 + s - 36),
               (x0 + w - 16, y0 + s - 8), (x0 + 16, y0 + s - 8)],
              fill=INK)
    d.line([(x0, y0 + s - 2), (x0 + w, y0 + s - 2)], fill=(96, 128, 168),
           width=3)
    # spiked mine, lower left
    mx, my, mr = x0 + 34, y0 + s - 14, 11
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([(mx, my), (mx + (mr + 7) * math.cos(a),
                            my + (mr + 7) * math.sin(a))],
               fill=INK, width=3)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=INK)
    # flame above the deck
    d.polygon([(x0 + w - 34, y0 + 14), (x0 + w - 18, y0 + 34),
               (x0 + w - 46, y0 + 34)], fill=ORANGE)


def icon_warship(d, x0, y0, s):
    """A warship listing to one side, smoke above it."""
    w = s + 26
    d.polygon([(x0 + 8, y0 + s - 40), (x0 + w - 6, y0 + s - 52),
               (x0 + w - 26, y0 + s - 14), (x0 + 26, y0 + s - 14)],
              fill=INK)
    d.rectangle([x0 + 34, y0 + s - 66, x0 + w - 52, y0 + s - 44],
                fill=INK)
    d.line([(x0 + w - 40, y0 + s - 66), (x0 + w - 40, y0 + s - 88)],
           fill=INK, width=4)
    for cx, cy, cr in ((x0 + 30, y0 + 6, 9), (x0 + 48, y0 - 2, 7),
                       (x0 + 18, y0 + 16, 6)):
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
                  fill=(150, 150, 150))
    d.line([(x0, y0 + s - 8), (x0 + w, y0 + s - 8)], fill=(96, 128, 168),
           width=3)


def icon_badge(d, x0, y0, s):
    """A sheriff's star badge: a cartel kingpin taken alive."""
    cx, cy = x0 + s // 2, y0 + s // 2
    r = s // 2 - 2
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.60
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=GOLD, outline=INK)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=INK)


def icon_ruin(d, x0, y0, s):
    """A broken apartment block: a drone strike in Dymer, Kyiv region."""
    d.rectangle([x0 + 10, y0 + 8, x0 + s - 8, y0 + s - 6], fill=INK)
    d.polygon([(x0 + 10, y0 + 8), (x0 + s // 2, y0 + 26),
               (x0 + s - 8, y0 + 8), (x0 + s - 8, y0 - 2),
               (x0 + 10, y0 - 2)], fill=INK)
    for row in range(2):
        for col in range(3):
            wx = x0 + 18 + col * 15
            wy = y0 + 32 + row * 15
            d.rectangle([wx, wy, wx + 9, wy + 9], fill=GOLD)
    # rubble at the base
    d.polygon([(x0 + 4, y0 + s - 6), (x0 + 22, y0 + s - 16),
               (x0 + 42, y0 + s - 6)], fill=GREY)


def icon_chart_down(d, x0, y0, s):
    """A falling market chart with a red arrow."""
    d.line([(x0 + 6, y0 + 18), (x0 + s // 3, y0 + s // 3),
            (x0 + s // 2, y0 + s // 4), (x0 + s - 8, y0 + s - 14)],
           fill=RED, width=5)
    ax, ay = x0 + s - 8, y0 + s - 14
    d.polygon([(ax, ay), (ax - 18, ay - 2), (ax - 2, ay - 18)],
              fill=RED)
    d.line([(x0 + 6, y0 + s - 8), (x0 + s - 4, y0 + s - 8)],
           fill=INK, width=3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)

    # ---------- masthead ----------
    d.text((W // 2, 20), "THE WORLD TODAY", font=font(SERIF_B, 76),
           fill=INK, anchor="ma")
    d.line([(24, 112), (W - 24, 112)], fill=INK, width=3)
    d.text((24, 122), "MONDAY 23 NOVEMBER 2026", font=font(SANS_B, 22),
           fill=INK)
    d.text((W - 24, 124), "ONE DAY  •  ONE PAGE", font=font(SANS, 18),
           fill=GREY, anchor="ra")
    d.line([(24, 154), (W - 24, 154)], fill=INK, width=2)

    # ---------- lead: COP31 collapses (162-384) ----------
    d.rectangle([24, 162, 1000, 384], fill=TEAL, outline=INK, width=2)
    y = kicker(d, 44, 176, "ANTALYA  •  CLIMATE  •  LEAD STORY",
               fill=GOLD)
    y = headline(d, 44, y, "CLIMATE TALKS COLLAPSE", 44, 660,
                 fill=(255, 255, 255))
    y += 8
    deck(d, 44, y,
         "COP31 fails after record overtime: the EU and others reject "
         "any deal with no language on phasing out fossil fuels.",
         20, 660, fill=(222, 234, 230))
    icon_cracked_globe(d, 812, 198, 150)

    # ---------- row 2: Hormuz / Benghazi (396-604) ----------
    d.rectangle([24, 396, 500, 604], outline=INK, width=2)
    y = kicker(d, 40, 408, "STRAIT OF HORMUZ  •  SHIPPING")
    y = headline(d, 40, y, "TANKERS HIT, MINES IN THE WATER", 28, 440)
    y += 4
    deck(d, 40, y,
         "Three tankers are struck near the strait; two more catch fire "
         "after hitting naval mines, Iran's navy says, as attacks on "
         "shipping hit their highest level since the war began.",
         17, 330)
    icon_tanker_mine(d, 396, 508, 78)

    d.rectangle([524, 396, 1000, 604], outline=INK, width=2)
    y = kicker(d, 540, 408, "BENGHAZI  •  LIBYA")
    y = headline(d, 540, y, "SEA DRONES SINK RUSSIAN WARSHIP", 28, 440)
    y += 4
    deck(d, 540, y,
         "Suspected Ukrainian sea drones hit the corvette Merkury at "
         "the Benghazi naval base; the ship is badly damaged and later "
         "capsizes, with 10 people hurt.",
         17, 330)
    icon_warship(d, 896, 508, 78)

    # ---------- row 3: Mexico / Ukraine / markets (616-824) ----------
    d.rectangle([24, 616, 340, 824], outline=INK, width=2)
    y = kicker(d, 38, 628, "SINALOA  •  MEXICO", size=16)
    y = headline(d, 38, y, "EL CHAPO ISIDRO CAPTURED", 24, 288)
    y += 4
    deck(d, 38, y,
         "Troops seize cartel boss Fausto Isidro Meza Flores, wanted "
         "by the US on a $5m bounty, in a raid that leaves 11 dead.",
         16, 236)
    icon_badge(d, 264, 758, 52)

    d.rectangle([354, 616, 670, 824], outline=INK, width=2)
    y = kicker(d, 368, 628, "KYIV REGION  •  UKRAINE", size=16)
    y = headline(d, 368, y, "DRONE HITS FLAT BLOCK", 24, 288)
    y += 4
    deck(d, 368, y,
         "A Russian drone hits a five-storey block in Dymer; 2 people "
         "are killed and 11 are missing, two of them children.",
         16, 236)
    icon_ruin(d, 602, 758, 52)

    d.rectangle([684, 616, 1000, 824], outline=INK, width=2)
    y = kicker(d, 698, 628, "MARKETS  •  MONEY", size=16)
    y = headline(d, 698, y, "STOCKS PLUNGE WORLDWIDE", 24, 288)
    y += 4
    deck(d, 698, y,
         "US shares dive on Friday; Taiwan falls 17.5% in a week and "
         "Asian markets stay on alert as trading opens on Monday.",
         16, 236)
    icon_chart_down(d, 922, 758, 52)

    # ---------- also today (836-968) ----------
    d.rectangle([24, 836, 1000, 968], outline=INK, width=2)
    y = kicker(d, 40, 848, "ALSO TODAY", size=17)
    items = [
        "POLAND: fallen objects were Russian cruise missiles.",
        "WASHINGTON: Democrats win control of Congress.",
        "UN: 128 states agree to pursue rules on killer robots.",
        "TURIN: Alcaraz wins his first ATP Finals title.",
        "MERCURY: BepiColombo enters orbit, a second-ever feat.",
        "INDONESIA: 24 body bags from the Cikande fire.",
    ]
    f_item = font(SANS, 16)
    col_w, x0s = 462, (40, 524)
    for i, text in enumerate(items):
        x = x0s[i % 2]
        yy = 876 + (i // 2) * 30
        d.text((x, yy), "•", font=f_item, fill=RED)
        for ln in wrap(d, text, f_item, col_w - 18):
            d.text((x + 16, yy), ln, font=f_item, fill=BODY)
            yy += 20
            break  # one line each: keep the ticker tight
    # footer
    d.text((24, 982), "Stories checked against same-day reporting by "
           "Reuters, AP, BBC, Al Jazeera, The Hindu and Dawn.",
           font=font(SANS, 14), fill=GREY)
    d.text((W - 24, 982), "make.fun  •  news-image-20261123",
           font=font(SANS, 14), fill=GREY, anchor="ra")

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    build()
    print("wrote entry.png")

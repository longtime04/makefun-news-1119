#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up
Thursday 19 November 2026 in a single image.

PIL only, system DejaVu fonts, deterministic output: the same
bytes on every run (no timestamps, no randomness).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
BODY = (40, 40, 40)
NAVY = (11, 31, 58)
GOLD = (212, 175, 55)
RED = (176, 42, 48)
WHITE = (255, 255, 255)
MAP_BG = (18, 50, 79)
LAND = (61, 106, 148)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(s):
    return font("DejaVuSerif-Bold.ttf", s)


def sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


def sans(s):
    return font("DejaVuSans.ttf", s)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(d, cx, y, text, fnt, fill):
    d.text((cx - d.textlength(text, font=fnt) / 2, y),
           text, font=fnt, fill=fill)


def draw_masthead(d):
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    center(d, W // 2, 12, "THE WORLD TODAY", serif_b(60), WHITE)
    center(d, W // 2, 82, "Thursday 19 November 2026",
           sans_b(28), GOLD)


def icon_summit(d, cx, top):
    """Three circles for the three leaders: T, X, P."""
    cols = [(176, 42, 48), (212, 175, 55), (30, 90, 160)]
    letters = ["T", "X", "P"]
    for i, (col, ch) in enumerate(zip(cols, letters)):
        ox = cx - 78 + i * 52
        d.ellipse([ox, top, ox + 52, top + 52], fill=col,
                  outline=WHITE, width=3)
        f = sans_b(26)
        d.text((ox + 26 - d.textlength(ch, font=f) / 2, top + 11),
               ch, font=f, fill=WHITE)


def icon_gta(d, cx, top):
    """Simple game controller: rounded body, pad and buttons."""
    d.rounded_rectangle([cx - 62, top + 8, cx + 62, top + 52],
                        radius=18, fill=(106, 63, 181),
                        outline=WHITE, width=3)
    d.ellipse([cx - 44, top + 20, cx - 24, top + 40], fill=WHITE)
    d.ellipse([cx + 24, top + 20, cx + 44, top + 40], fill=WHITE)
    d.rectangle([cx - 8, top + 24, cx + 8, top + 36], fill=GOLD)


def icon_ipo(d, cx, top):
    """Rising chart bars with an arrow."""
    base = top + 52
    bars = [(cx - 56, 20), (cx - 28, 32), (cx + 0, 44),
            (cx + 28, 56)]
    for bx, bh in bars:
        d.rectangle([bx, base - bh, bx + 20, base], fill=(14, 122, 77))
    d.line([cx - 56, base - 20, cx - 18, base - 32,
            cx + 10, base - 44, cx + 48, base - 56],
           fill=RED, width=4)
    d.polygon([(cx + 48, base - 56), (cx + 30, base - 56),
               (cx + 48, base - 38)], fill=RED)


def draw_hero(d, x, y, w, h, accent, headline, summary, icon):
    d.rectangle([x, y, x + w, y + h], fill=WHITE,
                outline=NAVY, width=2)
    d.rectangle([x, y, x + w, y + 8], fill=accent)
    icon(d, x + w // 2, y + 20)
    center(d, x + w // 2, y + 92, headline, sans_b(24), INK)
    lines = wrap(d, summary, sans(15), w - 28)
    ly = y + 128
    for ln in lines[:3]:
        center(d, x + w // 2, ly, ln, sans(15), BODY)
        ly += 20


def draw_map(d):
    x0, y0, x1, y1 = 16, 348, 1008, 462
    d.rectangle([x0, y0, x1, y1], fill=MAP_BG, outline=NAVY, width=2)
    d.text((x0 + 12, y0 + 6), "WORLD MAP  —  PINS 1-12 MARK THE LEAD STORIES",
           font=sans_b(14), fill=GOLD)
    # Schematic continents: simple light blobs on the dark sea.
    d.ellipse([60, 392, 250, 438], fill=LAND)    # N. America
    d.ellipse([225, 428, 315, 458], fill=LAND)   # S. America
    d.ellipse([478, 388, 560, 414], fill=LAND)   # Europe
    d.ellipse([500, 414, 600, 456], fill=LAND)   # Africa
    d.ellipse([620, 386, 905, 432], fill=LAND)   # Asia
    d.ellipse([828, 434, 912, 456], fill=LAND)   # Australia
    pins = [
        (712, 406), (798, 420), (605, 398), (620, 438),
        (688, 424), (668, 406), (650, 436), (580, 382),
        (812, 392), (842, 412), (762, 396), (535, 388),
    ]
    f = sans_b(12)
    for i, (px, py) in enumerate(pins, start=1):
        d.ellipse([px - 12, py - 12, px + 12, py + 12],
                  fill=RED, outline=WHITE, width=3)
        label = str(i)
        d.text((px - d.textlength(label, font=f) / 2, py - 8),
               label, font=f, fill=WHITE)


BRIEFS = [
    ("MIDEAST", "Three oil tankers ablaze after hitting mines near Hormuz."),
    ("WORLD COURT", "Court to rule today on Myanmar Rohingya genocide case."),
    ("GAZA", "Israel launches ground operation in central Gaza; dozens flee."),
    ("AFRICA", "Ethiopia-Eritrea clashes risk full-scale war."),
    ("GULF", "Gulf nations repel Iran drone attacks."),
    ("GULF", "US reissues security warnings in Bahrain and Saudi Arabia."),
    ("YEMEN", "Dozens more children killed as hostilities escalate."),
    ("UKRAINE", "Kyiv says it hit two Russian refineries; 'Operation Vivaldi'."),
    ("CHINA", "Xi meets Putin ahead of summit with Trump."),
    ("TAIWAN", "Taipei awaits Trump's OK on $14bn arms sale."),
    ("INDIA", "Police kill rebel leader in Kashmir."),
    ("FRANCE", "Three women jailed for joining ISIS in Syria."),
    ("US", "Pakistani jailed 27 years for Trump murder plot."),
    ("US", "Grand jury indicts man over foiled Hindu temple shooting."),
    ("ART", "Van Gogh sells for record $190.4m after dispute."),
    ("US", "Jeffries set to be first Black House Speaker."),
    ("AMERICAS", "Hegseth's surprise Venezuela trip; defense pact signed."),
    ("KOREA", "College exam held under strict curbs after cheating scandal."),
    ("JAPAN", "Magnitude 5.7 quake jolts Kumamoto; no tsunami warning."),
    ("TECH", "Governments warn Java flaw leaves systems open to hackers."),
    ("CLIMATE", "COP31 deadlock persists; new 'climate reality check' launched."),
    ("FAITH", "Muslims projected to outnumber Christians by 2035."),
    ("SPACE", "Voyager 1 reaches one light-day from Earth."),
    ("AUSTRALIA", "Red crabs begin annual march to sea on Christmas Island."),
    ("US", "El Nino rain floods south Florida; synagogue roof collapses."),
    ("SPORT", "Pochettino arrives at Man Utd as club fights relegation."),
    ("MARKETS", "Asian markets mixed; Nikkei up 0.55% on IPO, Fed worries."),
    ("AMERICAS", "Haiti and El Salvador ink security deal."),
]


def draw_briefs(d):
    d.text((16, 472), "THE DAY IN BRIEF  —  28 STORIES",
           font=sans_b(17), fill=NAVY)
    d.line([16, 496, 1008, 496], fill=NAVY, width=2)
    col_w = 484
    col_x = [16, 524]
    row_h = 35
    top = 504
    for idx, (tag, text) in enumerate(BRIEFS):
        col = idx // 14
        row = idx % 14
        y = top + row * row_h
        x = col_x[col]
        if row % 2 == 0:
            d.rectangle([x - 4, y - 3, x + col_w, y + row_h - 6],
                        fill=(238, 233, 220))
        num = str(idx + 1) + "."
        nf = sans_b(15)
        d.text((x, y), num, font=nf, fill=RED)
        nx = x + d.textlength(num, font=nf) + 6
        tf = sans_b(13)
        d.text((nx, y + 1), tag, font=tf, fill=NAVY)
        tx = nx + d.textlength(tag, font=tf) + 7
        # Shrink the story text until it fits the column on one line.
        size = 15
        while size > 12:
            f = sans(size)
            if tx + d.textlength(text, font=f) <= x + col_w:
                break
            size -= 1
        d.text((tx, y), text, font=sans(size), fill=INK)


def draw_footer(d):
    center(d, W // 2, 994,
           "All stories first reported Thursday 19 November 2026",
           sans_b(15), NAVY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    hy, hh, hw = 132, 204, 322
    draw_hero(d, 16, hy, hw, hh, RED, "SUMMIT OF THREE",
              "Trump, Xi and Putin hold first-ever trilateral "
              "summit in China; nuclear arms and two wars on "
              "the table.", icon_summit)
    draw_hero(d, 351, hy, hw, hh, (106, 63, 181), "GTA VI DAY",
              "Grand Theft Auto VI launches today on PS5 and "
              "Xbox Series X|S, $79.99; 99 Metascore; 2.3m "
              "watching on Twitch.", icon_gta)
    draw_hero(d, 686, hy, hw, hh, (14, 122, 77), "RECORD IPO",
              "Anthropic debuts as ANT: $81.3bn raised at "
              "$83; about a $1.5tn valuation, the largest "
              "IPO ever.", icon_ipo)
    draw_map(d)
    draw_briefs(d)
    draw_footer(d)
    img.save(OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()

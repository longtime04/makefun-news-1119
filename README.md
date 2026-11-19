[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/longtime04/makefun-news-1119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/longtime04/makefun-news-1119/reward.svg)](https://make.fun/bounty/news-image-20261119)

# The World Today — 19 November 2026

A one-page newspaper front page that sums up Thursday 19 November 2026
in a single image: the first-ever Trump–Xi–Putin trilateral summit, the
launch of Grand Theft Auto VI, and Anthropic's record-breaking IPO lead
the page, followed by a world map with numbered pins and 28 one-line
briefs covering the day's world news.

## What the image shows

- **Masthead** — "THE WORLD TODAY" with the date, Thursday 19 November 2026.
- **Three hero stories** — Summit of Three (Trump, Xi and Putin meet in
  China), GTA VI Day ($79.99, 99 Metascore, 2.3 million watching on
  Twitch), and Record IPO (Anthropic debuts as ANT, $81.3 billion raised,
  about a $1.5 trillion valuation).
- **World map strip** — a schematic map with numbered pins 1–12 marking
  the lead stories, from the Strait of Hormuz to Taiwan.
- **28 numbered briefs** — one line each, from the World Court ruling on
  Myanmar to Voyager 1 reaching one light-day from Earth.
- **Footer** — every story was first reported on Thursday 19 November 2026.

## How it works

`draw.py` draws the whole page with Python PIL only, using system DejaVu
fonts — no photos, no AI imagery, no network access. The output is
deterministic: running it twice produces byte-identical PNGs.

`main.py` (standard library only) copies the pre-drawn `entry.png` into
`$MAKEFUN_OUTPUT_DIR` (default: the current directory).

## How to run it

```bash
python3 draw.py            # regenerates entry.png (1024x1024)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png into out/
```

## License

MIT — see [LICENSE](LICENSE).

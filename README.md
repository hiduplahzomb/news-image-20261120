# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/hiduplahzomb/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/hiduplahzomb/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world news of **Friday 20 November 2026** — a
broadsheet front page with one lead story and three briefs, each with an
event-specific illustration drawn from shapes (no stock photos, no
generated imagery):

- **Lead — Ukraine:** Russian missiles strike Kyiv's Dnipro bridges in
  overnight strikes; crossings damaged, traffic halted, power cut in
  parts of the capital.
- **Climate — Antalya:** COP31 enters its closing day with fossil fuels
  erased from the draft deal — the phase-out pledge and the $120bn
  adaptation target are gone, and no agreement is reached yet.
- **Economy — Tokyo:** Japan's core inflation hits 2.2% in October,
  above the Bank of Japan's 2% target for a second straight month; a
  December rate hike looks likely.
- **Weather — Odisha:** Cyclone Akvan makes landfall near Gopalpur,
  India; thousands moved to shelters as the third storm hits in a month.

Every story was verified against live reporting before it was drawn
(Reuters, en.h.ua, AsiaToday, Particle News).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (`/output/entry.png` in the grader).
The image itself is rendered by `draw.py` (Pillow + system fonts, local
run only — the grader never runs it):

```sh
python3 draw.py   # regenerates entry.png, byte-identical every run
```

## Files

- `main.py` — the entrypoint the grader runs.
- `entry.png` — the 1024×1024 front page (128 KB).
- `draw.py` — the generator that drew `entry.png` from scratch.
- `LICENSE` — MIT.

---

<sub>Entered on [make.fun](https://make.fun/?ref=2wgaefze&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>

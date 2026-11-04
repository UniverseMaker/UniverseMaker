#!/usr/bin/env python3
"""UniverseMaker profile asset builder.

Generates every SVG used by README.md into ../assets:
  hero.svg        - animated cosmic banner (static content)
  highlights.svg  - research output tiles (edit HIGHLIGHTS below)
  orbit.svg       - "Research Universe" orbit map (edit ORBITS below)
  footer.svg      - animated wave footer
  stats.svg       - live GitHub telemetry (contributions, streaks, languages, heatmap)

Standard library only. Run locally or from GitHub Actions:
  python scripts/build.py            # everything
  python scripts/build.py --stats    # only the live stats card
Set GITHUB_TOKEN to raise API limits and get byte-accurate language stats.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import math
import os
import random
import re
import sys
import urllib.request
from pathlib import Path

USER = "UniverseMaker"
JOINED = dt.date(2015, 9, 24)
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# ── palette (matches daeseungpark.com dark theme + "Green Eye") ─────────────
BG0, BG1 = "#070914", "#0d1030"
INDIGO, INDIGO_D = "#8b9bff", "#3a4cf0"
EMERALD, GOLD = "#34d399", "#d8b25e"
INK, MUTED, LINE = "#f3f4f6", "#9aa1ad", "#262a40"
SANS = "'Segoe UI','Apple SD Gothic Neo','Noto Sans KR','Malgun Gothic',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','Cascadia Code',Consolas,'SFMono-Regular',Menlo,monospace"

HIGHLIGHTS = [  # (value, label, sub)
    ("25", "Publications", "SCIE 6 · KCI 2"),
    ("10", "Patents & SW", "4 patents · 6 registered SW"),
    ("26", "R&D Projects", "national & municipal"),
    ("2023–", "KAIST", "Research Engineer"),
]

ORBITS = [  # (rx, ry, [(angle_deg, label, color)])
    (210, 82, [(200, "Conversational AI", EMERALD), (338, "AI Safety", GOLD), (245, "Prompt Engineering", INDIGO)]),
    (365, 150, [(160, "Time-series Forecasting", INDIGO), (20, "Knowledge Graph · GeoLLM", EMERALD),
                (262, "Lightweight LMs", GOLD)]),
    (530, 222, [(196, "mmWave Indoor Sensing", GOLD), (325, "Distributed Simulation", INDIGO),
                (128, "Digital Twin Healthcare", EMERALD), (52, "Edge AI", INDIGO)]),
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def write(name: str, svg: str) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / name).write_text(re.sub(r"\n\s*\n", "\n", svg).strip() + "\n", encoding="utf-8")
    print(f"  wrote assets/{name} ({len(svg)//1024} KB)")


def starfield(rng: random.Random, w: int, h: int, n: int, pad: int = 0) -> str:
    out = []
    for i in range(n):
        x, y = rng.uniform(pad, w - pad), rng.uniform(pad, h - pad)
        r = rng.choice([0.6, 0.8, 1.0, 1.0, 1.3, 1.7])
        col = rng.choice([INK, INK, INK, INDIGO, EMERALD, GOLD])
        op = rng.uniform(0.35, 0.95)
        tw = ""
        if rng.random() < 0.35:
            tw = f' class="tw" style="animation-delay:{rng.uniform(0, 4):.2f}s;animation-duration:{rng.uniform(2.5, 5):.1f}s"'
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" opacity="{op:.2f}"{tw}/>')
    return "\n".join(out)


BASE_STYLE = """
.tw{animation:tw 3s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}
"""


# ── hero ────────────────────────────────────────────────────────────────────
def build_hero() -> None:
    w, h = 1200, 420
    rng = random.Random(7)
    px, py = 935, 206  # planet / eye centre
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Daeseung Park - AI and Software Systems Engineer at KAIST">
<defs>
  <radialGradient id="bg" cx="78%" cy="30%" r="90%">
    <stop offset="0" stop-color="#1a1f5c"/><stop offset=".45" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/>
  </radialGradient>
  <radialGradient id="neb1" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{INDIGO_D}" stop-opacity=".55"/><stop offset="1" stop-color="{INDIGO_D}" stop-opacity="0"/></radialGradient>
  <radialGradient id="neb2" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{EMERALD}" stop-opacity=".28"/><stop offset="1" stop-color="{EMERALD}" stop-opacity="0"/></radialGradient>
  <radialGradient id="iris" cx="42%" cy="40%" r="62%">
    <stop offset="0" stop-color="#b9ffe4"/><stop offset=".28" stop-color="{EMERALD}"/><stop offset=".62" stop-color="#0f8f68"/><stop offset=".86" stop-color="#16206b"/><stop offset="1" stop-color="#0b0f3a"/>
  </radialGradient>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset=".55" stop-color="{EMERALD}" stop-opacity=".35"/><stop offset="1" stop-color="{EMERALD}" stop-opacity="0"/></radialGradient>
  <linearGradient id="title" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#cfd6ff"/><stop offset="1" stop-color="{INDIGO}"/></linearGradient>
  <linearGradient id="shoot" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
  <clipPath id="card"><rect width="{w}" height="{h}" rx="22"/></clipPath>
  <clipPath id="type"><rect x="70" y="268" height="40" width="0">
    <animate attributeName="width" values="0;470;470" keyTimes="0;.45;1" dur="7s" repeatCount="indefinite"/></rect></clipPath>
</defs>
<style>
{BASE_STYLE}
.spin{{transform-origin:{px}px {py}px;animation:spin 60s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.pulse{{transform-origin:{px}px {py}px;animation:pulse 4s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{transform:scale(1);opacity:.85}}50%{{transform:scale(1.08);opacity:1}}}}
.blink{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.shoot{{animation:shoot 9s ease-in infinite}}
@keyframes shoot{{0%{{transform:translate(0,0);opacity:0}}3%{{opacity:1}}12%{{transform:translate(520px,170px);opacity:0}}100%{{opacity:0;transform:translate(520px,170px)}}}}
.fade{{animation:fade 1.4s ease-out both}}
@keyframes fade{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
</style>
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <ellipse cx="980" cy="120" rx="420" ry="260" fill="url(#neb1)"/>
  <ellipse cx="160" cy="400" rx="380" ry="200" fill="url(#neb2)"/>
  {starfield(rng, w, h, 170)}
  <g class="shoot"><line x1="80" y1="40" x2="190" y2="76" stroke="url(#shoot)" stroke-width="2" stroke-linecap="round"/></g>

  <!-- the green eye planet -->
  <circle cx="{px}" cy="{py}" r="170" fill="url(#glow)" class="pulse"/>
  <g transform="rotate(-16 {px} {py})">
    <ellipse cx="{px}" cy="{py}" rx="190" ry="48" fill="none" stroke="{INDIGO}" stroke-opacity=".35" stroke-width="1.5"/>
  </g>
  <circle cx="{px}" cy="{py}" r="96" fill="url(#iris)"/>
  <g class="spin" opacity=".55">
    {''.join(f'<line x1="{px + 30*math.cos(a):.1f}" y1="{py + 30*math.sin(a):.1f}" x2="{px + 88*math.cos(a):.1f}" y2="{py + 88*math.sin(a):.1f}" stroke="#d6fff0" stroke-opacity="{0.15 + 0.25*((i*7)%5)/4:.2f}" stroke-width="1"/>' for i, a in enumerate([k*math.pi/24 for k in range(48)]))}
  </g>
  <circle cx="{px}" cy="{py}" r="34" fill="#05060f"/>
  <circle cx="{px}" cy="{py}" r="34" fill="none" stroke="{EMERALD}" stroke-opacity=".6" stroke-width="2"/>
  <circle cx="{px-30}" cy="{py-34}" r="13" fill="#fff" opacity=".85"/>
  <circle cx="{px+22}" cy="{py+18}" r="5" fill="#fff" opacity=".5"/>
  <g transform="rotate(-16 {px} {py})">
    <path d="M{px-190},{py} A190,48 0 0 0 {px+190},{py}" fill="none" stroke="{INDIGO}" stroke-width="2.2" stroke-opacity=".9"/>
    <path d="M{px-190},{py} A190,48 0 0 0 {px+190},{py}" fill="none" stroke="{EMERALD}" stroke-width="2.2" stroke-dasharray="40 560" stroke-linecap="round">
      <animate attributeName="stroke-dashoffset" values="600;0" dur="5s" repeatCount="indefinite"/></path>
    <circle r="7" fill="{GOLD}"><animateMotion dur="9s" repeatCount="indefinite" path="M{px-190},{py} A190,48 0 0 0 {px+190},{py} A190,48 0 0 0 {px-190},{py}"/></circle>
  </g>

  <!-- text -->
  <g class="fade">
    <text x="72" y="104" font-family="{MONO}" font-size="15" letter-spacing="4" fill="{EMERALD}">◉ UNIVERSE MAKER · THE GREEN EYE</text>
    <text x="68" y="182" font-family="{SANS}" font-size="70" font-weight="800" fill="url(#title)" letter-spacing="-1">Daeseung Park</text>
    <text x="72" y="226" font-family="{SANS}" font-size="24" fill="{INK}" opacity=".92">AI &amp; Software Systems Engineer <tspan fill="{INDIGO}" font-weight="700">@ KAIST</tspan></text>
  </g>
  <text x="72" y="296" font-family="{SANS}" font-size="22" fill="{MUTED}" clip-path="url(#type)"><tspan fill="{GOLD}" font-family="{MONO}">❯ </tspan>문제의 본질을 코드로 옮기는 일을 합니다.</text>
  <text x="72" y="342" font-family="{MONO}" font-size="14" fill="{MUTED}" opacity=".85" letter-spacing="1">LLM · Time-series · Conversational AI · Knowledge Graph · mmWave Sensing</text>
  <rect x="70" y="372" width="64" height="4" rx="2" fill="{EMERALD}"/><rect x="140" y="372" width="28" height="4" rx="2" fill="{INDIGO}"/><rect x="174" y="372" width="12" height="4" rx="2" fill="{GOLD}"/>
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="22" fill="none" stroke="#ffffff" stroke-opacity=".08"/>
</svg>"""
    write("hero.svg", svg)


# ── highlights ──────────────────────────────────────────────────────────────
def build_highlights() -> None:
    w, h, gap = 1200, 150, 18
    n = len(HIGHLIGHTS)
    tw = (w - gap * (n - 1)) / n
    colors = [EMERALD, INDIGO, GOLD, "#f472b6"]
    tiles = []
    for i, (val, label, sub) in enumerate(HIGHLIGHTS):
        x = i * (tw + gap)
        c = colors[i % len(colors)]
        tiles.append(f"""
<g class="fade" style="animation-delay:{i*0.15:.2f}s">
  <rect x="{x+.5:.1f}" y=".5" width="{tw-1:.1f}" height="{h-1}" rx="16" fill="url(#tile)" stroke="{c}" stroke-opacity=".35"/>
  <rect x="{x+22:.1f}" y="22" width="34" height="4" rx="2" fill="{c}"/>
  <text x="{x+22:.1f}" y="84" font-family="{SANS}" font-size="46" font-weight="800" fill="{INK}">{esc(val)}</text>
  <text x="{x+22:.1f}" y="112" font-family="{SANS}" font-size="17" font-weight="700" fill="{c}">{esc(label)}</text>
  <text x="{x+22:.1f}" y="134" font-family="{SANS}" font-size="13" fill="{MUTED}">{esc(sub)}</text>
  <circle cx="{x+tw-30:.1f}" cy="32" r="4" fill="{c}" class="tw" style="animation-delay:{i*.7:.1f}s"/>
</g>""")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Research output highlights">
<defs><linearGradient id="tile" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#141838"/><stop offset="1" stop-color="{BG0}"/></linearGradient></defs>
<style>{BASE_STYLE}
.fade{{animation:fade 1s ease-out both}}@keyframes fade{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}</style>
{''.join(tiles)}
</svg>"""
    write("highlights.svg", svg)


# ── research orbit map ──────────────────────────────────────────────────────
def build_orbit() -> None:
    w, h = 1200, 560
    cx, cy = 600, 282
    rng = random.Random(42)
    rings, planets, comets = [], [], []
    for k, (rx, ry, items) in enumerate(ORBITS):
        rings.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{INDIGO}" stroke-opacity="{0.38 - k*0.08:.2f}" stroke-width="1.3" stroke-dasharray="{"2 7" if k == 2 else "none"}"/>')
        path = f"M{cx-rx},{cy} A{rx},{ry} 0 1 0 {cx+rx},{cy} A{rx},{ry} 0 1 0 {cx-rx},{cy}"
        dur = 18 + k * 14
        comets.append(f'<circle r="2.6" fill="{INK}" opacity=".9"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{path}"/></circle>')
        comets.append(f'<circle r="2" fill="{EMERALD}" opacity=".8"><animateMotion dur="{dur}s" begin="-{dur/2:.0f}s" repeatCount="indefinite" path="{path}"/></circle>')
        for j, (ang, label, col) in enumerate(items):
            a = math.radians(ang)
            x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
            r = 9 - k
            lw = len(label) * 8.2 + 26
            right = math.cos(a) >= -0.15
            lx = x + 16 if right else x - 16 - lw
            lx = max(8, min(w - 8 - lw, lx))
            ly = y - 15
            delay = rng.uniform(0, 3)
            planets.append(f"""
<g>
  <circle cx="{x:.1f}" cy="{y:.1f}" r="{r*2.4:.1f}" fill="{col}" opacity=".18" class="tw" style="animation-delay:{delay:.2f}s"/>
  <circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>
  <circle cx="{x - r*.35:.1f}" cy="{y - r*.35:.1f}" r="{r*.35:.1f}" fill="#fff" opacity=".55"/>
  <rect x="{lx:.1f}" y="{ly:.1f}" width="{lw:.1f}" height="30" rx="15" fill="#0b0e24" fill-opacity=".88" stroke="{col}" stroke-opacity=".55"/>
  <text x="{lx + lw/2:.1f}" y="{ly + 20:.1f}" text-anchor="middle" font-family="{MONO}" font-size="13.5" fill="{INK}">{esc(label)}</text>
</g>""")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Research universe: Generative AI and LLMs at the core, surrounded by conversational AI, AI safety, time-series forecasting, knowledge graphs, mmWave sensing, distributed simulation and digital twin healthcare">
<defs>
  <radialGradient id="bg" cx="50%" cy="50%" r="70%"><stop offset="0" stop-color="#141a4a"/><stop offset=".6" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></radialGradient>
  <radialGradient id="sun" cx="45%" cy="40%" r="60%"><stop offset="0" stop-color="#fff7d6"/><stop offset=".35" stop-color="{GOLD}"/><stop offset="1" stop-color="#8a5a12"/></radialGradient>
  <radialGradient id="corona" cx="50%" cy="50%" r="50%"><stop offset=".3" stop-color="{GOLD}" stop-opacity=".45"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
  <clipPath id="card"><rect width="{w}" height="{h}" rx="22"/></clipPath>
</defs>
<style>{BASE_STYLE}
.cor{{transform-origin:{cx}px {cy}px;animation:cor 5s ease-in-out infinite}}
@keyframes cor{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.12)}}}}
</style>
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  {starfield(rng, w, h, 120)}
  {''.join(rings)}
  {''.join(comets)}
  <circle cx="{cx}" cy="{cy}" r="88" fill="url(#corona)" class="cor"/>
  <circle cx="{cx}" cy="{cy}" r="46" fill="url(#sun)"/>
  <text x="{cx}" y="{cy+9}" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="800" fill="#2a1a00">LLM</text>
  <text x="{cx}" y="{cy+76}" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{GOLD}">GENERATIVE AI</text>
  {''.join(planets)}
  <text x="28" y="40" font-family="{MONO}" font-size="14" letter-spacing="4" fill="{EMERALD}">◉ RESEARCH UNIVERSE</text>
  <text x="28" y="62" font-family="{SANS}" font-size="13" fill="{MUTED}">closer orbit = closer to the core work</text>
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="22" fill="none" stroke="#ffffff" stroke-opacity=".08"/>
</svg>"""
    write("orbit.svg", svg)


# ── footer ──────────────────────────────────────────────────────────────────
def build_footer() -> None:
    w, h = 1200, 170

    def wave(amp: float, base: float, phase: float) -> str:
        pts = [f"M0,{h}"]
        for x in range(0, w * 2 + 1, 20):
            y = base + amp * math.sin(x / w * 4 * math.pi + phase)
            pts.append(f"L{x},{y:.1f}")
        pts.append(f"L{w*2},{h} Z")
        return " ".join(pts)

    rng = random.Random(3)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Thanks for visiting">
<defs>
  <linearGradient id="g1" x1="0" x2="1"><stop offset="0" stop-color="{EMERALD}"/><stop offset="1" stop-color="{INDIGO_D}"/></linearGradient>
  <linearGradient id="g2" x1="0" x2="1"><stop offset="0" stop-color="{INDIGO_D}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
  <clipPath id="card"><rect width="{w}" height="{h}" rx="22"/></clipPath>
</defs>
<style>{BASE_STYLE}
.w1{{animation:mv 14s linear infinite}}.w2{{animation:mv 9s linear infinite reverse}}
@keyframes mv{{to{{transform:translateX(-{w}px)}}}}
</style>
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="{BG0}"/>
  {starfield(rng, w, 90, 60)}
  <path class="w1" d="{wave(12, 104, 0)}" fill="url(#g2)" opacity=".75"/>
  <path class="w2" d="{wave(10, 124, 1.7)}" fill="url(#g1)" opacity=".85"/>
  <text x="{w/2}" y="58" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="700" fill="{INK}">Thanks for drifting by this corner of the universe</text>
  <text x="{w/2}" y="84" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{MUTED}">DAESEUNGPARK.COM · KAIST · DAEJEON, KOREA</text>
</g>
</svg>"""
    write("footer.svg", svg)


# ── live stats ──────────────────────────────────────────────────────────────
def http_get(url: str, api: bool = False) -> str:
    headers = {"User-Agent": f"{USER}-profile-builder"}
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if api:
        headers["Accept"] = "application/vnd.github+json"
        if tok:
            headers["Authorization"] = f"Bearer {tok}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return r.read().decode("utf-8")


def fetch_contributions(start: dt.date, end: dt.date) -> dict[dt.date, int]:
    page = http_get(f"https://github.com/users/{USER}/contributions?from={start}&to={end}")
    days: dict[str, str] = {}
    for m in re.finditer(r'data-date="(\d{4}-\d{2}-\d{2})"\s+id="([^"]+)"', page):
        days[m.group(2)] = m.group(1)
    counts: dict[dt.date, int] = {}
    for m in re.finditer(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', page):
        if m.group(1) in days:
            t = m.group(2)
            n = 0 if t.startswith("No contribution") else int(re.match(r"([\d,]+)", t).group(1).replace(",", ""))
            counts[dt.date.fromisoformat(days[m.group(1)])] = n
    return counts


def streaks(counts: dict[dt.date, int], today: dt.date) -> tuple[int, int, tuple]:
    longest, run, best_span, start = 0, 0, (None, None), None
    d = min(counts)
    while d <= today:
        if counts.get(d, 0) > 0:
            if run == 0:
                start = d
            run += 1
            if run > longest:
                longest, best_span = run, (start, d)
        else:
            run = 0
        d += dt.timedelta(days=1)
    cur, d = 0, today
    if counts.get(d, 0) == 0:  # today not counted yet → streak still alive from yesterday
        d -= dt.timedelta(days=1)
    while counts.get(d, 0) > 0:
        cur += 1
        d -= dt.timedelta(days=1)
    return cur, longest, best_span


LANG_COLORS = {"Python": "#3572A5", "JavaScript": "#f1e05a", "C#": "#178600", "PHP": "#4F5D95", "C": "#555555",
               "C++": "#f34b7d", "HTML": "#e34c26", "TypeScript": "#3178c6", "Java": "#b07219", "Kotlin": "#A97BFF",
               "CSS": "#663399", "Shell": "#89e051", "Jupyter Notebook": "#DA5B0B", "PowerShell": "#012456"}


def fetch_languages() -> tuple[list[tuple[str, float]], int, int]:
    repos = json.loads(http_get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner", api=True))
    own = [r for r in repos if not r["fork"]]
    stars = sum(r["stargazers_count"] for r in own)
    tally: dict[str, float] = {}
    use_bytes = bool(os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"))
    for r in own:
        if r["name"] == USER:
            continue
        if use_bytes:
            for lang, b in json.loads(http_get(r["languages_url"], api=True)).items():
                tally[lang] = tally.get(lang, 0) + b
        elif r["language"]:
            tally[r["language"]] = tally.get(r["language"], 0) + 1
    total = sum(tally.values()) or 1
    ranked = sorted(((k, v / total) for k, v in tally.items()), key=lambda kv: -kv[1])
    top = ranked[:6]
    rest = sum(v for _, v in ranked[6:])
    if rest > 0.001:
        top.append(("Other", rest))
    return top, len(own), stars


def build_stats() -> None:
    today = dt.date.today()
    allc: dict[dt.date, int] = {}
    for year in range(JOINED.year, today.year + 1):
        allc.update(fetch_contributions(dt.date(year, 1, 1), dt.date(year, 12, 31)))
    allc = {d: n for d, n in allc.items() if d <= today}
    total = sum(allc.values())
    cur, longest, (ls, le) = streaks(allc, today)
    year_ago = today - dt.timedelta(days=364)
    last_year = sum(n for d, n in allc.items() if d >= year_ago)
    langs, n_repos, stars = fetch_languages()

    w, h = 1200, 470
    tiles = [
        (f"{total:,}", "Total contributions", f"since {JOINED:%b %Y}", EMERALD),
        (f"{last_year:,}", "Last 12 months", f"{last_year/52:.0f} per week on average", INDIGO),
        (f"{cur:,}d", "Current streak", "and counting" if cur else "recharging", GOLD),
        (f"{longest:,}d", "Longest streak", f"{ls:%b %Y} – {le:%b %Y}" if ls else "", "#f472b6"),
        (f"{n_repos}", "Original repos", f"★ {stars} stars earned", INK),
    ]
    tw, gap = 212, 12
    tl = []
    for i, (v, lab, sub, c) in enumerate(tiles):
        x = 30 + i * (tw + gap)
        tl.append(f"""<g class="fade" style="animation-delay:{i*.12:.2f}s">
  <rect x="{x}" y="66" width="{tw}" height="112" rx="14" fill="#10142f" stroke="{c}" stroke-opacity=".3"/>
  <text x="{x+18}" y="116" font-family="{SANS}" font-size="34" font-weight="800" fill="{INK}">{esc(v)}</text>
  <text x="{x+18}" y="143" font-family="{SANS}" font-size="14" font-weight="700" fill="{c}">{esc(lab)}</text>
  <text x="{x+18}" y="162" font-family="{SANS}" font-size="12" fill="{MUTED}">{esc(sub)}</text>
</g>""")

    # language bar
    bx, by, bw = 30, 222, 1140
    segs, legend, x = [], [], bx
    for i, (lang, frac) in enumerate(langs):
        sw = bw * frac
        col = LANG_COLORS.get(lang, "#6b7280")
        segs.append(f'<rect x="{x:.1f}" y="{by}" width="{max(sw-2, 1):.1f}" height="12" fill="{col}"/>')
        x += sw
        lx = bx + (i % 7) * 163
        legend.append(f'<circle cx="{lx+6}" cy="{by+38}" r="5" fill="{col}"/><text x="{lx+18}" y="{by+43}" font-family="{SANS}" font-size="13" fill="{INK}">{esc(lang)} <tspan fill="{MUTED}">{frac*100:.1f}%</tspan></text>')

    # heatmap of the last 53 weeks as a starfield
    start = today - dt.timedelta(days=today.weekday() + 1 + 52 * 7) if today.weekday() != 6 else today - dt.timedelta(days=52 * 7)
    levels = ["#1a1f3d", "#25307a", INDIGO_D, INDIGO, EMERALD]
    nz = sorted(n for d, n in allc.items() if d >= start and n > 0) or [1]
    quart = [nz[int(len(nz) * f)] for f in (0.25, 0.5, 0.75)]
    dots, d = [], start
    hx, hy, cs = 34, 312, 21.4
    while d <= today:
        col_i = (d - start).days // 7
        row = (d.weekday() + 1) % 7
        n = allc.get(d, 0)
        lv = 0 if n == 0 else 1 + sum(n > q for q in quart)  # GitHub-style quartiles
        r = 3.2 if lv == 0 else 3.6 + lv * 0.9
        cxp, cyp = hx + col_i * cs + 6, hy + row * 21 + 6
        tw_ = f' class="tw" style="animation-delay:{(col_i*7+row)%37/9:.2f}s"' if lv >= 4 else ""
        dots.append(f'<circle cx="{cxp:.1f}" cy="{cyp}" r="{r:.1f}" fill="{levels[lv]}"{tw_}><title>{d}: {n}</title></circle>')
        d += dt.timedelta(days=1)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="GitHub stats: {total} total contributions, current streak {cur} days, longest streak {longest} days">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
<clipPath id="bar"><rect x="{bx}" y="{by}" width="{bw}" height="12" rx="6"/></clipPath><clipPath id="card"><rect width="{w}" height="{h}" rx="22"/></clipPath></defs>
<style>{BASE_STYLE}
.fade{{animation:fade 1s ease-out both}}@keyframes fade{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.grow{{animation:grow 1.6s cubic-bezier(.2,.8,.2,1) both;transform-origin:{bx}px 0}}@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}</style>
<g clip-path="url(#card)">
<rect width="{w}" height="{h}" fill="url(#bg)"/>
<text x="30" y="42" font-family="{MONO}" font-size="14" letter-spacing="4" fill="{EMERALD}">◉ MISSION TELEMETRY</text>
<text x="{w-30}" y="42" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">synced {today:%Y-%m-%d} · github.com/{USER}</text>
{''.join(tl)}
<text x="30" y="210" font-family="{SANS}" font-size="13" font-weight="700" fill="{MUTED}" letter-spacing="1">LANGUAGES</text>
<g clip-path="url(#bar)"><g class="grow">{''.join(segs)}</g></g>
{''.join(legend)}
<text x="30" y="302" font-family="{SANS}" font-size="13" font-weight="700" fill="{MUTED}" letter-spacing="1">LAST 53 WEEKS · EVERY STAR IS A DAY</text>
{''.join(dots)}
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="22" fill="none" stroke="#ffffff" stroke-opacity=".08"/>
</svg>"""
    write("stats.svg", svg)
    print(f"  total={total} last_year={last_year} streak={cur} longest={longest} ({ls}~{le}) repos={n_repos} stars={stars}")


if __name__ == "__main__":
    only_stats = "--stats" in sys.argv
    if not only_stats:
        build_hero(); build_highlights(); build_orbit(); build_footer()
    build_stats()

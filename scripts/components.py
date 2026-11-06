"""Self-hosted SVG components for the profile README.

Nothing here touches a third-party image host: every badge, icon and card is
written into ../assets and served from this repository, so GitHub's image proxy
never has a remote server to time out on. Glyphs in scripts/icons come from
simple-icons (CC0) and are vendored as plain path data.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ICONS = Path(__file__).resolve().parent / "icons"
BG0, BG1 = "#070914", "#0d1030"
INDIGO, INDIGO_D = "#8b9bff", "#3a4cf0"
EMERALD, GOLD, PINK, CYAN = "#34d399", "#d8b25e", "#f472b6", "#22d3ee"
INK, MUTED = "#f3f4f6", "#a4abb8"
SANS = "'Segoe UI','Apple SD Gothic Neo','Noto Sans KR','Malgun Gothic',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','Cascadia Code',Consolas,'SFMono-Regular',Menlo,monospace"
_PATH_OK = re.compile(r"^[MmZzLlHhVvCcSsQqTtAa0-9eE.,\s+-]+$")

# ── content ─────────────────────────────────────────────────────────────────
BUTTONS = [  # file, icon, colour, label, sub
    ("website", "googlechrome", INDIGO, "Website", "daeseungpark.com"),
    ("scholar", "googlescholar", "#8ab4f8", "Scholar", "Google Scholar"),
    ("orcid", "orcid", "#a6ce39", "ORCID", "0009-0002-3044-2689"),
    ("linkedin", "linkedin", "#6aa9ff", "LinkedIn", "in/daeseungpark"),
    ("huggingface", "huggingface", "#ffd21e", "Hugging Face", "daeseungpark"),
    ("docker", "docker", "#39a7f0", "Docker Hub", "daeseungpark"),
    ("blog", "rss", EMERALD, "Blog", "codespectrum.net"),
    ("email", "maildotru", GOLD, "Email", "dspark@daeseungpark.com"),
    ("kofi", "kofi", "#ff7a77", "Ko-fi", "ko-fi.com/daeseungpark"),
    ("bmc", "buymeacoffee", "#ffdd00", "Buy Me a Coffee", "buymeacoffee.com"),
]

SECTIONS = [  # file, number, title, sub
    ("research", "01", "Research Universe", "what I orbit"),
    ("signals", "02", "Latest Transmissions", "news from the lab"),
    ("journal", "03", "From the Journal", "auto-synced from daeseungpark.com"),
    ("work", "04", "Featured Work", "built and shipped"),
    ("stack", "05", "The Periodic Table of My Stack", "40 elements"),
    ("telemetry", "06", "Mission Telemetry", "refreshed daily"),
    ("fuel", "07", "Fuel the Rocket", "support my side quests"),
]

SIGNALS = [  # file, tag, kicker, colour, title, sub
    ("ieee", "NEW", "JOURNAL PAPER", EMERALD, "IEEE Access", "Distributed mmWave radar for indoor human detection & geo-referencing"),
    ("iceccme", "TALK", "CONFERENCE", GOLD, "ICECCME 2026 · Bali", "Predictive load-balancing simulation with spatiotemporal GNNs · Oct 15–17"),
    ("abliterated", "TRY", "PUBLIC TRIAL", PINK, "Abliterated AI", "Public trial of an abliterated (uncensored) model for AI-safety research"),
    ("rchat", "LAB", "RESEARCH TOOL", INDIGO, "LLM Research Platform", "Hosted workbench for testing and comparing LLMs"),
]

CARDS = [  # file, kicker, colour, title, description, chips (icon|None, label), repo|None
    ("addresskg", "KNOWLEDGE GRAPH", EMERALD, "AddressKG",
     "National address knowledge graph built on a national-standard ontology.",
     [("neo4j", "Neo4j"), ("fastapi", "FastAPI"), ("python", "Python")], None),
    ("citysafety", "MULTIMODAL AI", GOLD, "City-Safety AI API",
     "Multimodal LLM serving for disaster perception across video, sensor, spatial and text data.",
     [(None, "Multimodal LLM"), ("docker", "Serving")], None),
    ("llm-platform", "LLM WORKBENCH", INDIGO, "Universal LLM Test Platform",
     "Bring-your-own-key workbench for any OpenAI-compatible API: RAG, agents, evaluation and a full request inspector.",
     [("javascript", "JavaScript"), (None, "RAG")], "Universal-LLM-Test-Research-Platform"),
    ("sso", "SECURITY", PINK, "Universal Login & SSO",
     "Sign in once and receive per-service secrets from the server, so API keys never ship in your frontend.",
     [("php", "PHP"), ("mysql", "MySQL")], "Universal-Login-SSO-Server"),
    ("unslop", "WRITING TOOL", CYAN, "Unslop",
     "AI copy-editing for work and research documents. 업무·연구자 전용 AI 윤문 도구.",
     [("python", "Python"), (None, "LLM")], "Unslop"),
    ("ai-office", "WORKSPACE", EMERALD, "AI Office",
     "DSPark's AI Office: a personal, self-hosted AI workspace.",
     [("javascript", "JavaScript"), (None, "Agents")], "AI-Office"),
    ("eyedrive", "WINDOWS TOOL", GOLD, "EyeDrive",
     "Mount a WebDAV server as a real local drive on Windows 10/11, built on rclone.",
     [("csharp", "C#"), ("dotnet", ".NET")], "EyeDrive"),
    ("resswitch", "WINDOWS TOOL", INDIGO, "ResSwitch",
     "One-click and scheduled resolution switching for Chrome Remote Desktop, with multi-monitor profiles.",
     [("csharp", "C#"), ("dotnet", ".NET")], "Display-Resolution-Changer-ResSwitch"),
]

STACK = [  # group, colour, [(icon, name, glyph colour)]
    ("AI / ML", EMERALD, [("python", "Python", "#ffd43b"), ("pytorch", "PyTorch", "#ff6a3d"),
                          ("tensorflow", "TensorFlow", "#ff9f1c"), ("scikitlearn", "scikit-learn", "#f7931e"),
                          ("opencv", "OpenCV", "#7cc3ff"), ("huggingface", "Hugging Face", "#ffd21e"),
                          ("pandas", "pandas", "#c4b5fd")]),
    ("Languages", INDIGO, [("c", "C", "#8fb3e8"), ("cplusplus", "C++", "#6aa9ff"), ("csharp", "C#", "#b794f6"),
                           ("openjdk", "Java", "#f5a97f"), ("kotlin", "Kotlin", "#b79dff"),
                           ("javascript", "JavaScript", "#f7df1e"), ("php", "PHP", "#a5b4fc"),
                           ("gnubash", "Bash", "#86efac")]),
    ("Backend & Data", GOLD, [("fastapi", "FastAPI", "#2dd4bf"), ("laravel", "Laravel", "#ff6b5e"),
                              ("nginx", "NGINX", "#4ade80"), ("mysql", "MySQL", "#7dd3fc"),
                              ("mariadb", "MariaDB", "#d6a97c"), ("postgresql", "PostgreSQL", "#93c5fd"),
                              ("sqlite", "SQLite", "#7dd3fc"), ("oracle", "Oracle", "#ff6b5e"),
                              ("neo4j", "Neo4j", "#60a5fa")]),
    ("Infra & Cloud", PINK, [("docker", "Docker", "#39a7f0"), ("kubernetes", "Kubernetes", "#6d9eff"),
                             ("jenkins", "Jenkins", "#f0a58a"), ("linux", "Linux", "#fde68a"),
                             ("git", "Git", "#ff7a59"), ("amazonwebservices", "AWS", "#ffb84d"),
                             ("microsoftazure", "Azure", "#5cb8ff"), ("googlecloud", "Google Cloud", "#7fb0ff"),
                             ("firebase", "Firebase", "#ffca28")]),
    ("Devices & Apps", CYAN, [("arduino", "Arduino", "#2dd4bf"), ("android", "Android", "#4ade80"),
                              ("dotnet", ".NET", "#a78bfa"), ("html5", "HTML5", "#ff7a4d"),
                              ("css3", "CSS3", "#60a5fa"), ("bootstrap", "Bootstrap", "#b794f6"),
                              ("zapier", "Zapier", "#ff7a33")]),
]

WHOAMI = [
    ("name", "Daeseung Park (박대승)"),
    ("alias", "Universe Maker · The Green Eye"),
    ("role", "AI & Software Systems Engineer"),
    ("lab", "KAIST · Convergence Research Center"),
    ("base", "Daejeon, Korea"),
    ("focus", "LLM · Time-series · Conversational AI · Knowledge Graph · mmWave"),
    ("motto", "문제의 본질을 코드로 옮긴다."),
    ("reach", "dspark@daeseungpark.com · dspark@kaist.ac.kr"),
    ("side", "Small, useful tools, shipped right here."),
]


# ── helpers ─────────────────────────────────────────────────────────────────
def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def glyph(name: str, x: float, y: float, size: float, fill: str) -> str:
    src = (ICONS / f"{name}.svg").read_text(encoding="utf-8")
    d = re.search(r'<path[^>]*?\sd="([^"]+)"', src).group(1)
    if not _PATH_OK.match(d):
        raise ValueError(f"unexpected path data in {name}.svg")
    return f'<path transform="translate({x:.1f} {y:.1f}) scale({size/24:.4f})" d="{d}" fill="{fill}"/>'


def text_width(s: str, size: float) -> float:
    return sum(size * (1.0 if ord(c) > 0x2E80 else 0.55) for c in s)


def wrap(s: str, size: float, max_w: float, max_lines: int) -> list[str]:
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if text_width(trial, size) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" ,.;:") + "…"
    return lines


def fit(s: str, size: float, max_w: float) -> str:
    return wrap(s, size, max_w, 1)[0]


def frame(w: int, h: int, label: str, style: str, body: str, defs: str = "", r: int = 18) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">
<defs><clipPath id="c"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>{defs}</defs>
<style>{style}</style>
<g clip-path="url(#c)">{body}</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="#fff" stroke-opacity=".09"/>
</svg>"""


def surface(w: int, h: int, accent: str) -> tuple[str, str]:
    defs = f"""<linearGradient id="s" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#141838"/><stop offset="1" stop-color="{BG0}"/></linearGradient>
<radialGradient id="o"><stop offset="0" stop-color="{accent}" stop-opacity=".30"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>"""
    body = f'<rect width="{w}" height="{h}" fill="url(#s)"/><ellipse cx="{w*.92:.0f}" cy="0" rx="{w*.42:.0f}" ry="{h*.95:.0f}" fill="url(#o)"/>'
    return defs, body


SHINE = """.sh{animation:sh 7s ease-in-out infinite}
@keyframes sh{0%,62%{transform:translateX(-120%) skewX(-20deg)}100%{transform:translateX(140%) skewX(-20deg)}}"""


# ── builders ────────────────────────────────────────────────────────────────
def build_buttons(write) -> None:
    w, h = 300, 88
    for i, (slug, icon, col, label, sub) in enumerate(BUTTONS):
        defs, base = surface(w, h, col)
        body = f"""{base}
<circle cx="46" cy="44" r="27" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".5"/>
{glyph(icon, 31, 29, 30, col)}
<text x="86" y="41" font-family="{SANS}" font-size="23" font-weight="700" fill="{INK}">{esc(label)}</text>
<text x="86" y="65" font-family="{MONO}" font-size="14" fill="{MUTED}">{esc(sub)}</text>
<rect class="sh" style="animation-delay:{i*.35:.2f}s" width="{w*.5:.0f}" height="{h}" fill="url(#sh)"/>"""
        write(f"btn-{slug}.svg", frame(w, h, f"{label}: {sub}", SHINE, body, defs))


def build_sections(write) -> None:
    w, h = 1200, 76
    for slug, num, title, sub in SECTIONS:
        defs = f'<linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{EMERALD}"/><stop offset=".5" stop-color="{INDIGO}"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>'
        style = ".ln{animation:ln 1.6s cubic-bezier(.2,.8,.2,1) both;transform-origin:0 0}@keyframes ln{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        body = f"""<rect width="{w}" height="{h}" fill="{BG0}"/>
<text x="26" y="48" font-family="{MONO}" font-size="24" font-weight="700" fill="{EMERALD}">{num}</text>
<text x="74" y="50" font-family="{SANS}" font-size="31" font-weight="800" fill="{INK}">{esc(title)}</text>
<text x="{w-26}" y="46" text-anchor="end" font-family="{MONO}" font-size="16" fill="{MUTED}">{esc(sub)}</text>
<rect class="ln" y="{h-4}" width="{w}" height="4" fill="url(#l)"/>"""
        write(f"sec-{slug}.svg", frame(w, h, f"{num}. {title}", style, body, defs, r=14))


def strip(write, name: str, left: str, col: str, kicker: str, title: str, sub: str) -> None:
    w, h = 1200, 128
    defs, base = surface(w, h, col)
    latin = all(ord(c) < 0x2E80 for c in kicker)
    k_attr = f'font-family="{MONO}" letter-spacing="2"' if latin else f'font-family="{SANS}"'
    style = SHINE + ".ar{animation:ar 2.4s ease-in-out infinite}@keyframes ar{50%{transform:translateX(8px)}}"
    body = f"""{base}
<rect x="24" y="24" width="96" height="80" rx="14" fill="{col}" fill-opacity=".13" stroke="{col}" stroke-opacity=".55"/>
<text x="72" y="74" text-anchor="middle" font-family="{MONO}" font-size="24" font-weight="700" fill="{col}">{esc(left)}</text>
<text x="146" y="40" {k_attr} font-size="15" fill="{col}">{esc(kicker)}</text>
<text x="146" y="74" font-family="{SANS}" font-size="29" font-weight="700" fill="{INK}">{esc(fit(title, 29, 950))}</text>
<text x="146" y="104" font-family="{SANS}" font-size="19" fill="{MUTED}">{esc(fit(sub, 19, 950))}</text>
<text class="ar" x="{w-62}" y="76" font-family="{SANS}" font-size="32" fill="{col}">→</text>
<rect class="sh" width="{w*.3:.0f}" height="{h}" fill="url(#sh)"/>"""
    write(name, frame(w, h, f"{title} - {sub}", style, body, defs))


def build_signals(write) -> None:
    for slug, tag, kicker, col, title, sub in SIGNALS:
        strip(write, f"signal-{slug}.svg", tag, col, kicker, title, sub)


def build_journal(write, articles: list[dict]) -> None:
    cols = [EMERALD, INDIGO, GOLD]
    for i, a in enumerate(articles):
        strip(write, f"journal-{i+1}.svg", f"#{a['num']}", cols[i % 3],
              " · ".join(x for x in (a["cat"], a["read"]) if x), a["title"], a["sub"])


def build_cards(write, stars: dict[str, int]) -> None:
    w, h = 600, 300
    for slug, kicker, col, title, desc, chips, repo in CARDS:
        defs, base = surface(w, h, col)
        lines = wrap(desc, 20, w - 60, 3)
        desc_svg = "".join(f'<text x="30" y="{130 + i*29}" font-family="{SANS}" font-size="20" fill="{MUTED}">{esc(l)}</text>'
                           for i, l in enumerate(lines))
        x, chip_svg = 30.0, ""
        for icon, label in chips:
            lw = text_width(label, 15) + (54 if icon else 30)
            chip_svg += f'<rect x="{x:.1f}" y="238" width="{lw:.1f}" height="36" rx="18" fill="#fff" fill-opacity=".05" stroke="{col}" stroke-opacity=".45"/>'
            tx = x + 15
            if icon:
                chip_svg += glyph(icon, x + 13, 247, 18, col)
                tx = x + 39
            chip_svg += f'<text x="{tx:.1f}" y="262" font-family="{MONO}" font-size="15" fill="{INK}">{esc(label)}</text>'
            x += lw + 10
        n = stars.get(repo, 0) if repo else 0
        star = f'<text x="{w-30}" y="44" text-anchor="end" font-family="{MONO}" font-size="17" font-weight="700" fill="{GOLD}">★ {n}</text>' if n else ""
        body = f"""{base}
<rect x="30" y="26" width="34" height="4" rx="2" fill="{col}"/>
<text x="30" y="56" font-family="{MONO}" font-size="15" letter-spacing="2" fill="{col}">{esc(kicker)}</text>
<text x="30" y="96" font-family="{SANS}" font-size="31" font-weight="800" fill="{INK}">{esc(title)}</text>
{star}{desc_svg}{chip_svg}
<rect class="sh" width="{w*.4:.0f}" height="{h}" fill="url(#sh)"/>"""
        write(f"card-{slug}.svg", frame(w, h, f"{title}: {desc}", SHINE, body, defs))


def build_stack(write) -> None:
    cols, pad, gap = 10, 26, 8
    w = 1200
    t = (w - 2 * pad - gap * (cols - 1)) / cols
    top = 74
    rows = (sum(len(g[2]) for g in STACK) + cols - 1) // cols
    h = int(top + rows * (t + gap) + 18)
    legend, tiles, i, x = "", "", 0, float(pad)
    for group, col, items in STACK:
        lw = text_width(group, 16) + 56
        legend += f'<rect x="{x:.0f}" y="24" width="16" height="16" rx="4" fill="{col}"/><text x="{x+24:.0f}" y="38" font-family="{SANS}" font-size="16" font-weight="600" fill="{INK}">{esc(group)}</text>'
        x += lw
        for icon, name, gc in items:
            r, c = divmod(i, cols)
            tx, ty = pad + c * (t + gap), top + r * (t + gap)
            tiles += f"""<g>
<rect x="{tx:.1f}" y="{ty:.1f}" width="{t:.1f}" height="{t:.1f}" rx="12" fill="{col}" fill-opacity=".06" stroke="{col}" stroke-opacity=".32"/>
<rect class="sw" style="animation-delay:{(c + r)*.14:.2f}s" x="{tx:.1f}" y="{ty:.1f}" width="{t:.1f}" height="{t:.1f}" rx="12" fill="{col}" fill-opacity=".16" stroke="{col}"/>
<text x="{tx+9:.1f}" y="{ty+18:.1f}" font-family="{MONO}" font-size="12" fill="{col}">{i+1}</text>
{glyph(icon, tx + t/2 - 21, ty + 22, 42, gc)}
<text x="{tx+t/2:.1f}" y="{ty+t-11:.1f}" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="600" fill="{INK}">{esc(name)}</text>
</g>"""
            i += 1
    style = ".sw{opacity:0;animation:sw 9s ease-in-out infinite}@keyframes sw{0%,16%,100%{opacity:0}6%{opacity:1}}"
    body = f'<rect width="{w}" height="{h}" fill="{BG0}"/>{legend}{tiles}'
    names = ", ".join(n for _, _, g in STACK for _, n, _ in g)
    write("stack.svg", frame(w, h, f"Tech stack: {names}", style, body))


def build_whoami(write) -> None:
    w, h = 1200, 92 + 40 * (len(WHOAMI) + 2)
    rows = ""
    y = 106
    rows += f'<g class="l" style="animation-delay:.2s"><text x="34" y="{y}" font-family="{MONO}" font-size="22" fill="{INK}"><tspan fill="{EMERALD}">dspark@kaist</tspan><tspan fill="{MUTED}">:~$ </tspan>whoami --verbose</text></g>'
    for i, (k, v) in enumerate(WHOAMI):
        y += 40
        col = GOLD if k == "motto" else INK
        rows += f'<g class="l" style="animation-delay:{.7 + i*.16:.2f}s"><text x="34" y="{y}" font-family="{MONO}" font-size="21" fill="{INDIGO}">{k}</text><text x="170" y="{y}" font-family="{SANS}" font-size="22" fill="{col}">{esc(v)}</text></g>'
    y += 40
    delay = .9 + len(WHOAMI) * .16
    rows += f'<g class="l" style="animation-delay:{delay:.2f}s"><text x="34" y="{y}" font-family="{MONO}" font-size="22"><tspan fill="{EMERALD}">dspark@kaist</tspan><tspan fill="{MUTED}">:~$ </tspan></text><rect class="b" x="248" y="{y-19}" width="12" height="23" fill="{EMERALD}"/></g>'
    bar = f'<rect width="{w}" height="50" fill="#141838"/>' + "".join(
        f'<circle cx="{32 + i*24}" cy="25" r="7" fill="{c}"/>' for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"])
    ) + f'<text x="{w/2}" y="31" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{MUTED}">~/universe</text>'
    style = """.l{animation:in .35s ease-out backwards}@keyframes in{from{opacity:0}}
.b{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}"""
    alt = "; ".join(f"{k}: {v}" for k, v in WHOAMI)
    write("whoami.svg", frame(w, h, alt, style, f'<rect width="{w}" height="{h}" fill="{BG0}"/>{bar}{rows}'))

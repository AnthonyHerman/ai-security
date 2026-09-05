#!/usr/bin/env python3
"""Regenerate the corpus statistics for the README.

Counts every link in the category READMEs, rebuilds the SVG charts in assets/,
and rewrites the blocks between the STATS / TOC markers in README.md.

Usage: python3 scripts/stats.py
"""
import collections
import datetime as dt
import json
import math
import os
import random
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
ASSETS = ROOT / "assets"
LINK = re.compile(r"^- \[([^\]]+)\]\((https?://[^)\s]+)\)")
URL = re.compile(r"https?://[^\s)>\"']+")

GROUPS = {
    "Foundations": ("#7c83ff", "🧱"), "Attacks": ("#ff3b6b", "💥"), "Defense": ("#2ee38a", "🛡️"),
    "Agents": ("#00d4ff", "🤖"), "Coding": ("#ffb020", "⌨️"), "Research": ("#c77dff", "📚"),
    "Practice": ("#ff7a45", "🎯"), "General": ("#9aa4b2", "📰"),
}
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def fmt(n):
    return f"{n:,}"


# ---------------------------------------------------------------- corpus
def parse_toc(text):
    """Return [(group, [(category, path, desc), ...]), ...] from the TOC block (list or table form)."""
    m = re.search(r"<!-- TOC:START -->(.*?)<!-- TOC:END -->", text, re.S)
    block = m.group(1) if m else text
    groups, cur = [], None
    for line in block.split("\n"):
        h = re.match(r"^### (?:\S+ )?([A-Za-z]+)", line)
        if h and h.group(1) in GROUPS:
            cur = (h.group(1), [])
            groups.append(cur)
            continue
        if not cur:
            continue
        r = re.match(r"^- \[([^\]]+)\]\(([^)]+/README\.md)\) -- (.*)$", line) or \
            re.match(r"^\| \[([^\]]+)\]\(([^)]+/README\.md)\) \| [^|]* \| [^|]* \| (.*?) \|$", line)
        if r:
            cur[1].append((r.group(1), r.group(2), r.group(3).strip()))
    return groups


def scan(groups):
    cats, all_urls, domains = [], set(), collections.Counter()
    for g, items in groups:
        for cat, path, desc in items:
            urls, secs, cur = set(), [], None
            for line in (ROOT / path).read_text().split("\n"):
                if line.startswith("## "):
                    cur = [line[3:].strip(), 0]
                    secs.append(cur)
                m = LINK.match(line)
                if m:
                    u = m.group(2)
                    if cur:
                        cur[1] += 1
                    if u not in all_urls and u not in urls:
                        domains[re.sub(r"^https?://(www\.)?", "", u).split("/")[0].lower()] += 1
                    urls.add(u)
            cats.append({"group": g, "name": cat, "path": path, "desc": desc, "links": len(urls), "sections": secs})
            all_urls |= urls
    return cats, all_urls, domains


def sources(domains):
    buckets = collections.OrderedDict([("GitHub", 0), ("arXiv", 0), ("X / Twitter", 0), ("YouTube", 0), ("Everything else", 0)])
    for d, n in domains.items():
        if d in ("github.com", "gist.github.com"):
            buckets["GitHub"] += n
        elif d.endswith("arxiv.org"):
            buckets["arXiv"] += n
        elif d in ("x.com", "twitter.com"):
            buckets["X / Twitter"] += n
        elif d in ("youtube.com", "youtu.be"):
            buckets["YouTube"] += n
        else:
            buckets["Everything else"] += n
    return buckets


def growth():
    cache_p = ASSETS / "growth.json"
    cache = json.loads(cache_p.read_text()) if cache_p.exists() else {}
    log = subprocess.run(["git", "log", "--reverse", "--format=%H %ad", "--date=short"], cwd=ROOT,
                         capture_output=True, text=True).stdout.split("\n")
    rows = []
    for line in log:
        if not line.strip():
            continue
        sha, date = line.split()
        if sha not in cache:
            out = subprocess.run(["git", "grep", "-h", "-o", "-E", r"https?://[^ )>\"'|]+", sha, "--", "*.md",
                                  ":(exclude)README.md", ":(exclude)vault", ":(exclude).claude", ":(exclude)agents.md"],
                                 cwd=ROOT, capture_output=True, text=True).stdout
            cache[sha] = [date, len(set(out.split()))]
        rows.append((cache[sha][0], cache[sha][1]))
    cache_p.write_text(json.dumps(cache, indent=0))
    return rows


def recent(n=8):
    out = subprocess.run(["git", "log", "-p", "-n", "15", "--format=%x00%ad", "--date=short", "--", "*.md",
                          ":(exclude)vault", ":(exclude)README.md", ":(exclude).claude"],
                         cwd=ROOT, capture_output=True, text=True).stdout
    items, seen, date = [], set(), ""
    for line in out.split("\n"):
        if line.startswith("\x00"):
            date = line[1:].strip()
        m = LINK.match(line[1:]) if line.startswith("+- [") else None
        if m and m.group(2) not in seen:
            seen.add(m.group(2))
            items.append((date, m.group(1), m.group(2)))
        if len(items) >= n:
            break
    return items


# ---------------------------------------------------------------- svg
def theme(dark):
    return dict(bg="#0b0e14" if dark else "#ffffff", fg="#e6edf3" if dark else "#1f2328", muted="#8b949e" if dark else "#656d76",
                grid="#21262d" if dark else "#d0d7de", track="#161b22" if dark else "#f6f8fa")


def svg_categories(cats, dark):
    t = theme(dark)
    order = [g for g in GROUPS]
    W, rowh, pad = 960, 22, 24
    groups = collections.OrderedDict((g, [c for c in cats if c["group"] == g]) for g in order)
    n = sum(len(v) + 1 for v in groups.values())
    H = pad * 2 + n * rowh + len(groups) * 8
    mx = max(c["links"] for c in cats)
    x0, barw = 250, W - 250 - 90
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{SANS}">',
         f'<rect width="{W}" height="{H}" rx="12" fill="{t["bg"]}"/>']
    y = pad
    for g, items in groups.items():
        color = GROUPS[g][0]
        total = sum(c["links"] for c in items)
        o.append(f'<text x="{x0 - 10}" y="{y + 15}" text-anchor="end" font-size="13" font-weight="700" fill="{color}">{esc(g.upper())}</text>')
        o.append(f'<text x="{x0}" y="{y + 15}" font-size="12" fill="{t["muted"]}">{fmt(total)} links · {len(items)} categories</text>')
        o.append(f'<line x1="{x0}" y1="{y + rowh - 2}" x2="{W - pad}" y2="{y + rowh - 2}" stroke="{t["grid"]}"/>')
        y += rowh
        for c in sorted(items, key=lambda c: -c["links"]):
            w = max(2, barw * c["links"] / mx)
            o.append(f'<text x="{x0 - 10}" y="{y + 15}" text-anchor="end" font-size="13" fill="{t["fg"]}">{esc(c["name"])}</text>')
            o.append(f'<rect x="{x0}" y="{y + 4}" width="{barw}" height="{rowh - 8}" rx="4" fill="{t["track"]}"/>')
            o.append(f'<rect x="{x0}" y="{y + 4}" width="{w:.1f}" height="{rowh - 8}" rx="4" fill="{color}" opacity="0.9"/>')
            o.append(f'<text x="{x0 + w + 8:.1f}" y="{y + 15}" font-size="12" font-family="{MONO}" fill="{t["fg"]}">{fmt(c["links"])}</text>')
            y += rowh
        y += 8
    o.append("</svg>")
    return "\n".join(o)


def svg_growth(rows, dark):
    t = theme(dark)
    W, H, L, R, T, B = 620, 300, 56, 24, 28, 44
    pts = []
    for d, n in rows:
        pts.append((dt.date.fromisoformat(d).toordinal(), n))
    x_min, x_max = pts[0][0], max(pts[-1][0], pts[0][0] + 1)
    y_max = max(n for _, n in pts) or 1
    X = lambda x: L + (W - L - R) * (x - x_min) / (x_max - x_min)
    Y = lambda y: T + (H - T - B) * (1 - y / y_max)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{SANS}">',
         f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2ee38a" stop-opacity="0.55"/><stop offset="1" stop-color="#2ee38a" stop-opacity="0.02"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" rx="12" fill="{t["bg"]}"/>',
         f'<text x="{L}" y="18" font-size="13" font-weight="700" fill="{t["fg"]}">Unique URLs over time</text>']
    for k in range(5):
        yv = y_max * k / 4
        o.append(f'<line x1="{L}" y1="{Y(yv):.1f}" x2="{W - R}" y2="{Y(yv):.1f}" stroke="{t["grid"]}" stroke-dasharray="2 4"/>')
        o.append(f'<text x="{L - 8}" y="{Y(yv) + 4:.1f}" text-anchor="end" font-size="11" font-family="{MONO}" fill="{t["muted"]}">{fmt(int(yv))}</text>')
    d0 = dt.date.fromordinal(x_min)
    m = dt.date(d0.year, d0.month, 1)
    while m.toordinal() <= x_max:
        if m.month in (1, 4, 7, 10):
            xx = X(max(m.toordinal(), x_min))
            o.append(f'<text x="{xx:.1f}" y="{H - B + 18}" text-anchor="middle" font-size="11" font-family="{MONO}" fill="{t["muted"]}">{m.strftime("%b %y")}</text>')
        m = dt.date(m.year + (m.month == 12), 1 if m.month == 12 else m.month + 1, 1)
    # step line (count only changes at commits)
    path, prev = [], None
    for x, n in pts:
        if prev is None:
            path.append(f"M{X(x):.1f},{Y(n):.1f}")
        else:
            path.append(f"L{X(x):.1f},{Y(prev):.1f} L{X(x):.1f},{Y(n):.1f}")
        prev = n
    line = " ".join(path)
    area = f"{line} L{X(x_max):.1f},{Y(prev):.1f} L{X(x_max):.1f},{Y(0):.1f} L{X(x_min):.1f},{Y(0):.1f} Z"
    o.append(f'<path d="{area}" fill="url(#g)"/>')
    o.append(f'<path d="{line} L{X(x_max):.1f},{Y(prev):.1f}" fill="none" stroke="#2ee38a" stroke-width="2.5" stroke-linejoin="round"/>')
    # biggest jump annotation
    jumps = [(pts[i][1] - pts[i - 1][1], i) for i in range(1, len(pts))]
    if jumps:
        delta, i = max(jumps)
        if delta > 0:
            xx, yy = X(pts[i][0]), Y(pts[i][1])
            o.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="4" fill="{t["bg"]}" stroke="#2ee38a" stroke-width="2"/>')
            label = f"+{fmt(delta)} in one commit"
            lx = xx - 12
            o.append(f'<text x="{lx:.1f}" y="{yy + 18:.1f}" text-anchor="end" font-size="11" font-family="{MONO}" fill="{t["fg"]}">{esc(label)}</text>')
    o.append(f'<text x="{W - R}" y="{Y(prev) - 8:.1f}" text-anchor="end" font-size="20" font-weight="800" font-family="{MONO}" fill="#2ee38a">{fmt(prev)}</text>')
    o.append("</svg>")
    return "\n".join(o)


def svg_sources(buckets, dark):
    t = theme(dark)
    W, H = 320, 300
    total = sum(buckets.values()) or 1
    colors = ["#e6edf3" if dark else "#24292f", "#c77dff", "#00d4ff", "#ff3b6b", "#8b949e"]
    cx, cy, r, sw = 100, 150, 70, 26
    C = 2 * math.pi * r
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{SANS}">',
         f'<rect width="{W}" height="{H}" rx="12" fill="{t["bg"]}"/>',
         f'<text x="24" y="18" font-size="13" font-weight="700" fill="{t["fg"]}">Where the links point</text>',
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["track"]}" stroke-width="{sw}"/>']
    off = 0.0
    for (name, n), col in zip(buckets.items(), colors):
        seg = C * n / total
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-dasharray="{seg:.2f} {C - seg:.2f}" stroke-dashoffset="{-off:.2f}" transform="rotate(-90 {cx} {cy})"/>')
        off += seg
    o.append(f'<text x="{cx}" y="{cy - 4}" text-anchor="middle" font-size="22" font-weight="800" font-family="{MONO}" fill="{t["fg"]}">{fmt(total)}</text>')
    o.append(f'<text x="{cx}" y="{cy + 16}" text-anchor="middle" font-size="11" fill="{t["muted"]}">links</text>')
    y = 70
    for (name, n), col in zip(buckets.items(), colors):
        o.append(f'<rect x="196" y="{y - 10}" width="12" height="12" rx="3" fill="{col}"/>')
        o.append(f'<text x="214" y="{y}" font-size="12" fill="{t["fg"]}">{esc(name)}</text>')
        o.append(f'<text x="214" y="{y + 15}" font-size="11" font-family="{MONO}" fill="{t["muted"]}">{fmt(n)} · {100 * n / total:.0f}%</text>')
        y += 42
    o.append("</svg>")
    return "\n".join(o)


def svg_banner(total, ncat, nsec, updated):
    W, H = 1200, 320
    rnd = random.Random(1337)
    glyphs = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ$#%&*<>/\\{}[]"
    cols = []
    for i in range(28):
        x = 12 + i * 43
        chars = "".join(rnd.choice(glyphs) for _ in range(22))
        dur = rnd.uniform(5, 11)
        delay = -rnd.uniform(0, 11)
        tsp = "".join(f'<tspan x="{x}" dy="16">{esc(ch)}</tspan>' for ch in chars)
        cols.append(f'<text class="rain" style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s" x="{x}" y="0">{tsp}</text>')
    words = ["prompt injection", "agent security", "model context protocol", "red teaming", "supply chain", "governance",
             "incidents", "sandboxing", "secrets", "papers", f"{fmt(total)} links and counting"]
    cyc = 2.4 * len(words)
    typed = []
    for i, w in enumerate(words):
        typed.append(f'<text class="word" style="animation-delay:{i * 2.4:.1f}s;animation-duration:{cyc:.1f}s" x="600" y="212" text-anchor="middle">{esc(w)}<tspan class="cursor" fill="#2ee38a">▍</tspan></text>')
    pct = 100 / len(words)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}">
<style>
  .rain {{ font-size: 13px; fill: #2ee38a; opacity: 0.28; animation: fall linear infinite; }}
  @keyframes fall {{ from {{ transform: translateY(-360px); }} to {{ transform: translateY(340px); }} }}
  .title {{ font-size: 88px; font-weight: 800; letter-spacing: 6px; }}
  .ghost {{ animation: glitch 4s steps(2) infinite; }}
  @keyframes glitch {{ 0%,88%,100% {{ transform: translate(0,0); opacity: 0; }} 90% {{ transform: translate(-4px,2px); opacity: .8; }} 94% {{ transform: translate(4px,-2px); opacity: .8; }} 97% {{ transform: translate(-2px,0); opacity: .6; }} }}
  .word {{ font-size: 26px; fill: #e6edf3; opacity: 0; animation: show linear infinite; }}
  @keyframes show {{ 0% {{ opacity: 0; }} 1% {{ opacity: 1; }} {pct - 1:.2f}% {{ opacity: 1; }} {pct:.2f}% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
  .cursor {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .scan {{ animation: scan 7s linear infinite; }}
  @keyframes scan {{ from {{ transform: translateY(-40px); }} to {{ transform: translateY({H}px); }} }}
  .stat {{ font-size: 15px; letter-spacing: 3px; fill: #8b949e; }}
  .num {{ fill: #2ee38a; font-weight: 700; }}
</style>
<defs>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#2ee38a" stroke-opacity="0.07"/></pattern>
  <pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" fill-opacity="0.18"/></pattern>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070b" stop-opacity="0"/><stop offset="1" stop-color="#05070b" stop-opacity="1"/></linearGradient>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="#05070b"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  {"".join(cols)}
  <rect width="{W}" height="{H}" fill="url(#fade)" opacity="0.85"/>
  <text class="title ghost" x="600" y="150" text-anchor="middle" fill="#ff3b6b">AI SECURITY</text>
  <text class="title ghost" style="animation-delay:.15s" x="600" y="150" text-anchor="middle" fill="#00d4ff">AI SECURITY</text>
  <text class="title" x="600" y="150" text-anchor="middle" fill="#f4fff8" filter="url(#glow)">AI SECURITY</text>
  <text x="600" y="180" text-anchor="middle" font-size="14" letter-spacing="8" fill="#2ee38a">THE COMPENDIUM</text>
  {"".join(typed)}
  <text class="stat" x="600" y="272" text-anchor="middle"><tspan class="num">{fmt(total)}</tspan> LINKS   ·   <tspan class="num">{ncat}</tspan> CATEGORIES   ·   <tspan class="num">{nsec}</tspan> SECTIONS   ·   UPDATED <tspan class="num">{updated}</tspan></text>
  <text x="24" y="30" font-size="14" fill="#2ee38a" opacity="0.7">┌──</text><text x="{W - 24}" y="30" text-anchor="end" font-size="14" fill="#2ee38a" opacity="0.7">──┐</text>
  <text x="24" y="{H - 14}" font-size="14" fill="#2ee38a" opacity="0.7">└──</text><text x="{W - 24}" y="{H - 14}" text-anchor="end" font-size="14" fill="#2ee38a" opacity="0.7">──┘</text>
  <rect width="{W}" height="{H}" fill="url(#lines)"/>
  <rect class="scan" width="{W}" height="40" fill="#2ee38a" opacity="0.05"/>
</g>
</svg>'''


# ---------------------------------------------------------------- readme
def badge(label, value, color):
    q = lambda s: s.replace("-", "--").replace("_", "__").replace(" ", "%20").replace(",", "%2C")
    return f'<img alt="{esc(label)}: {esc(value)}" src="https://img.shields.io/badge/{q(label)}-{q(value)}-{color.lstrip("#")}?style=for-the-badge&labelColor=0b0e14">'


def picture(name, alt, width=None):
    w = f' width="{width}"' if width else ""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">'
            f'<img alt="{esc(alt)}" src="assets/{name}-light.svg"{w}></picture>')


def render_stats(cats, total, buckets, rows, recents, updated):
    nsec = sum(len(c["sections"]) for c in cats)
    biggest = sorted(((s[1], s[0], c["name"]) for c in cats for s in c["sections"]), reverse=True)[:5]
    o = []
    o.append('<p align="center">')
    o.append("  " + badge("links", fmt(total), "#2ee38a"))
    o.append("  " + badge("categories", str(len(cats)), "#00d4ff"))
    o.append("  " + badge("sections", str(nsec), "#c77dff"))
    o.append("  " + badge("papers", fmt(buckets["arXiv"]), "#ff3b6b"))
    o.append("  " + badge("repos", fmt(buckets["GitHub"]), "#ffb020"))
    o.append("  " + badge("updated", updated, "#9aa4b2"))
    o.append("</p>\n")
    o.append('<table align="center"><tr>')
    for n, lab in ((fmt(total), "links"), (str(len(cats)), "categories"), (str(nsec), "sections"),
                   (fmt(buckets["arXiv"]), "arXiv papers"), (fmt(buckets["GitHub"]), "GitHub repos"), (fmt(buckets["X / Twitter"]), "posts on X")):
        o.append(f'<td align="center"><h1>{n}</h1><sub>{lab}</sub></td>')
    o.append("</tr></table>\n")
    o.append('<p align="center">' + picture("categories", "Links per category") + "</p>\n")
    o.append('<table align="center"><tr>')
    o.append('<td>' + picture("growth", "Growth of the corpus over time") + "</td>")
    o.append('<td>' + picture("sources", "Share of links by source") + "</td>")
    o.append("</tr></table>\n")
    o.append("<details><summary><b>Largest sections</b></summary>\n")
    o.append("| Section | Category | Links |\n|---|---|---:|")
    for n, s, c in biggest:
        o.append(f"| {s} | {c} | {fmt(n)} |")
    o.append("\n</details>\n")
    o.append("<details><summary><b>Recently added</b></summary>\n")
    for d, title, url in recents:
        o.append(f"- `{d}` [{title}]({url})")
    o.append("\n</details>\n")
    o.append("```mermaid\nmindmap\n  root((AI Security · " + fmt(total) + " links))")
    for g in GROUPS:
        gc = [c for c in cats if c["group"] == g]
        if not gc:
            continue
        o.append(f"    {g} · {fmt(sum(c['links'] for c in gc))}")
        for c in gc:
            o.append(f"      {c['name'].replace('(', '- ').replace(')', '')} · {fmt(c['links'])}")
    o.append("```")
    return "\n".join(o)


def render_toc(cats):
    o = []
    for g, (color, emoji) in GROUPS.items():
        gc = [c for c in cats if c["group"] == g]
        if not gc:
            continue
        o.append(f"### {emoji} {g}\n\n<sub>{fmt(sum(c['links'] for c in gc))} links across {len(gc)} categor{'y' if len(gc) == 1 else 'ies'}</sub>\n")
        o.append("| Category | Links | Sections | What's inside |\n|---|---:|---:|---|")
        for c in gc:
            o.append(f"| [{c['name']}]({c['path']}) | {fmt(c['links'])} | {len(c['sections'])} | {c['desc']} |")
        o.append("")
    return "\n".join(o)


def replace_block(text, tag, body):
    start, end = f"<!-- {tag}:START -->", f"<!-- {tag}:END -->"
    if start not in text or end not in text:
        sys.exit(f"README is missing the {tag} markers")
    a, b = text.index(start) + len(start), text.index(end)
    return text[:a] + "\n" + body.strip("\n") + "\n" + text[b:]


def main():
    text = README.read_text()
    groups = parse_toc(text)
    cats, all_urls, domains = scan(groups)
    total = len(all_urls)
    buckets = sources(domains)
    rows = growth()
    updated = dt.date.today().isoformat()
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "banner.svg").write_text(svg_banner(total, len(cats), sum(len(c["sections"]) for c in cats), updated))
    for dark in (True, False):
        suf = "dark" if dark else "light"
        (ASSETS / f"categories-{suf}.svg").write_text(svg_categories(cats, dark))
        (ASSETS / f"growth-{suf}.svg").write_text(svg_growth(rows, dark))
        (ASSETS / f"sources-{suf}.svg").write_text(svg_sources(buckets, dark))
    text = replace_block(text, "STATS", render_stats(cats, total, buckets, rows, recent(), updated))
    text = replace_block(text, "TOC", render_toc(cats))
    README.write_text(text)
    print(f"{fmt(total)} links · {len(cats)} categories · {sum(len(c['sections']) for c in cats)} sections · "
          f"{fmt(buckets['GitHub'])} repos · {fmt(buckets['arXiv'])} papers · README + assets regenerated")


if __name__ == "__main__":
    main()

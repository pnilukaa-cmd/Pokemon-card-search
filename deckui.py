"""Render a deck report as a standalone HTML page (B4).

Reads the JSON deckreport.py emits and writes one self-contained file.
The page derives nothing of its own -- every figure on it came out of the
Python side -- so the interface and the engine can never disagree.

    python3 deckreport.py mydeck.txt decks/ --out=r.json
    python3 deckui.py r.json --out=deck.html
"""

import html
import json
import sys

SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
          "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
SERIES_DARK = ["#3987e5", "#d95926", "#199e70", "#c98500",
               "#d55181", "#008300", "#9085e9", "#e66767"]

CSS = """
:root{
  --ground:#f2f5f7; --surface:#ffffff; --surface-2:#e9eef1;
  --ink:#121a20; --muted:#5a6b78; --line:#d6dee4; --line-strong:#b9c6cf;
  --accent:#0d6b7b; --good:#0ca30c; --critical:#d03b3b; --mid:#f0efec;
  --f-display:"Archivo","Helvetica Neue",Arial,sans-serif;
  --f-body:"Source Serif 4",Georgia,serif;
  --f-mono:"JetBrains Mono",ui-monospace,Menlo,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --ground:#0d1418; --surface:#141d23; --surface-2:#1b262d;
  --ink:#e4ecf1; --muted:#94a6b3; --line:#25323a; --line-strong:#3a4b56;
  --accent:#43b3c2; --good:#0ca30c; --critical:#d03b3b; --mid:#383835;
}}
:root[data-theme="dark"]{
  --ground:#0d1418; --surface:#141d23; --surface-2:#1b262d;
  --ink:#e4ecf1; --muted:#94a6b3; --line:#25323a; --line-strong:#3a4b56;
  --accent:#43b3c2; --good:#0ca30c; --critical:#d03b3b; --mid:#383835;
}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font-family:var(--f-body);
  font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:70rem;margin:0 auto;padding:2.5rem 1.5rem 4rem}
h1{font-family:var(--f-display);font-weight:700;font-size:2rem;margin:0;
  letter-spacing:-.02em}
.sub{font-family:var(--f-mono);font-size:.72rem;letter-spacing:.09em;
  text-transform:uppercase;color:var(--accent);margin:0 0 .6rem}
h2{font-family:var(--f-display);font-weight:600;font-size:1.15rem;
  margin:2.5rem 0 .9rem;letter-spacing:-.01em}
.tiles{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);
  border-radius:4px;overflow:hidden;
  grid-template-columns:repeat(auto-fit,minmax(11rem,1fr));margin-top:1.5rem}
.tile{background:var(--surface);padding:1.1rem 1.2rem}
.tile .k{font-family:var(--f-mono);font-size:.65rem;letter-spacing:.1em;
  text-transform:uppercase;color:var(--muted);display:block;margin-bottom:.45rem}
.tile .v{font-family:var(--f-display);font-weight:700;font-size:1.7rem;
  line-height:1;font-variant-numeric:tabular-nums;display:block}
.pill{display:inline-flex;align-items:center;gap:.4rem;font-family:var(--f-mono);
  font-size:.7rem;font-weight:600;padding:.25rem .6rem;border-radius:2px}
.pill.ok{background:color-mix(in srgb,var(--good) 16%,transparent);color:var(--good)}
.pill.bad{background:color-mix(in srgb,var(--critical) 16%,transparent);color:var(--critical)}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:4px;
  padding:1.4rem 1.5rem}
.note{font-size:.9rem;color:var(--muted);margin:.35rem 0 0}
ul.issues{margin:.6rem 0 0;padding-left:1.1rem;font-size:.92rem}
ul.issues li{margin-bottom:.3rem}
.legend{display:flex;flex-wrap:wrap;gap:.35rem 1.1rem;margin:0 0 .9rem;
  font-size:.85rem}
.legend span{display:inline-flex;align-items:center;gap:.4rem}
.swatch{width:.8rem;height:.8rem;border-radius:2px;flex:none}
.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.88rem;
  font-variant-numeric:tabular-nums}
th,td{padding:.5rem .7rem;text-align:right;border-bottom:1px solid var(--line);
  white-space:nowrap}
th:first-child,td:first-child{text-align:left}
th{font-family:var(--f-mono);font-size:.65rem;letter-spacing:.07em;
  text-transform:uppercase;color:var(--muted)}
tr:last-child td{border-bottom:0}
.bar-row{display:grid;grid-template-columns:minmax(8rem,14rem) 1fr;
  gap:.9rem;align-items:center;margin-bottom:.5rem;font-size:.88rem}
.track{position:relative;height:1.5rem;background:var(--surface-2);border-radius:2px}
.fill{position:absolute;top:0;bottom:0;border-radius:2px}
.mid-line{position:absolute;top:-.2rem;bottom:-.2rem;left:50%;width:1px;
  background:var(--line-strong)}
.bar-val{position:absolute;top:0;bottom:0;display:flex;align-items:center;
  font-family:var(--f-mono);font-size:.74rem;font-weight:600;color:var(--ink)}
foreignObject{overflow:visible}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media (max-width:620px){.bar-row{grid-template-columns:1fr;gap:.2rem}}
"""


def esc(s):
    return html.escape(str(s))


def curve_svg(curve, turns=6):
    """Multi-series line chart: setup rate by turn.

    Direct end-labels on every series plus a legend and the table below --
    three of the eight categorical slots sit under 3:1 on the light
    surface, and the palette's relief rule requires visible labels or a
    table view when they do.
    """
    items = sorted(curve.items(), key=lambda kv: -kv[1][-1])[:8]
    if not items:
        return ""
    W, H = 660, 260
    L, R, T, B = 44, 168, 16, 34
    px = lambda t: L + (W - L - R) * (t - 1) / max(turns - 1, 1)
    py = lambda v: T + (H - T - B) * (1 - v / 100.0)

    parts = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
             f'aria-label="Setup rate by turn">']
    for v in (0, 25, 50, 75, 100):
        y = py(v)
        parts.append(f'<line x1="{L}" y1="{y:.1f}" x2="{W-R}" y2="{y:.1f}" '
                     f'stroke="var(--line)" stroke-width="1"/>')
        parts.append(f'<text x="{L-8}" y="{y+4:.1f}" text-anchor="end" '
                     f'font-size="10" fill="var(--muted)" '
                     f'font-family="var(--f-mono)">{v}%</text>')
    for t in range(1, turns + 1):
        parts.append(f'<text x="{px(t):.1f}" y="{H-12}" text-anchor="middle" '
                     f'font-size="10" fill="var(--muted)" '
                     f'font-family="var(--f-mono)">T{t}</text>')
    for i, (name, vals) in enumerate(items):
        c = SERIES[i % len(SERIES)]
        cd = SERIES_DARK[i % len(SERIES_DARK)]
        pts = " ".join(f"{px(t+1):.1f},{py(v):.1f}" for t, v in enumerate(vals[:turns]))
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{c}" '
                     f'stroke-width="2" stroke-linejoin="round" '
                     f'class="s{i}"/>')
        lastx, lasty = px(turns), py(vals[turns - 1])
        parts.append(f'<circle cx="{lastx:.1f}" cy="{lasty:.1f}" r="4" '
                     f'fill="{c}" stroke="var(--surface)" stroke-width="2" '
                     f'class="s{i}"/>')
        parts.append(f'<text x="{lastx+10:.1f}" y="{lasty+4:.1f}" font-size="11" '
                     f'fill="var(--ink)" font-family="var(--f-body)">'
                     f'{esc(name)} <tspan font-family="var(--f-mono)" '
                     f'font-size="10" fill="var(--muted)">'
                     f'{vals[turns-1]:.0f}%</tspan></text>')
    parts.append("<style>")
    for i in range(len(items)):
        parts.append(f'@media (prefers-color-scheme:dark){{'
                     f':root:not([data-theme="light"]) .s{i}'
                     f'{{stroke:{SERIES_DARK[i % 8]};fill:{SERIES_DARK[i % 8]}}}}}')
        parts.append(f':root[data-theme="dark"] .s{i}'
                     f'{{stroke:{SERIES_DARK[i % 8]};fill:{SERIES_DARK[i % 8]}}}')
    parts.append("circle{stroke:var(--surface)}</style>")
    parts.append("</svg>")

    legend = ['<div class="legend">']
    for i, (name, _) in enumerate(items):
        legend.append(f'<span><i class="swatch" style="background:'
                      f'{SERIES[i % 8]}"></i>{esc(name)}</span>')
    legend.append("</div>")
    return "".join(legend) + "".join(parts)


def field_bars(rows):
    """Win rate against each opponent, diverging around the 50% line.

    Above and below 50 are opposite outcomes, not more and less of one
    thing, so this is a polarity encoding with a neutral midpoint -- not a
    single-hue magnitude ramp.
    """
    out = []
    for r in rows:
        pct = r["win_pct"]
        good = pct >= 50
        col = "var(--good)" if good else "var(--critical)"
        if good:
            left, width = 50, pct - 50
        else:
            left, width = pct, 50 - pct
        label_left = f"calc({min(left + width, 96)}% + .5rem)" if good \
            else f"calc({max(left - 8, 1)}%)"
        out.append(
            f'<div class="bar-row"><span>{esc(r["opponent"])}</span>'
            f'<span class="track"><i class="mid-line"></i>'
            f'<i class="fill" style="left:{left}%;width:{width}%;'
            f'background:{col}"></i>'
            f'<span class="bar-val" style="left:{label_left}">{pct:.1f}%</span>'
            f'</span></div>')
    return "".join(out)


def render(d):
    ok = d.get("legal")
    tiles = [
        ("Cards", d["size"], ""),
        ("Basic Pokémon", d["basics"], ""),
        ("Mulligan", f'{d["mulligan_pct"]}%', ""),
    ]
    if "field_mean" in d:
        tiles.append(("Field mean", f'{d["field_mean"]}%', ""))
        tiles.append(("Winning matchups",
                      f'{d["field_wins"]}/{len(d["field"])}', ""))

    issues = ""
    if d["errors"] or d["warnings"] or d["unresolved"]:
        rows = ([f'<li><b>Error:</b> {esc(e)}</li>' for e in d["errors"]]
                + [f'<li>{esc(w)}</li>' for w in d["warnings"][:10]]
                + [f'<li>{esc(u)} did not resolve in this card pool</li>'
                   for u in d["unresolved"]])
        more = len(d["warnings"]) - 10
        if more > 0:
            rows.append(f'<li class="note">and {more} more warnings</li>')
        issues = f'<ul class="issues">{"".join(rows)}</ul>'

    curve_table = ['<div class="scroll"><table><thead><tr><th>Pokémon</th>'
                   + "".join(f"<th>T{t}</th>" for t in range(1, 7))
                   + "</tr></thead><tbody>"]
    for name, vals in sorted(d["curve"].items(), key=lambda kv: -kv[1][-1]):
        curve_table.append(f"<tr><td>{esc(name)}</td>"
                           + "".join(f"<td>{v:.0f}%</td>" for v in vals[:6])
                           + "</tr>")
    curve_table.append("</tbody></table></div>")

    lines = "".join(
        f'<tr><td>{l["count"]}× {esc(l["name"])}</td>'
        f'<td>{esc((l["set"] or "") + " " + (l["number"] or ""))}</td></tr>'
        for l in d["lines"])

    field_html = ""
    if d.get("field"):
        field_html = (f'<h2>Against the field</h2><div class="panel">'
                      f'<p class="note">Win rate per opponent, diverging from '
                      f'the 50% line. Green is a winning matchup.</p>'
                      f'<div style="margin-top:1rem">{field_bars(d["field"])}</div>'
                      f'</div>')

    return f"""<title>{esc(d['name'])} — Deck Report</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <p class="sub">Deck report · engine {esc(d['engine'])}</p>
  <h1>{esc(d['name'])}</h1>
  <p style="margin-top:.7rem">
    <span class="pill {'ok' if ok else 'bad'}">{'LEGAL' if ok else 'ILLEGAL'}</span>
  </p>
  <div class="tiles">
    {''.join(f'<div class="tile"><span class="k">{esc(k)}</span><span class="v">{esc(v)}</span></div>' for k, v, _ in tiles)}
  </div>

  <h2>Checks</h2>
  <div class="panel">
    {issues or '<p class="note">No errors, warnings or unresolved cards.</p>'}
  </div>

  <h2>Setup curve</h2>
  <div class="panel">
    <p class="note">Share of games with each Pokémon in play by the end of
    turn N, over 800 openings with the six Prize cards set aside.</p>
    <div style="margin-top:1rem">{curve_svg(d['curve'])}</div>
    <div style="margin-top:1.2rem">{''.join(curve_table)}</div>
  </div>

  {field_html}

  <h2>Decklist</h2>
  <div class="panel scroll">
    <table><tbody>{lines}</tbody></table>
  </div>
</div>
"""


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    d = json.load(open(args[0]))
    page = render(d)
    out = next((a for a in sys.argv if a.startswith("--out=")), None)
    path = out.split("=", 1)[1] if out else "deck_report.html"
    open(path, "w").write(page)
    print(f"wrote {path}")

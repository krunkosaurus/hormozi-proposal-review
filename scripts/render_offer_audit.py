#!/usr/bin/env python3
import json
import html
import sys
from pathlib import Path


def esc(value):
    if value is None:
        value = ""
    return html.escape(str(value), quote=True)


def quote_copy(value):
    text = str(value or "").strip()
    if not text:
        return ""
    if text[0] in {'"', "“", "‘", "'"}:
        return esc(text)
    return f"“{esc(text)}”"


def slugify(text):
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in str(text or ""))
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "status"


def numeric_score(value):
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value or "").strip()
    if not text:
        return None
    if "/" in text:
        text = text.split("/", 1)[0]
    text = text.replace("%", "").strip()
    try:
        return float(text)
    except ValueError:
        return None


def row_score_max(row, default_max=2):
    for key in ("score_max", "score_total", "max_score", "total"):
        value = row.get(key)
        if value not in (None, ""):
            parsed = numeric_score(value)
            if parsed and parsed > 0:
                return parsed
    score_text = str(row.get("score", "")).strip()
    if "/" in score_text:
        parsed = numeric_score(score_text.split("/", 1)[1])
        if parsed and parsed > 0:
            return parsed
    parsed_default = numeric_score(default_max)
    return parsed_default if parsed_default and parsed_default > 0 else 2.0


def format_score_number(value):
    if value is None:
        return "?"
    if float(value).is_integer():
        return str(int(value))
    return f"{value:g}"


def render_list(items, cls=""):
    if not items:
        return ""
    class_attr = f' class="{esc(cls)}"' if cls else ""
    return f'<ul{class_attr}>' + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def render_dossier_cell(item):
    label = item.get("label", "")
    if item.get("bullets"):
        value = render_list(item.get("bullets"), "plain-list")
    else:
        value = f'<p>{esc(item.get("value", ""))}</p>'
    return f"""<article class="dossier-cell">
      <p class="mono-label">{esc(label)}</p>
      <div class="dossier-copy">{value}</div>
    </article>"""


def render_unclear_block(item):
    if not item or not item.get("bullets"):
        return ""
    bullets = "".join(f"<li>— {esc(bullet)}</li>" for bullet in item.get("bullets", []))
    return f"""<aside class="unclear-callout">
      <p class="mono-label orange">{esc(item.get("label", "WHAT IS UNCLEAR"))}</p>
      <ul>{bullets}</ul>
    </aside>"""


def score_class(score, max_score=None):
    numeric = numeric_score(score)
    if numeric is None:
        return "score-unknown"
    max_numeric = numeric_score(max_score)
    if max_numeric and max_numeric > 0 and numeric >= max_numeric:
        return "score-high"
    if numeric <= 0:
        return "score-zero"
    if numeric <= 1:
        return "score-low"
    return "score-mid"


def render_score_row(row, index, default_max=2):
    status = row.get("status", "")
    zebra = "row-warm" if index % 2 else "row-cream"
    score = row.get("score", "")
    numeric = numeric_score(score)
    max_score = row_score_max(row, default_max)
    percent = 0 if numeric is None else max(0, min(100, (numeric / max_score) * 100))
    score_label = f"{format_score_number(numeric)} / {format_score_number(max_score)}"
    return f"""<div class="score-row {zebra}">
      <span class="score-area">{esc(row.get("area", ""))}</span>
      <div class="score-center">
        <span class="score-badge {score_class(score, max_score)}">{esc(score)}</span>
        <div class="score-mini-track" role="img" aria-label="Section score {esc(score_label)}"><div class="score-mini-fill" style="width:{percent:.4g}%;"></div></div>
        <span class="score-mini-label">{esc(score_label)}</span>
        <span class="score-status status-{esc(slugify(status))}">{esc(status)}</span>
      </div>
      <span class="score-notes">{esc(row.get("notes", ""))}</span>
    </div>"""


def render_leak(index, leak):
    return f"""<article class="leak-card">
      <div class="leak-number"><span>LEAK</span><strong>{index:02d}</strong></div>
      <h3>{esc(leak.get("title", ""))}</h3>
      <div class="leak-grid">
        <div><p class="mono-label">EVIDENCE</p><p>{esc(leak.get("evidence", ""))}</p></div>
        <div><p class="mono-label">WHY IT HURTS</p><p>{esc(leak.get("why_it_hurts", ""))}</p></div>
        <div><p class="mono-label">PRINCIPLE VIOLATED</p><p>{esc(leak.get("principle_violated", ""))}</p></div>
        <div><p class="mono-label">FIX</p>{render_list(leak.get("fixes", []), "plain-list")}</div>
      </div>
    </article>"""


def render_rewrite(item):
    blocks = []
    current_copy = item.get("before") or "Not clearly stated in current materials."
    current_label = "CURRENT" if item.get("before") else "CURRENT (IMPLIED)"
    blocks.append(f"""<div class="rewrite-column rewrite-current">
      <p class="mono-label">{current_label}</p>
      <p class="rewrite-copy quote-copy">{quote_copy(current_copy)}</p>
    </div>""")
    blocks.append(f"""<div class="rewrite-column rewrite-after">
      <p class="mono-label teal">BETTER</p>
      <p class="rewrite-copy quote-copy">{quote_copy(item.get("after", ""))}</p>
    </div>""")
    if item.get("strongest"):
        blocks.append(f"""<div class="rewrite-column rewrite-strongest">
      <p class="mono-label teal">STRONGEST</p>
      <p class="rewrite-copy quote-copy">{quote_copy(item.get("strongest", ""))}</p>
    </div>""")
    grid_class = "rewrite-grid rewrite-grid-three" if len(blocks) == 3 else "rewrite-grid"
    return f"""<article class="rewrite-card">
      <h3>{esc(item.get("title", ""))}</h3>
      <p class="muted-copy">{esc(item.get("diagnosis", ""))}</p>
      <div class="{grid_class}">{''.join(blocks)}</div>
    </article>"""


def render_pricing_option(item):
    return f"""<article class="pricing-card">
      <p class="mono-label">{esc(item.get("name", ""))}</p>
      {render_list(item.get("bullets", []), "plain-list")}
    </article>"""


def render_action_column(title, items, tone="neutral"):
    return f"""<article class="action-card action-{esc(tone)}">
      <p class="mono-label">{esc(title)}</p>
      {render_list(items, "plain-list action-list")}
    </article>"""


def build_html(data):
    meta = data.get("meta", {})
    verdict = data.get("verdict", {})
    scorecard = data.get("scorecard", {})
    pricing = data.get("pricing", {})
    action_plan = data.get("action_plan", {})

    total = scorecard.get("score_total", 0) or 0
    obtained = scorecard.get("score_obtained", 0) or 0
    percent = scorecard.get("percent")
    if percent in (None, ""):
        percent = round((obtained / total) * 100) if total else 0
    try:
        bar_width = max(0, min(100, float(percent)))
    except (TypeError, ValueError):
        bar_width = 0

    nav_items = [("verdict", "Verdict"), ("scorecard", "Scorecard"), ("leaks", "Leaks"), ("strengths", "Strengths"), ("rewrites", "Rewrites"), ("pricing", "Pricing"), ("action", "Action Plan")]
    nav_html = "\n        ".join(f'<a href="#{section_id}">{label}</a>' for section_id, label in nav_items)

    unclear_item = None
    dossier_items = []
    for item in data.get("dossier", []):
        if str(item.get("label", "")).strip().upper() == "WHAT IS UNCLEAR":
            unclear_item = item
        else:
            dossier_items.append(item)

    dossier_html = "\n".join(render_dossier_cell(item) for item in dossier_items)
    unclear_html = render_unclear_block(unclear_item)
    default_row_max = scorecard.get("max_score_per_row", scorecard.get("section_score_total", 2))
    score_rows_html = "\n".join(render_score_row(row, i, default_row_max) for i, row in enumerate(scorecard.get("rows", [])))
    leaks_html = "\n".join(render_leak(i + 1, leak) for i, leak in enumerate(data.get("leaks", [])))
    strengths_html = "".join(f"<li>{esc(item)}</li>" for item in data.get("strengths", []))
    rewrites_html = "\n".join(render_rewrite(item) for item in data.get("section_rewrites", []))
    pricing_html = "\n".join(render_pricing_option(item) for item in pricing.get("options", []))
    action_html = "\n".join([render_action_column("FIX THIS FIRST", action_plan.get("fix_this_first", []), "orange"), render_action_column("THEN TEST THIS", action_plan.get("then_test", []), "teal"), render_action_column("DO NOT CHANGE YET", action_plan.get("do_not_change_yet", []), "neutral")])
    funnel_steps = action_plan.get("funnel_flow", [])
    funnel_parts = []
    for i, step in enumerate(funnel_steps):
        funnel_parts.append(f'<span class="funnel-step">{esc(step)}</span>')
        if i < len(funnel_steps) - 1:
            funnel_parts.append('<span class="funnel-arrow">→</span>')
    funnel_html = "".join(funnel_parts)
    blunt = action_plan.get("blunt_recommendation") or {}
    blunt_headline = blunt.get("headline") or verdict.get("quote") or verdict.get("headline", "")
    blunt_body = blunt.get("body") or verdict.get("summary", "")

    title = esc(meta.get("title", "Offer Audit"))
    eyebrow = esc(meta.get("eyebrow", "ALEX HORMOZI METHOD"))
    subtitle = esc(meta.get("subtitle", ""))
    subject = esc(meta.get("subject", ""))
    generated_for = esc(meta.get("generated_for", "Internal Use Only"))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Offer Audit</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,400&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {{ --bg:#FDF6EC; --ink:#2B1D0E; --muted:#7A6A55; --hairline:#D4C5A9; --panel:#2B1D0E; --cream:#FDF6EC; --warm:#FAF2E4; --warm-2:#F5EDD8; --teal:#0D5C63; --teal-soft:#E8F4F5; --orange:#C4500A; --orange-soft:#FDF0E8; --page-width:1088px; }}
    * {{ box-sizing:border-box; }} html {{ scroll-behavior:smooth; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font-family:"Source Serif 4", Georgia, serif; font-size:21px; line-height:1.72; -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility; }}
    a {{ color:inherit; text-decoration:none; }} p {{ margin:0; }}
    .mono,.mono-label,.section-number,.nav,.annotation {{ font-family:"DM Mono",ui-monospace,monospace; }}
    .sticky-nav {{ position:sticky; top:0; z-index:50; background:var(--bg); backdrop-filter:blur(12px); border-bottom:2px solid var(--ink); }}
    .nav-inner {{ max-width:var(--page-width); margin:0 auto; padding:8px 32px; display:flex; align-items:center; gap:4px; overflow-x:auto; scrollbar-width:none; }} .nav-inner::-webkit-scrollbar {{ display:none; }}
    .brand {{ margin-right:12px; color:var(--muted); font-size:12px; letter-spacing:.16em; text-transform:uppercase; white-space:nowrap; flex:0 0 auto; }}
    .nav a {{ color:var(--muted); font-size:12px; padding:4px 12px; border-radius:2px; white-space:nowrap; transition:color .15s ease,background .15s ease; }} .nav a:hover {{ color:var(--teal); background:var(--teal-soft); }}
    .hero, main {{ max-width:var(--page-width); margin:0 auto; padding-left:32px; padding-right:32px; }} .hero {{ padding-top:56px; padding-bottom:40px; }}
    .annotation {{ display:inline-block; margin-bottom:24px; padding:5px 8px; background:var(--panel); color:var(--cream); font-size:12px; letter-spacing:.14em; text-transform:uppercase; line-height:1.2; }}
    h1,h2,h3 {{ margin:0; color:var(--ink); font-family:"Playfair Display",Georgia,serif; line-height:1.05; letter-spacing:-.025em; }} h1 {{ max-width:780px; margin-bottom:16px; font-size:clamp(50px,7.4vw,78px); font-weight:900; line-height:.98; letter-spacing:-.035em; }} h2 {{ margin-bottom:20px; font-size:clamp(32px,4.2vw,46px); font-weight:900; }} h3 {{ margin-bottom:14px; font-size:clamp(24px,3.1vw,33px); font-weight:900; }}
    .lede {{ max-width:640px; color:var(--muted); font-size:22px; line-height:1.72; font-weight:300; }} .hero-meta {{ margin-top:16px; color:var(--muted); font-size:18px; }}
    .rule-divider-thick {{ display:block; height:4px; margin:32px 0 0; border:0; background:var(--ink); }} .section {{ margin-bottom:64px; scroll-margin-top:64px; }}
    .section-number {{ display:block; margin-bottom:0; color:var(--muted); font-size:12px; letter-spacing:.16em; text-transform:uppercase; }} .rule-divider {{ display:block; height:2px; margin:40px 0; border:0; background:var(--hairline); }}
    .mono-label {{ margin-bottom:7px; color:var(--muted); font-size:12px; font-weight:500; letter-spacing:.105em; text-transform:uppercase; }} .orange {{ color:var(--orange); }} .teal {{ color:var(--teal); }}
    .muted-copy {{ max-width:720px; margin-bottom:18px; color:var(--muted); font-size:19px; line-height:1.65; }}
    .verdict-panel {{ margin-top:24px; margin-bottom:24px; padding:32px 40px; background:var(--panel); color:var(--cream); }} .verdict-panel .mono-label {{ color:var(--hairline); }} .verdict-panel h2 {{ max-width:760px; color:var(--cream); font-size:clamp(32px,5vw,44px); }}
    .verdict-summary {{ margin-bottom:18px; color:var(--ink); line-height:1.75; }} .pull-quote {{ margin:24px 0 0; padding-left:22px; border-left:4px solid var(--teal); color:var(--teal); font-family:"Playfair Display",Georgia,serif; font-size:23px; font-style:italic; font-weight:700; line-height:1.45; }}
    .dossier-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:0; margin-top:24px; border-top:1px solid var(--hairline); border-left:1px solid var(--hairline); }} .dossier-cell {{ min-height:100%; padding:22px; border-right:1px solid var(--hairline); border-bottom:1px solid var(--hairline); }} .dossier-copy,.dossier-copy p {{ color:var(--ink); font-size:19px; line-height:1.65; }}
    .unclear-callout {{ margin-top:24px; padding:20px; border-left:4px solid var(--orange); background:var(--orange-soft); }} .unclear-callout ul {{ margin:0; padding:0; list-style:none; color:var(--ink); font-size:19px; line-height:1.55; }} .unclear-callout li+li {{ margin-top:4px; }}
    .score-title {{ margin:0 0 20px; font-size:clamp(26px,3.5vw,34px); }} .score-kpi {{ display:flex; align-items:center; gap:16px; margin-bottom:12px; }} .score-track {{ flex:1; height:12px; overflow:hidden; border-radius:2px; background:#F0E8D8; }} .score-fill {{ height:100%; background:var(--orange); }} .score-percent {{ color:var(--orange); font-family:"DM Mono",ui-monospace,monospace; font-size:17px; font-weight:500; white-space:nowrap; }} .score-interpretation {{ margin-bottom:24px; color:var(--orange); font-family:"DM Mono",ui-monospace,monospace; font-size:12px; letter-spacing:.12em; text-transform:uppercase; line-height:1.5; }}
    .score-table {{ overflow:hidden; border:1px solid var(--hairline); }} .score-header,.score-row {{ display:grid; grid-template-columns:minmax(150px,1fr) minmax(104px,auto) minmax(240px,2fr); gap:16px; align-items:start; padding:14px 22px; }} .score-header {{ background:var(--panel); color:var(--cream); }} .score-header span {{ font-family:"DM Mono",ui-monospace,monospace; font-size:12px; letter-spacing:.14em; text-transform:uppercase; }} .score-header span:nth-child(2) {{ text-align:center; padding:0 14px; }}
    .score-row {{ border-bottom:1px solid var(--hairline); transition:background .15s ease; }} .score-row:last-child {{ border-bottom:0; }} .score-row:hover {{ background:var(--warm-2); }} .row-cream {{ background:var(--cream); }} .row-warm {{ background:var(--warm); }} .score-area {{ color:var(--ink); font-size:19px; font-weight:600; line-height:1.45; }} .score-center {{ display:flex; flex-direction:column; align-items:center; gap:5px; min-width:104px; padding:0 8px; }} .score-badge {{ display:inline-flex; width:30px; height:30px; align-items:center; justify-content:center; border-radius:2px; border:1px solid currentColor; background:var(--cream); font-family:"DM Mono",ui-monospace,monospace; font-size:14px; font-weight:500; }} .score-mini-track {{ width:88px; height:6px; overflow:hidden; border:1px solid var(--hairline); border-radius:999px; background:#F0E8D8; }} .score-mini-fill {{ height:100%; background:var(--orange); }} .score-mini-label {{ color:var(--orange); font-family:"DM Mono",ui-monospace,monospace; font-size:10px; font-weight:500; line-height:1; }} .score-zero {{ color:#8F2B18; background:#FDF0E8; }} .score-low {{ color:#B17816; background:#FFF7DD; }} .score-mid {{ color:var(--teal); background:var(--teal-soft); }} .score-high {{ color:var(--teal); background:var(--teal-soft); }} .score-status {{ color:var(--muted); font-family:"DM Mono",ui-monospace,monospace; font-size:11px; text-transform:none; }} .score-notes {{ color:var(--muted); font-size:19px; line-height:1.6; }}
    .section-intro {{ max-width:68ch; margin-bottom:28px; color:var(--muted); font-size:19px; line-height:1.65; }} .leak-card {{ margin:24px 0 0; padding:26px 30px 28px; border-left:4px solid var(--orange); background:var(--orange-soft); }} .leak-card:first-of-type {{ margin-top:24px; }} .leak-card > * {{ max-width:780px; }} .leak-number {{ display:flex; gap:6px; align-items:baseline; margin-bottom:7px; color:var(--orange); font-family:"DM Mono",ui-monospace,monospace; font-size:12px; font-weight:500; letter-spacing:.09em; text-transform:uppercase; }} .leak-number strong {{ font-size:14px; letter-spacing:.01em; }} .leak-card h3 {{ margin-bottom:13px; font-size:clamp(22px,2.4vw,27px); line-height:1.18; }} .leak-grid {{ display:grid; grid-template-columns:1fr; gap:12px; margin-top:16px; }} .leak-grid .mono-label {{ margin-bottom:4px; color:var(--orange); letter-spacing:.09em; }} .leak-grid p,.plain-list {{ color:#4F3A24; font-size:19px; line-height:1.56; }} .leak-grid div:nth-child(3) p:not(.mono-label) {{ color:var(--orange); font-weight:600; }} .plain-list {{ margin:0; padding-left:0; list-style:none; }} .plain-list li {{ position:relative; padding-left:18px; }} .plain-list li::before {{ content:"→"; position:absolute; left:0; color:var(--orange); }} .plain-list li+li {{ margin-top:3px; }}
    .strength-list {{ margin:8px 0 0; padding:0; list-style:none; }} .strength-list li {{ margin:0 0 8px; padding:12px 20px; border-left:4px solid var(--green,#4A7C59); background:#EEF5F0; color:var(--ink); font-size:19px; line-height:1.45; }}
    .rewrite-card {{ margin-bottom:40px; padding:0; border-top:0; }} .rewrite-card:first-of-type {{ border-top:0; }} .rewrite-card h3 {{ margin-bottom:12px; font-family:"Source Serif 4",Georgia,serif; font-size:23px; font-weight:700; letter-spacing:0; line-height:1.35; }} .rewrite-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; margin-top:18px; border:0; }} .rewrite-grid-three {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} .rewrite-grid.single {{ grid-template-columns:1fr; }} .rewrite-column {{ padding:18px; border:1px solid var(--hairline); background:var(--cream); }} .rewrite-column+.rewrite-column {{ border-left:1px solid var(--teal); }} .rewrite-column .mono-label {{ color:var(--orange); }} .rewrite-copy {{ color:var(--ink); font-family:"Source Serif 4",Georgia,serif; font-size:20px; font-weight:400; line-height:1.7; }} .quote-copy {{ font-style:italic; hanging-punctuation:first last; }} .rewrite-current .quote-copy {{ color:var(--muted); }} .rewrite-after,.rewrite-strongest {{ background:var(--teal-soft); border-color:var(--teal); }} .rewrite-after .mono-label,.rewrite-strongest .mono-label {{ color:var(--teal); }} .rewrite-strongest {{ border-width:2px; }} .rewrite-strongest .quote-copy {{ font-weight:600; font-style:normal; }}
    .pricing-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; margin-top:24px; border:0; }} .pricing-card {{ padding:22px; border:1px solid var(--hairline); background:transparent; }} .pricing-card .mono-label {{ color:var(--teal); }}
    .action-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:28px; margin:24px 0 40px; border:0; }} .action-card {{ padding:22px; border-left:4px solid var(--hairline); background:var(--warm-2); }} .action-card .mono-label {{ margin-bottom:12px; }} .action-card.action-orange {{ border-left-color:var(--orange); background:var(--orange-soft); }} .action-card.action-orange .mono-label {{ color:var(--orange); }} .action-card.action-teal {{ border-left-color:var(--teal); background:var(--teal-soft); }} .action-card.action-teal .mono-label {{ color:var(--teal); }} .action-card.action-neutral .mono-label {{ color:var(--muted); }} .action-card .plain-list {{ color:var(--ink); font-size:19px; }} .action-list {{ display:grid; gap:10px; }} .action-list li {{ display:grid; grid-template-columns:18px 1fr; column-gap:8px; align-items:start; padding-left:0; line-height:1.42; }} .action-list li::before {{ content:"→"; position:static; left:auto; color:var(--action-arrow,var(--orange)); font-family:"DM Mono",ui-monospace,monospace; font-size:17px; font-weight:500; line-height:1.55; }} .action-orange {{ --action-arrow:var(--orange); }} .action-teal {{ --action-arrow:var(--teal); }} .action-neutral {{ --action-arrow:var(--muted); }}
    .funnel-box {{ margin-top:24px; padding:0; border-top:0; }} .funnel-flow {{ display:flex; flex-wrap:wrap; align-items:center; gap:8px; max-width:84ch; }} .funnel-step {{ display:inline-block; padding:8px 16px; background:var(--teal); color:var(--cream); font-size:17px; font-weight:600; line-height:1.4; }} .funnel-arrow {{ color:var(--ink); font-size:19px; }}
    .blunt-recommendation {{ margin-top:32px; padding:40px; background:var(--panel); color:var(--cream); }} .blunt-recommendation .mono-label {{ margin-bottom:16px; color:var(--hairline); }} .blunt-recommendation h3 {{ margin:0 0 16px; color:var(--cream); font-family:"Playfair Display",Georgia,serif; font-size:clamp(24px,3vw,32px); font-weight:900; line-height:1.35; letter-spacing:-.015em; }} .blunt-recommendation p {{ color:var(--hairline); font-size:19px; line-height:1.65; }}
    .footer {{ border-top:2px solid var(--ink); padding:34px 0; background:var(--bg); }} .footer-inner {{ max-width:var(--page-width); margin:0 auto; padding:0 32px; display:flex; align-items:flex-start; justify-content:space-between; gap:28px; }} .footer-title,.score-label {{ color:var(--muted); font-family:"DM Mono",ui-monospace,monospace; font-size:12px; letter-spacing:.16em; text-transform:uppercase; }} .footer-subtitle {{ margin-top:4px; color:#A99378; font-family:"DM Mono",ui-monospace,monospace; font-size:12px; }} .score-value {{ margin-top:2px; color:var(--orange); font-family:"Playfair Display",Georgia,serif; font-size:34px; font-weight:900; line-height:1; text-align:right; }}
    @media (max-width:760px) {{ body {{ font-size:19px; }} .rewrite-grid-three {{ grid-template-columns:1fr; }} .nav-inner {{ padding:8px 16px; }} .hero,main {{ padding-left:20px; padding-right:20px; }} .hero {{ padding-top:42px; }} h1 {{ font-size:clamp(42px,12vw,56px); }} .section {{ margin-bottom:48px; }} .dossier-grid,.leak-grid,.rewrite-grid,.pricing-grid,.action-grid {{ grid-template-columns:1fr; }} .rewrite-column+.rewrite-column {{ border-left:0; border-top:1px solid var(--hairline); }} .score-header {{ display:none; }} .score-row {{ grid-template-columns:1fr; gap:8px; padding:16px; }} .score-center {{ align-items:flex-start; min-width:0; padding:0; }} .footer-inner {{ padding:0 20px; }} .score-value {{ text-align:left; }} }}
  </style>
</head>
<body>
  <nav class="sticky-nav nav" aria-label="Audit sections"><div class="nav-inner"><span class="brand">Offer Audit</span>{nav_html}</div></nav>
  <header class="hero"><div><span class="annotation">{eyebrow}</span></div><h1>{title}</h1><p class="lede">{subtitle}</p>{f'<p class="hero-meta">{subject} · {generated_for}</p>' if subject or generated_for else ''}<hr class="rule-divider-thick"></header>
  <main>
    <section id="verdict" class="section"><span class="section-number">01 — Executive Verdict</span><hr class="rule-divider"><div class="verdict-panel"><p class="mono-label">{esc(verdict.get("label", "VERDICT"))}</p><h2>{esc(verdict.get("headline", ""))}</h2></div><p class="verdict-summary">{esc(verdict.get("summary", ""))}</p>{f'<blockquote class="pull-quote">“{esc(verdict.get("quote", ""))}”</blockquote>' if verdict.get("quote") else ''}</section>
    <section id="dossier" class="section"><span class="section-number">02 — Proposal Dossier</span><hr class="rule-divider"><div class="dossier-grid">{dossier_html}</div>{unclear_html}</section>
    <section id="scorecard" class="section"><span class="section-number">03 — Scorecard</span><h2 class="score-title">Score: {esc(obtained)} / {esc(total)}</h2><hr class="rule-divider"><div class="score-kpi"><div class="score-track"><div class="score-fill" style="width:{bar_width:.4g}%;"></div></div><span class="score-percent">{esc(percent)}%</span></div><p class="score-interpretation">Interpretation: {esc(scorecard.get("interpretation", ""))}</p><div class="score-table"><div class="score-header"><span>Area</span><span>Score</span><span>Notes</span></div>{score_rows_html}</div></section>
    <section id="leaks" class="section"><span class="section-number">04 — Biggest Leaks</span><h2>Five Critical Revenue Leaks</h2><hr class="rule-divider"><p class="section-intro">These are structural problems in the offer — not cosmetic fixes. Address them before scaling any paid traffic.</p>{leaks_html}</section>
    <section id="strengths" class="section"><span class="section-number">05 — What Is Strong</span><h2>Keep These. Don’t Touch Them.</h2><hr class="rule-divider"><ul class="strength-list">{strengths_html}</ul></section>
    <section id="rewrites" class="section"><span class="section-number">06 — Section Critique &amp; Rewrites</span><h2>What to Say Instead</h2><hr class="rule-divider">{rewrites_html}</section>
    <section id="pricing" class="section"><span class="section-number">07 — Pricing</span><h2>{esc(pricing.get("title", "Pricing Recommendation"))}</h2><hr class="rule-divider"><p class="section-intro">{esc(pricing.get("intro", ""))}</p><div class="pricing-grid">{pricing_html}</div></section>
    <section id="action" class="section"><span class="section-number">08 — Action Plan</span><h2>What to Do First</h2><hr class="rule-divider"><div class="action-grid">{action_html}</div>{f'<div class="funnel-box"><h3>The Right Funnel Flow</h3><div class="funnel-flow">{funnel_html}</div></div>' if action_plan.get("funnel_flow") else ''}{f'<aside class="blunt-recommendation"><p class="mono-label">Blunt Recommendation</p><h3>{esc(blunt_headline)}</h3><p>{esc(blunt_body)}</p></aside>' if blunt_headline or blunt_body else ''}</section>
  </main>
  <footer class="footer"><div class="footer-inner"><div><div class="footer-title">Offer Audit</div><div class="footer-subtitle">{eyebrow} · {generated_for or "Internal Use Only"}</div></div><div><div class="score-label">Total Score</div><div class="score-value">{esc(obtained)} / {esc(total)}</div></div></div></footer>
</body>
</html>"""


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 render_offer_audit.py <input.json> <output.html>", file=sys.stderr)
        return 1
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_html(data), encoding="utf-8")
    print(f"Rendered {input_path} -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

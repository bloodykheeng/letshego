"""Write briefing.html from BRIEFING.md, so the team briefing has one source.

Handles the Markdown the briefing uses: headings, paragraphs, lists, tables, blockquotes, code blocks, links,
bold, italics and inline code. Heading ids follow GitHub's rules so the contents links work in both places.
"""
from __future__ import annotations

import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
  :root {
    --bg:#F5F6FA; --card:#FFFFFF; --ink:#1B1C3A; --ink2:#4B4D6B; --muted:#6E7190; --line:#E4E5EF;
    --brand:#2F2E80; --brand-bg:#ECECF8; --yellow:#FBD405; --yellow-ink:#7A5C00; --yellow-bg:#FFF7CC;
    --code-bg:#1F1E57; --code-ink:#E9E8FB;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg:#121226; --card:#1B1B36; --ink:#ECECF8; --ink2:#C6C6E0; --muted:#9A9BBC; --line:#2C2C4E;
      --brand:#A9A6FF; --brand-bg:#25244D; --yellow:#FBD405; --yellow-ink:#FBD405; --yellow-bg:#2E2A14;
      --code-bg:#0D0D1F; --code-ink:#E9E8FB;
    }
  }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font:16px/1.6 "Segoe UI", system-ui, sans-serif; }
  .top { background:#2F2E80; color:#fff; }
  .top .in { max-width:960px; margin:0 auto; padding:28px 16px 30px; }
  .brand { display:flex; align-items:center; gap:10px; font-weight:700; font-style:italic; font-size:24px; }
  .tag { display:inline-block; margin-top:14px; font-size:12px; font-weight:700; letter-spacing:.08em;
         text-transform:uppercase; color:#1F1E57; background:#FBD405; border-radius:999px; padding:2px 10px; }
  .wrap { max-width:960px; margin:0 auto; padding:8px 16px 80px; }
  h1 { font-size:32px; line-height:1.2; margin:10px 0 0; color:#fff; }
  h2 { font-size:22px; margin:44px 0 12px; padding-top:10px; border-top:1px solid var(--line); }
  h3 { font-size:17px; margin:22px 0 6px; }
  p { margin:8px 0; color:var(--ink2); }
  a { color:var(--brand); font-weight:600; }
  strong { color:var(--ink); }
  ul, ol { color:var(--ink2); padding-left:22px; }
  li { margin:4px 0; }
  hr { display:none; }
  blockquote { margin:14px 0; background:var(--brand-bg); border-radius:12px; padding:12px 18px; }
  blockquote p { color:var(--ink); }
  .toc a { display:inline-block; font-size:13.5px; background:var(--card); border:1px solid var(--line);
           border-radius:999px; padding:3px 12px; margin:3px 2px; text-decoration:none; color:var(--ink);
           font-weight:500; }
  .table { overflow-x:auto; margin:12px 0; border:1px solid var(--line); border-radius:12px; background:var(--card); }
  table { width:100%; border-collapse:collapse; font-size:14.5px; }
  th, td { text-align:left; vertical-align:top; padding:9px 12px; border-bottom:1px solid var(--line); }
  th { font-size:12px; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); background:var(--bg); }
  tr:last-child td { border-bottom:0; }
  td { color:var(--ink2); }
  pre { background:var(--code-bg); color:var(--code-ink); border-radius:12px; padding:14px 16px; overflow-x:auto;
        font:12.5px/1.5 Consolas, "Cascadia Mono", monospace; }
  code { font-family:Consolas, "Cascadia Mono", monospace; font-size:.92em; background:var(--brand-bg);
         padding:1px 5px; border-radius:5px; }
  pre code { background:none; padding:0; }
  @media (max-width:640px) { h1 { font-size:26px; } body { font-size:15.5px; } }
"""

MARK = ('<svg width="30" height="28" viewBox="0 0 36 36" aria-hidden="true"><path d="M19 2 L1 33 L21 23 Z" '
        'fill="#FBD405"/><path d="M19 2 L21 23 L35 33 Z" fill="#E9B800"/><path d="M1 33 L21 23 L35 33 Z" '
        'fill="#FFE457"/></svg>')


def slug(text):
    t = re.sub(r"<[^>]+>", "", text).lower()
    t = re.sub(r"[^\w\- ]", "", t)
    return t.replace(" ", "-")


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r'(?<!["=>])(https://[^\s<]+[^\s<.,)])', r'<a href="\1">\1</a>', t)
    return t


def convert(md):
    lines = md.split("\n")
    out, i, title = [], 0, ""
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            j = i + 1
            while not lines[j].startswith("```"):
                j += 1
            out.append("<pre><code>" + html.escape("\n".join(lines[i + 1:j])) + "</code></pre>")
            i = j + 1
        elif ln.startswith("# "):
            title = ln[2:].strip()
            i += 1
        elif re.match(r"#{2,3} ", ln):
            level = len(ln.split(" ")[0])
            text = ln[level + 1:].strip()
            out.append(f'<h{level} id="{slug(text)}">{inline(text)}</h{level}>')
            i += 1
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], rows[2:]
            t = "<div class=\"table\"><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + \
                "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
            out.append(t + "</tbody></table></div>")
        elif ln.startswith(">"):
            block = []
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i][1:].strip())
                i += 1
            paras = [p for p in "\n".join(block).split("\n\n") if p.strip()]
            out.append("<blockquote>" + "".join(f"<p>{inline(' '.join(p.split()))}</p>" for p in paras) +
                       "</blockquote>")
        elif re.match(r"(- |\d+\. )", ln):
            ordered = bool(re.match(r"\d+\. ", ln))
            items = []
            while i < len(lines) and re.match(r"(- |\d+\. )", lines[i]):
                items.append(re.sub(r"^(- |\d+\. )", "", lines[i]))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
        elif ln.strip() == "---":
            i += 1
        elif not ln.strip():
            i += 1
        else:
            para = [ln]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"(#|\||>|- |\d+\. |```|---)", lines[i]):
                para.append(lines[i])
                i += 1
            text = " ".join(para)
            cls = ' class="toc"' if text.startswith("**Contents:**") else ""
            if cls:
                text = text.replace(" · ", " ")
            out.append(f"<p{cls}>{inline(text)}</p>")
    return title, "\n".join(out)


def main():
    md = open(os.path.join(ROOT, "BRIEFING.md"), encoding="utf-8").read()
    title, body = convert(md)
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Letshego Team Briefing</title>
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#2F2E80">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="description" content="Internal team briefing: the Letshego Field Sales brief in plain language, the client journey, and how the prototype answers each request.">
<meta property="og:title" content="Letshego Field Sales: team briefing">
<meta property="og:description" content="Internal notes: the brief in plain language, questions for the client, and the demo walkthrough.">
<meta property="og:image" content="https://letshego.vercel.app/og-image.jpg">
<style>{CSS}</style>
</head>
<body>
<div class="top"><div class="in">
<div class="brand">{MARK}Letshego</div>
<h1>{html.escape(title.replace("Letshego ", ""))}</h1>
<span class="tag">Internal · team only</span>
</div></div>
<div class="wrap">
{body}
</div>
</body>
</html>
"""
    open(os.path.join(ROOT, "briefing.html"), "w", encoding="utf-8").write(page)
    print("briefing.html", len(page) // 1024, "KB")


if __name__ == "__main__":
    main()

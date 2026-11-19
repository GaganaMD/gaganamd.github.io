"""Assemble the site's HTML pages from the fragments in pages/ and the page list in content.py.

Run from anywhere:  python _build/build.py
Output is written to the repository root (the folder above _build/).
Jekyll on GitHub Pages does not publish folders starting with "_", so this
source is versioned with the site but never served. See _build/README.md."""
import hashlib, json, pathlib, re, sys

sys.dont_write_bytecode = True  # keep _build/ free of __pycache__

SRC = pathlib.Path(__file__).parent / "pages"
OUT = pathlib.Path(__file__).resolve().parent.parent  # repository root
SITE = "https://gaganamd.github.io"
EMAIL = "gaganaaa.dev@gmail.com"


def v(name):
    """Asset URL with a short content hash, so browsers and the CDN never pair new HTML with an old file."""
    data = (OUT / name).read_bytes()
    return f"{name}?v={hashlib.sha256(data).hexdigest()[:10]}"

NAV = [
    ("research.html", "Research"),
    ("writing.html", "Writing"),
    ("about.html", "About"),
    None,
    ("speaking.html", "Speaking"),
    ("consulting.html", "Consulting"),
]

# Runs before first paint so a saved theme choice never flashes the other theme.
THEME_JS = ('<script>(function(){document.documentElement.classList.add("js");try{var t=localStorage.getItem("theme");'
            'if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t);}catch(e){}})();</script>')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect width='64' height='64' fill='%23f8f7f3'/%3E%3Ctext x='32' y='44' font-family='Georgia,serif' "
           "font-size='34' text-anchor='middle' fill='%23202c32'%3EG%3Ctspan fill='%23305d64'%3E.%3C/tspan%3E%3C/text%3E%3C/svg%3E")


def header(current):
    links = []
    for item in NAV:
        if item is None:
            links.append('<span class="nav-sep" aria-hidden="true"></span>')
            continue
        href, label = item
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    links.append(f'<a class="nav-contact" href="mailto:{EMAIL}">Email me</a>')
    return (
        '<a class="skip" href="#main">Skip to content</a>\n'
        '<header class="header">\n  <div class="wrap nav">\n'
        '    <a class="brand" href="index.html">Gagana M D<span class="brand-dot">.</span></a>\n'
        '    <button class="theme-toggle" id="theme-toggle" type="button" aria-pressed="false" title="Dark theme">'
        '<svg class="icon-moon" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
        '<svg class="icon-sun" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 2.5v2.6M12 18.9v2.6M2.5 12h2.6M18.9 12h2.6M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
        '<span class="visually-hidden">Dark theme</span></button>\n'
        '    <button class="menu" id="menu" type="button" aria-controls="nav-links" aria-expanded="false">Menu</button>\n'
        '    <nav class="nav-links" id="nav-links" aria-label="Main">\n      '
        + "\n      ".join(links)
        + "\n    </nav>\n  </div>\n</header>\n"
    )


FOOTER = f"""<footer class="footer">
  <div class="wrap">
    <span>© <span id="year">2026</span> Gagana M D · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
    <nav aria-label="Elsewhere">
      <a href="https://github.com/GaganaMD" rel="me noopener">GitHub</a>
      <a href="https://www.linkedin.com/in/gaganamd/" rel="me noopener">LinkedIn</a>
      <a href="https://orcid.org/0009-0003-2594-1026" rel="me noopener">ORCID</a>
      <a href="cv.pdf">CV</a>
      <a href="#main">Back to top ↑</a>
    </nav>
  </div>
</footer>
"""


def contact(eyebrow="Contact", title="Get in touch", body=None, links=None):
    body = body or ("I'm looking for a funded research fellowship or research engineering role in empirical AI safety. "
                    "If you work on agent monitoring, control evaluations or multi-agent safety, I'd like to hear what you're testing. "
                    "A short note on the problem and where it's stuck is the best first email.")
    links = links or [
        (f"mailto:{EMAIL}", f"{EMAIL}"),
        ("https://github.com/GaganaMD", "GitHub"),
        ("https://www.linkedin.com/in/gaganamd/", "LinkedIn"),
        ("https://orcid.org/0009-0003-2594-1026", "ORCID"),
    ]
    acts = "".join(f'<a href="{h}">{t} <span aria-hidden="true">↗</span></a>' for h, t in links)
    return (f'<section class="contact" aria-labelledby="contact-title"><div class="wrap contact-inner">'
            f'<p class="eyebrow">{eyebrow}</p><h2 id="contact-title">{title}</h2><p>{body}</p>'
            f'<div class="contact-actions">{acts}</div></div></section>\n')


def page(fname, title, desc, body, extra_head="", scripts=("script.js",), jsonld=None, og_type="website"):
    url = f"{SITE}/" if fname == "index.html" else f"{SITE}/{fname}"
    ld = f'\n<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    sc = "".join(f'\n<script src="{v(s)}" defer></script>' for s in scripts)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">{extra_head}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Gagana M D">
<meta name="theme-color" content="#f8f7f3">
{THEME_JS}
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Gagana M D">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_IN">
<meta property="og:image" content="{SITE}/assets/img/og-card.jpg">
<meta property="og:image:secure_url" content="{SITE}/assets/img/og-card.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Gagana M D, AI safety research: agent monitoring, evaluations and AI control.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/assets/img/og-card.jpg">
<meta name="twitter:image:alt" content="Gagana M D, AI safety research: agent monitoring, evaluations and AI control.">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;family=DM+Serif+Display:ital@0;1&amp;display=swap">
<link rel="stylesheet" href="{v('styles.css')}">{ld}
</head>
<body>
{header(fname)}<main id="main">
{body}</main>
{FOOTER}{sc}
</body>
</html>
"""
    (OUT / fname).write_text(html)


if __name__ == "__main__":
    import importlib.util, sys
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    import content
    for p in content.PAGES:
        page(**p)
    print("built", [p["fname"] for p in content.PAGES])

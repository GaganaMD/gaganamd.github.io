"""Read the editable content in _content/ (YAML and Markdown) and render it as HTML fragments.

The page shell lives in build.py and the page list in content.py; this module only turns
structured content into the exact HTML the pages already use. Needs PyYAML and Markdown:
    py -m pip install -r _build\\requirements.txt"""
import pathlib, sys

try:
    import markdown
    import yaml
except ImportError:  # pragma: no cover - message for a fresh computer
    sys.exit("Missing packages. Run:  py -m pip install -r _build\\requirements.txt")

CONTENT = pathlib.Path(__file__).resolve().parent.parent / "_content"


def load_yaml(name):
    """Load _content/<name> as UTF-8 YAML (safe loader only)."""
    path = CONTENT / name
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def inline_md(text):
    """Render one line of Markdown (links, *emphasis*, **bold**) without the surrounding <p>."""
    html = markdown.markdown(text.strip())
    if html.startswith("<p>") and html.endswith("</p>"):
        html = html[3:-4]
    return html


# ---- Publications -------------------------------------------------------------
def _authors(p, stars=False):
    n = p.get("equal_contribution", 0) if stars else 0
    out = []
    for i, a in enumerate(p["authors"]):
        s = f"<strong>{a}</strong>" if a == p["me"] else a
        out.append(s + ("*" if i < n else ""))
    return ", ".join(out)


def papers_home_html():
    """Homepage "Research papers" list items (publications with a `home` block, by home.order)."""
    pubs = sorted((p for p in load_yaml("publications.yml") if p.get("home")), key=lambda p: p["home"]["order"])
    lines = []
    for p in pubs:
        h = p["home"]
        tag_cls = "ac-tag peer" if h.get("peer") else "ac-tag"
        links = "".join(f'<a href="{l["url"]}">{l["label"]}</a>' for l in h.get("links", []))
        lines += [f'    <li><span class="t">{p["title"]}</span>',
                  f'      <span class="a">{_authors(p)}</span>',
                  f'      <span class="v">{h["venue"]} · <span>{h["role"]}</span></span>',
                  f'      <span class="ac-btns"><span class="{tag_cls}">{h["tag"]}</span>{links}</span></li>']
    return "\n".join(lines)


def pubs_research_html():
    """Research page publication groups (file order; a new <h3> + <ol> whenever `group` changes)."""
    lines, group = [], None
    for p in load_yaml("publications.yml"):
        if p["group"] != group:
            if group is not None:
                lines.append("  </ol>")
            group = p["group"]
            lines += [f'  <h3 class="group-title">{group}</h3>', '  <ol class="pubs">']
        title = f'<a href="{p["url"]}">{p["title"]}</a>' if p.get("url") else p["title"]
        note = inline_md(p["note"])
        if p.get("equal_contribution"):
            note = "*Equal contribution. " + note
        lines += ["    <li>",
                  f'      <p class="pub-title">{title}</p>',
                  f'      <p class="pub-authors">{_authors(p, stars=True)}</p>',
                  f'      <p class="pub-venue">{inline_md(p["venue"])}</p>',
                  f'      <p class="pub-note">{note}</p>',
                  "    </li>"]
    if group is not None:
        lines.append("  </ol>")
    return "\n".join(lines)

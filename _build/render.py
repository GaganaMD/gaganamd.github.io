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


# ---- Research projects (_content/projects/*.md) ------------------------------------
PROJECTS = CONTENT / "projects"


def load_projects():
    """Every _content/projects/*.md (except README.md): YAML front matter between --- lines, then the body."""
    out = []
    for path in sorted(PROJECTS.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        if not text.startswith("---\n") or "\n---\n" not in text[3:]:
            sys.exit(f"{path}: must start with YAML front matter between two --- lines.")
        head, body = text[4:].split("\n---\n", 1)
        meta = yaml.safe_load(head) or {}
        meta["body"] = body.strip("\n")
        meta["_file"] = path.name
        out.append(meta)
    return out


def _entry_html(p):
    lines = [f'    <article class="entry" id="{p["id"]}">', "      <div>",
             f'        <span class="tag">{p["tag"]}</span>', f'        <h3>{p["title"]}</h3>']
    lines += [f"        {line}" for line in p["body"].split("\n") if line.strip()]
    if p.get("role"):
        lines.append(f'        <p class="role">{p["role"]}</p>')
    d = p.get("details")
    if d:
        lines += [f'        <details class="more"><summary>{d["summary"]}</summary>', '        <dl class="facts">']
        lines += [f'          <dt>{f["dt"]}</dt><dd>{f["dd"]}</dd>' for f in d["facts"]]
        lines += ["        </dl>", "        </details>"]
    lines += ["      </div>", '      <div class="entry-side">']
    for s in p.get("side", []):
        if "status" in s:
            lines.append(f'        <span class="status {s["class"]}">{s["status"]}</span>')
        elif "links" in s:
            links = "".join(f'<a href="{l["url"]}">{l["label"]}</a>' for l in s["links"])
            lines.append(f'        <div class="links">{links}</div>')
        else:
            lines.append(f'        <span>{s["text"]}</span>')
    lines += ["      </div>", "    </article>"]
    return "\n".join(lines)


def entries_html(section):
    """Research page project entries for one section ("main" or "earlier"), by `order`, blank line between."""
    ps = sorted((p for p in load_projects() if p.get("section") == section), key=lambda p: p["order"])
    return "\n\n".join(_entry_html(p) for p in ps)


def ongoing_html():
    """Research page "In progress" list."""
    ps = sorted((p for p in load_projects() if p.get("section") == "ongoing"), key=lambda p: p["order"])
    return "\n".join(f'    <li id="{p["id"]}"><strong>{p["title"]}</strong>{p["text"]}</li>' for p in ps)


def current_home_html():
    """Homepage "Current research" list: projects with a `home` block, by home.order."""
    ps = sorted((p for p in load_projects() if p.get("home")), key=lambda p: p["home"]["order"])
    lines = []
    for p in ps:
        h = p["home"]
        cls = f' class="{h["class"]}"' if h.get("class") else ""
        tag = "ac-tag peer" if h.get("peer") else "ac-tag"
        when = f' <span class="when">{h["when"]}</span>' if h.get("when") else ""
        lines.append(f'    <li{cls}><span class="{tag}">{h["tag"]}</span> <strong>{h["title"]}</strong>{when}<br>{h["text"]}</li>')
    return "\n".join(lines)


def code_archive_html():
    """Research page "All code" cards from _content/code.yml, in file order."""
    lines = []
    for c in load_yaml("code.yml"):
        if c.get("gap_before"):
            lines.append("")
        lines += [f'    <article class="archive-item" data-category="{c["category"]}">',
                  f'      <span class="category">{c["label"]}</span>', f'      <h3>{c["title"]}</h3>']
        if "text_lines" in c:
            lines += ["      <p>"] + [f"        {t}" for t in c["text_lines"]] + ["      </p>"]
        else:
            lines.append(f'      <p>{c["text"]}</p>')
        if c.get("evidence"):
            lines.append('      <p class="evidence">' + "".join(f"<span>{e}</span>" for e in c["evidence"]) + "</p>")
        if c.get("meta"):
            lines.append(f'      <p class="meta">{c["meta"]}</p>')
        lines.append("    </article>")
    return "\n".join(lines)

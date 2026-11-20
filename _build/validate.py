"""Structured-content and generated-link validation for _build/check.py."""
import datetime as dt
import pathlib
import re

try:
    import yaml
except ImportError:  # pragma: no cover - handled with a useful check error
    yaml = None

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "_content"
FRAGMENTS = ROOT / "_build" / "pages"
PAGES = ("index.html", "research.html", "detection-is-not-containment.html", "projects.html",
         "writing.html", "about.html", "speaking.html", "consulting.html", "404.html")
ID = re.compile(r"^[A-Za-z][A-Za-z0-9_:-]*$")
# Check the textual shape first, then let datetime give a truthful calendar-date
# diagnostic for values such as 2026-13 or 2026-02-30.
DATE = re.compile(r"^\d{4}-\d{2}(?:-\d{2})?$")


def _where(path):
    return path.relative_to(ROOT).as_posix()


def _yaml(path, problems):
    if yaml is None:
        problems.append("_build/requirements.txt: PyYAML is required; run: py -m pip install -r _build\\requirements.txt")
        return None
    try:
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line = f":{mark.line + 1}" if mark else ""
        problems.append(f"{_where(path)}{line}: malformed YAML: {getattr(exc, 'problem', str(exc))}")
    except OSError as exc:
        problems.append(f"{_where(path)}: cannot read YAML: {exc}")
    return None


def _keys(path, item, allowed, required, label, problems):
    if not isinstance(item, dict):
        problems.append(f"{_where(path)}: {label} must be a mapping")
        return False
    for key in sorted(set(item) - set(allowed)):
        problems.append(f"{_where(path)}: {label}: unknown field '{key}'")
    for key in required:
        if key not in item or item[key] in (None, ""):
            problems.append(f"{_where(path)}: {label}: missing required field '{key}'")
    return True


def _id(path, item, label, seen, problems):
    value = item.get("id") if isinstance(item, dict) else None
    if not isinstance(value, str) or not ID.fullmatch(value):
        problems.append(f"{_where(path)}: {label}: id must be a valid HTML id (letters, digits, _, :, -; starts with a letter)")
        return
    if value in seen:
        problems.append(f"{_where(path)}: {label}: duplicate id '{value}' (also in {seen[value]})")
    else:
        seen[value] = _where(path)


def _list(path, data, name, problems):
    if data is None:
        return []
    if not isinstance(data, list):
        problems.append(f"{_where(path)}: expected a YAML list")
        return []
    return data


def _date(path, value, label, problems):
    if not isinstance(value, str) or not DATE.fullmatch(value):
        problems.append(f"{_where(path)}: {label}: date must be a quoted YYYY-MM or YYYY-MM-DD string")
        return
    try:
        if len(value) == 7:
            dt.datetime.strptime(value, "%Y-%m")
        else:
            dt.datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        problems.append(f"{_where(path)}: {label}: invalid calendar date '{value}'")


def _home(path, home, label, problems, fields=("order", "title", "org", "when")):
    if not _keys(path, home, {"order", "title", "org", "when", "description", "tag", "peer", "class", "text", "venue", "role", "links"}, fields, label, problems):
        return
    if "order" in home and not isinstance(home["order"], int):
        problems.append(f"{_where(path)}: {label}.order must be an integer")


def _news(problems):
    path = CONTENT / "news.yml"
    seen = set()
    for i, item in enumerate(_list(path, _yaml(path, problems), "news", problems), 1):
        label = f"news item {i}"
        if _keys(path, item, {"date", "text"}, {"date", "text"}, label, problems):
            _date(path, item.get("date"), label, problems)


def _publications(problems):
    path = CONTENT / "publications.yml"
    seen = {}
    for i, item in enumerate(_list(path, _yaml(path, problems), "publications", problems), 1):
        label = f"publication {i}"
        if not _keys(path, item, {"id", "title", "url", "authors", "me", "equal_contribution", "group", "venue", "note", "home"},
                     {"id", "title", "authors", "me", "group", "venue", "note"}, label, problems):
            continue
        _id(path, item, label, seen, problems)
        authors = item.get("authors")
        if not isinstance(authors, list) or not all(isinstance(a, str) and a for a in authors):
            problems.append(f"{_where(path)}: {label}.authors must be a non-empty list of names")
        elif item.get("me") not in authors:
            problems.append(f"{_where(path)}: {label}.me must be one of authors")
        if item.get("home") is not None:
            home = item["home"]
            _home(path, home, f"{label}.home", problems, ("order", "venue", "role", "tag", "links"))
            if isinstance(home, dict):
                links = home.get("links")
                if not isinstance(links, list):
                    problems.append(f"{_where(path)}: {label}.home.links must be a list")
                else:
                    for n, link in enumerate(links, 1):
                        if not isinstance(link, dict) or not link.get("url"):
                            problems.append(f"{_where(path)}: {label}.home.links[{n}].url must be non-empty")


def _project(path, problems, seen):
    try:
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except OSError as exc:
        problems.append(f"{_where(path)}: cannot read Markdown: {exc}")
        return
    if not text.startswith("---\n"):
        problems.append(f"{_where(path)}: missing YAML frontmatter opening '---'")
        return
    end = text.find("\n---\n", 4)
    if end < 0:
        problems.append(f"{_where(path)}: missing YAML frontmatter closing '---'")
        return
    if yaml is None:
        problems.append(f"_build/requirements.txt: PyYAML is required; run: py -m pip install -r _build\\requirements.txt")
        return
    try:
        item = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line = f":{mark.line + 2}" if mark else ""
        problems.append(f"{_where(path)}{line}: malformed YAML frontmatter: {getattr(exc, 'problem', str(exc))}")
        return
    label = "frontmatter"
    allowed = {"id", "section", "order", "tag", "title", "role", "details", "side", "home", "text"}
    if not _keys(path, item, allowed, {"id", "section"}, label, problems):
        return
    _id(path, item, label, seen, problems)
    section = item.get("section")
    if section not in {"main", "earlier", "ongoing", "home-only"}:
        problems.append(f"{_where(path)}: frontmatter.section must be main, earlier, ongoing or home-only")
    if section != "home-only" and not isinstance(item.get("order"), int):
        problems.append(f"{_where(path)}: frontmatter.order must be an integer")
    if section in {"main", "earlier"}:
        _keys(path, item, allowed, {"id", "section", "order", "tag", "title"}, label, problems)
        if not text[end + 5:].strip():
            problems.append(f"{_where(path)}: {item.get('id', label)} needs a Markdown/HTML body")
    if section == "ongoing":
        _keys(path, item, allowed, {"id", "section", "order", "title", "text"}, label, problems)
    if section == "home-only" and item.get("home") is None:
        problems.append(f"{_where(path)}: {item.get('id', label)} needs a home block")
    if item.get("home") is not None:
        _home(path, item["home"], f"{item.get('id', label)}.home", problems, ("order", "tag", "title", "text"))


def _projects(problems):
    directory = CONTENT / "projects"
    if not directory.is_dir():
        problems.append("_content/projects: missing project content directory")
        return
    seen = {}
    for path in sorted(directory.glob("*.md")):
        if path.name.lower() != "readme.md":
            _project(path, problems, seen)


def _code(problems):
    path = CONTENT / "code.yml"
    allowed = {"category", "label", "title", "text", "text_lines", "evidence", "meta", "gap_before"}
    for i, item in enumerate(_list(path, _yaml(path, problems), "code", problems), 1):
        label = f"code card {i}"
        if _keys(path, item, allowed, {"category", "label", "title"}, label, problems):
            if item.get("category") not in {"research", "agents", "rl", "applied"}:
                problems.append(f"{_where(path)}: {label}.category must match a Research-page filter")
            if ("text" in item) == ("text_lines" in item):
                problems.append(f"{_where(path)}: {label} needs exactly one of text or text_lines")


def _experience(problems):
    path = CONTENT / "experience.yml"
    seen = {}
    for i, item in enumerate(_list(path, _yaml(path, problems), "experience", problems), 1):
        label = f"experience item {i}"
        if not _keys(path, item, {"id", "home", "about"}, {"id"}, label, problems):
            continue
        _id(path, item, label, seen, problems)
        if not item.get("home") and not item.get("about"):
            problems.append(f"{_where(path)}: {label} needs home and/or about")
        if item.get("home") is not None:
            _home(path, item["home"], f"{label}.home", problems)
        if item.get("about") is not None:
            about = item["about"]
            if _keys(path, about, {"order", "group", "time", "title", "position", "multiline", "paragraphs"},
                     {"order", "group", "time", "title", "position", "paragraphs"}, f"{label}.about", problems):
                if not isinstance(about.get("order"), int):
                    problems.append(f"{_where(path)}: {label}.about.order must be an integer")
                if not isinstance(about.get("paragraphs"), list) or not about["paragraphs"]:
                    problems.append(f"{_where(path)}: {label}.about.paragraphs must be a non-empty list")


def _service(problems):
    path = CONTENT / "service.yml"
    seen = {}
    for i, item in enumerate(_list(path, _yaml(path, problems), "service", problems), 1):
        label = f"service item {i}"
        if _keys(path, item, {"id", "title", "org", "when", "description"}, {"id", "title", "org", "when"}, label, problems):
            _id(path, item, label, seen, problems)


def content_problems():
    """Return actionable structured-content and source-template errors without writing files."""
    problems = []
    templates = {
        "index.html": ("@@NEWS@@", "@@PAPERS_HOME@@", "@@CURRENT_HOME@@", "@@EXPERIENCE_HOME@@", "@@SERVICE_HOME@@"),
        "research.html": ("@@ENTRIES_MAIN@@", "@@ONGOING@@", "@@PUBS_RESEARCH@@", "@@CODE_ARCHIVE@@", "@@ENTRIES_EARLIER@@"),
        "about.html": ("@@EXPERIENCE_ABOUT@@",),
        "detection-is-not-containment.html": (), "writing.html": (), "speaking.html": (), "consulting.html": (),
    }
    for name, markers in templates.items():
        path = FRAGMENTS / name
        if not path.is_file():
            problems.append(f"_build/pages/{name}: missing page template")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if text.count(marker) != 1:
                problems.append(f"_build/pages/{name}: missing or duplicate placeholder {marker}")
    _news(problems)
    _publications(problems)
    _projects(problems)
    _code(problems)
    _experience(problems)
    _service(problems)
    return problems


def link_problems():
    """Check generated local .html links and anchors after a successful build."""
    pages = {name: ROOT / name for name in PAGES}
    anchors = {}
    for name, path in pages.items():
        if not path.is_file():
            return [f"{name}: generated page is missing"]
        anchors[name] = set(re.findall(r'\bid=["\']([^"\']+)["\']', path.read_text(encoding="utf-8")))
    problems = []
    for name, path in pages.items():
        html = path.read_text(encoding="utf-8")
        for href in re.findall(r'\bhref=["\']([^"\']+)["\']', html):
            if href.startswith(("http:", "https:", "mailto:", "tel:", "data:")):
                continue
            target, sep, anchor = href.partition("#")
            if not target and not sep:
                continue
            target = target or name
            if target not in pages:
                if target.endswith(".html"):
                    problems.append(f'{name}: internal link "{href}" targets missing page {target}')
                continue
            if sep and anchor and anchor not in anchors[target]:
                problems.append(f'{name}: internal link "{href}" targets missing anchor #{anchor} in {target}')
    return problems

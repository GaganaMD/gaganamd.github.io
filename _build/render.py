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

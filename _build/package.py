"""Create and verify the explicitly allowlisted static GitHub Pages artifact.

Usage:
  python -B _build/package.py PATH
  python -B _build/package.py --verify PATH
  python -B _build/package.py --self-test
"""
import argparse
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ("index.html", "research.html", "detection-is-not-containment.html", "projects.html",
         "writing.html", "about.html", "speaking.html", "consulting.html", "404.html")
ROOT_FILES = PAGES + ("styles.css", "script.js", "speaking.js", "cv.pdf", "robots.txt", "sitemap.xml")
ASSET_FILES = (
    "assets/img/gagana-md-440.jpg",
    "assets/img/gagana-md-640.jpg",
    "assets/img/gagana-md.jpg",
    "assets/img/ingarss-2025-poster-960.jpg",
    "assets/img/ingarss-2025-poster.jpg",
    "assets/img/og-card.jpg",
    "assets/img/speaking-wibd-github-workshop-960.jpg",
    "assets/img/speaking-wibd-github-workshop.jpg",
    "assets/research/dinc-fig1-evidence-representation.png",
    "assets/research/dinc-fig3-closed-loop.png",
)
PUBLIC_FILES = tuple(pathlib.PurePosixPath(path) for path in ROOT_FILES + ASSET_FILES)
PUBLIC_SET = frozenset(PUBLIC_FILES)
HTML_ATTR = re.compile(r'''\b(?:href|src)=["']([^"']+)["']|\bsrcset=["']([^"']+)["']''')
CSS_URL = re.compile(r"url\((?:[\"']?)([^\"')]+)(?:[\"']?)\)")
JS_LOCAL = re.compile(r'''["']((?:assets/)?[A-Za-z0-9_./-]+\.(?:css|js|html|jpg|jpeg|png|gif|webp|svg|pdf))["']''')
COMMENT = re.compile(r"/\*.*?\*/|//[^\n]*", re.DOTALL)


def allowed(rel):
    """Only a declared public file is eligible; unknown root and asset files are denied."""
    return pathlib.PurePosixPath(rel) in PUBLIC_SET


def source_path(rel):
    path = ROOT.joinpath(*pathlib.PurePosixPath(rel).parts)
    parent = ROOT
    for part in pathlib.PurePosixPath(rel).parts:
        parent = parent / part
        if parent.is_symlink():
            raise SystemExit(f"Refusing to package symlinked public path: {rel}")
    if not path.is_file():
        raise SystemExit(f"Required public file is missing: {rel}")
    return path


def local_path(ref):
    """Return a local package path, or None for anchors, external URLs and data URLs."""
    ref = ref.strip().split("#", 1)[0].split("?", 1)[0]
    if not ref or ref.startswith(("/", "http:", "https:", "mailto:", "tel:", "data:")):
        return None
    return pathlib.PurePosixPath(ref)


def references():
    """Declared local file references in the generated HTML, CSS and JavaScript."""
    out = []
    for page in PAGES:
        text = source_path(page).read_text(encoding="utf-8")
        for href, srcset in HTML_ATTR.findall(text):
            if href:
                path = local_path(href)
                if path:
                    out.append((page, path))
            else:
                for candidate in srcset.split(","):
                    path = local_path(candidate.strip().split()[0])
                    if path:
                        out.append((page, path))
    for name in ("styles.css", "script.js", "speaking.js"):
        text = COMMENT.sub("", source_path(name).read_text(encoding="utf-8"))
        matches = CSS_URL.findall(text) if name == "styles.css" else JS_LOCAL.findall(text)
        for ref in matches:
            path = local_path(ref)
            if path:
                out.append((name, path))
    return out


def verify_references(destination):
    problems = []
    for source, rel in references():
        if not allowed(rel):
            problems.append(f"{source}: local reference is not allowlisted: {rel}")
        elif not (destination / rel).is_file():
            problems.append(f"{source}: local reference is missing from artifact: {rel}")
    return problems


def package(destination):
    destination = destination.resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise SystemExit("Artifact destination must be outside the repository root.")
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit(f"Artifact destination is not empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    for rel in sorted(PUBLIC_FILES, key=str):
        source = source_path(rel)
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    verify(destination)
    print(f"Packaged {len(PUBLIC_FILES)} explicitly allowlisted public files in {destination}")


def verify(destination):
    destination = destination.resolve()
    if not destination.is_dir() or destination.is_symlink():
        raise SystemExit(f"Artifact directory is missing or symlinked: {destination}")
    actual = {pathlib.PurePosixPath(path.relative_to(destination).as_posix())
              for path in destination.rglob("*") if path.is_file()}
    missing = PUBLIC_SET - actual
    unexpected = actual - PUBLIC_SET
    problems = [f"missing allowlisted public file: {path}" for path in sorted(missing, key=str)]
    problems += [f"unexpected file in artifact: {path}" for path in sorted(unexpected, key=str)]
    for page in PAGES:
        rel = pathlib.PurePosixPath(page)
        if rel in actual and (destination / rel).read_bytes() != source_path(rel).read_bytes():
            problems.append(f"generated page differs from source root: {page}")
    problems += verify_references(destination)
    if problems:
        raise SystemExit("Invalid Pages artifact:\n  " + "\n  ".join(problems))
    print(f"Artifact verification passed: {len(PAGES)} generated pages and {len(PUBLIC_FILES)} allowlisted files")


def self_test():
    """Focused policy checks; no files are written."""
    required = {pathlib.PurePosixPath(path) for path in ROOT_FILES + ASSET_FILES}
    assert required == PUBLIC_SET
    assert not allowed("unexpected.txt")
    assert not allowed("assets/img/options/private.png")
    assert not allowed("assets/unapproved.png")
    assert all(allowed(path) for path in required)
    print("Allowlist self-test passed: required files included; unknown root and asset files rejected")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--verify", action="store_true", help="verify an existing artifact instead of creating one")
    parser.add_argument("--self-test", action="store_true", help="run focused allowlist policy checks without writing files")
    parser.add_argument("destination", nargs="?", type=pathlib.Path)
    args = parser.parse_args()
    if args.self_test:
        if args.destination:
            parser.error("--self-test does not take a destination")
        self_test()
    elif args.destination is None:
        parser.error("destination is required unless --self-test is used")
    elif args.verify:
        verify(args.destination)
    else:
        package(args.destination)


if __name__ == "__main__":
    main()

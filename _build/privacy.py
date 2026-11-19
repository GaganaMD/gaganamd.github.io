"""Privacy guard shared by check.py and site.py (standard library only).

Finds phone-number-like text in tracked files and private paths that must never be tracked.
It reports the file and line only; matched text is never printed."""
import pathlib, re, shutil, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent

# A plus sign, country code and 10 digits; two groups of five digits; or 10-12 digits in a row.
# Deliberately narrow so DOIs, arXiv ids, dates and the ?v= fingerprints do not match.
PHONE = re.compile(r"(?<![\w.])(?:\+\d{1,3}[ -]?\d{3,5}[ -]?\d{3,5}(?:[ -]?\d{1,5})?|\d{5}[ -]\d{5}|\d{10,12})(?![\w.])")
PRIVATE_PATH = re.compile(r"(^|/)(_private/|contact\.tex$|cv-private[^/]*$|[^/]*\.private\.[^/]*$|Claude outputs/)")
BINARY = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".ico", ".pdf", ".zip", ".bundle", ".woff", ".woff2"}


def tracked_files():
    if not shutil.which("git"):
        return None
    # Tracked files plus new files git would pick up with "git add" (ignored files are excluded).
    r = subprocess.run(["git", "--no-optional-locks", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                       cwd=ROOT, capture_output=True)
    if r.returncode:
        return None
    return [p for p in r.stdout.decode("utf-8", "replace").split("\0") if p]


def phone_lines(text):
    return [i for i, line in enumerate(text.splitlines(), 1) if PHONE.search(line)]


def problems():
    """List of human-readable problems (empty list = OK). None if git is unavailable."""
    files = tracked_files()
    if files is None:
        return None
    out = []
    for f in files:
        if PRIVATE_PATH.search(f):
            out.append(f"{f}: private file is tracked or not ignored by git (move it into _private/ or run: git rm --cached \"{f}\")")
            continue
        p = ROOT / f
        if p.suffix.lower() in BINARY or not p.is_file():
            continue
        lines = phone_lines(p.read_text(encoding="utf-8", errors="replace"))
        if lines:
            out.append(f"{f}: phone-number-like text on line(s) {', '.join(map(str, lines))} (text not shown)")
    pdf = ROOT / "cv.pdf"
    if pdf.exists() and shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True)
        if phone_lines(r.stdout.decode("utf-8", "replace")):
            out.append("cv.pdf: phone-number-like text in the public CV (text not shown)")
    return out

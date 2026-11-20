"""Pre-push check: the generated pages and the assets they reference must belong together.

Run from anywhere:  python _build/check.py
Fails (exit 1) if any page links a stylesheet or script whose ?v= fingerprint doesn't match the
file on disk, or if rebuilding from _build/ would change any generated page,
or if a tracked file contains phone-number-like text or a private file (see _build/privacy.py). Run it before every
commit so new HTML is never published with an old stylesheet, or the reverse."""
import hashlib, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "research.html", "detection-is-not-containment.html", "projects.html",
         "writing.html", "about.html", "speaking.html", "consulting.html", "404.html"]
sys.dont_write_bytecode = True  # keep _build/ free of __pycache__
problems = []
sys.path.insert(0, str(ROOT / "_build"))
import validate  # noqa: E402
problems += validate.content_problems()
for page in PAGES:
    html = (ROOT / page).read_text(encoding="utf-8")
    for name, ver in re.findall(r'(?:href|src)="([\w.-]+\.(?:css|js))\?v=([0-9a-f]+)"', html):
        actual = hashlib.sha256((ROOT / name).read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:10]
        if ver != actual:
            problems.append(f"{page}: {name}?v={ver} but the file on disk is v={actual}")
    if re.search(r'(?:href|src)="(?:styles\.css|script\.js|speaking\.js)"', html):
        problems.append(f"{page}: links an asset without a fingerprint")
before = {p: (ROOT / p).read_bytes() for p in PAGES}
build = None
if not problems:  # schema errors are already actionable; do not bury them under a renderer traceback
    build = subprocess.run([sys.executable, "-B", str(ROOT / "_build" / "build.py")], capture_output=True)
    if build.returncode:
        detail = (build.stderr or build.stdout).decode("utf-8", "replace").strip()
        problems.append("BUILD: " + (detail or "python _build/build.py failed"))
    else:
        problems += validate.link_problems()
    for p in PAGES:
        if (ROOT / p).read_bytes().replace(b"\r\n", b"\n") != before[p].replace(b"\r\n", b"\n"):
            problems.append(f"{p}: out of date; rebuilding changes it (run python _build/build.py and commit the result)")
        if (ROOT / p).read_bytes() != before[p]:
            (ROOT / p).write_bytes(before[p])  # always leave the working copy exactly as it was
import privacy  # noqa: E402  (phone numbers and private files must never be committed)
priv = privacy.problems()
if priv is None:
    print("WARNING: git not found, so the privacy check was skipped.")
else:
    problems += ["PRIVACY " + x for x in priv]
if problems:
    print("NOT READY TO PUSH:\n  " + "\n  ".join(problems)); sys.exit(1)
print(f"OK: {len(PAGES)} pages are up to date and every stylesheet/script fingerprint matches the file on disk; no private data is tracked.")

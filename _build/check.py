"""Pre-push check: the generated pages and the assets they reference must belong together.

Run from anywhere:  python _build/check.py
Fails (exit 1) if any page links a stylesheet or script whose ?v= fingerprint doesn't match the
file on disk, or if rebuilding from _build/ would change any generated page. Run it before every
commit so new HTML is never published with an old stylesheet, or the reverse."""
import hashlib, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "research.html", "detection-is-not-containment.html", "projects.html",
         "writing.html", "about.html", "speaking.html", "consulting.html", "404.html"]
problems = []
for page in PAGES:
    html = (ROOT / page).read_text()
    for name, ver in re.findall(r'(?:href|src)="([\w.-]+\.(?:css|js))\?v=([0-9a-f]+)"', html):
        actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()[:10]
        if ver != actual:
            problems.append(f"{page}: {name}?v={ver} but the file on disk is v={actual}")
    if re.search(r'(?:href|src)="(?:styles\.css|script\.js|speaking\.js)"', html):
        problems.append(f"{page}: links an asset without a fingerprint")
before = {p: (ROOT / p).read_bytes() for p in PAGES}
subprocess.run([sys.executable, "-B", str(ROOT / "_build" / "build.py")], check=True, capture_output=True)
for p in PAGES:
    if (ROOT / p).read_bytes() != before[p]:
        problems.append(f"{p}: out of date; rebuilding changes it (run python _build/build.py and commit the result)")
        (ROOT / p).write_bytes(before[p])
if problems:
    print("NOT READY TO PUSH:\n  " + "\n  ".join(problems)); sys.exit(1)
print(f"OK: {len(PAGES)} pages are up to date and every stylesheet/script fingerprint matches the file on disk.")

"""One entry point for maintaining the site. Run from the repository folder.

Stage 1A provides the CV commands; preview, build and check arrive in later stages.

  py _build\\site.py cv             Public CV preview  -> _private\\cv-public-preview.pdf (no phone number)
  py _build\\site.py cv --private   Application CV     -> _private\\cv-private.pdf (with your phone number)

The private CV reads your phone number from _private\\contact.tex, which git ignores. See cv/README.md.
The public cv.pdf on the website is built by GitHub Actions from cv/main.tex; this script never touches it."""
import argparse, pathlib, shutil, subprocess, sys

sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parent.parent
CV, PRIVATE = ROOT / "cv", ROOT / "_private"
BUILD = PRIVATE / "cv-build"
CONTACT = PRIVATE / "contact.tex"
sys.path.insert(0, str(ROOT / "_build"))
import privacy  # noqa: E402


def git_ok(*args):
    return shutil.which("git") and subprocess.run(["git", "--no-optional-locks", *args], cwd=ROOT,
                                                  capture_output=True).returncode == 0


def ensure_private(path):
    """Refuse to continue if a private file could end up in git."""
    rel = path.relative_to(ROOT).as_posix()
    if not shutil.which("git"):
        sys.exit("git not found: can't confirm the private files are ignored, so nothing was built.")
    if git_ok("ls-files", "--error-unmatch", rel):
        sys.exit(f"STOP: {rel} is tracked by git. Run: git rm --cached \"{rel}\" and check .gitignore.")
    if not git_ok("check-ignore", "-q", rel):
        sys.exit(f"STOP: {rel} is not ignored by git. Add _private/ to .gitignore first.")


def latex(jobname, source, private):
    exe = shutil.which("pdflatex")
    if not exe:
        sys.exit("pdflatex not found. Install MiKTeX (https://miktex.org/download), reopen the terminal, "
                 "and check with: pdflatex --version")
    BUILD.mkdir(parents=True, exist_ok=True)
    ensure_private(BUILD)
    for _ in range(2):  # twice, so hyperref links settle
        r = subprocess.run([exe, "-interaction=nonstopmode", "-halt-on-error", f"-jobname={jobname}",
                            f"-output-directory={BUILD}", source], cwd=CV, capture_output=True)
        if r.returncode:
            log = BUILD / f"{jobname}.log"
            if private:  # the log could echo the phone number, so don't print it
                sys.exit(f"LaTeX failed. Open {log} to see why.")
            tail = r.stdout.decode("utf-8", "replace").splitlines()[-25:]
            sys.exit("LaTeX failed:\n" + "\n".join(tail) + f"\n(full log: {log})")
    return BUILD / f"{jobname}.pdf"


def cv(private):
    PRIVATE.mkdir(exist_ok=True)
    if private:
        if not CONTACT.exists():
            sys.exit(f"Missing {CONTACT}. Create it with one line:  \\def\\cvphone{{YOUR PHONE NUMBER}}")
        ensure_private(CONTACT)
        pdf = latex("cv-private", r"\input{../_private/contact.tex}\input{main.tex}", True)
        out = PRIVATE / "cv-private.pdf"
    else:
        if privacy.phone_lines((CV / "main.tex").read_text(encoding="utf-8")):
            sys.exit("STOP: cv/main.tex contains phone-number-like text. Keep the number only in _private/contact.tex.")
        pdf = latex("cv-public", "main.tex", False)
        out = PRIVATE / "cv-public-preview.pdf"
    shutil.copyfile(pdf, out)
    ensure_private(out)
    print(f"Built {out.relative_to(ROOT)}" + ("  (private: never upload or commit it)" if private else ""))


def main():
    ap = argparse.ArgumentParser(prog="site.py", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cv", help="build the public CV preview, or the private application CV")
    c.add_argument("--private", action="store_true", help="include the phone number from _private/contact.tex")
    a = ap.parse_args()
    if a.cmd == "cv":
        cv(a.private)


if __name__ == "__main__":
    main()

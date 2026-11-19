# CV source

`cv/main.tex` is the single source for both versions of the CV.

| Version | Phone number | Built by | Where it ends up |
|---|---|---|---|
| **Public** | No | GitHub Actions (`.github/workflows/build-cv.yml`) on every push that changes `cv/` | `cv.pdf` at the site root: https://gaganamd.github.io/cv.pdf (the URL never changes) |
| **Private** (applications) | Yes | You, on your own computer | `_private\cv-private.pdf` (gitignored, never published) |

`main.tex` never contains the phone number. It prints one only if `\cvphone` is defined, and only the
private build defines it, from the gitignored file `_private/contact.tex`. The public build cannot show a
number, and the workflow refuses to publish a CV whose source or PDF contains phone-number-like text.

## Update the public CV

Edit `cv/main.tex` (on github.com, in VS Code, or in Overleaf) and push. The workflow compiles it, checks
it, and commits `cv.pdf`. Check the run under the repository's **Actions** tab.

From Overleaf: Menu → Download → Source, then on github.com open this folder → Add file → Upload files →
upload **only `main.tex`** (and any images it needs) → Commit.

> **Never put your phone number in the Overleaf project or anywhere in `cv/`.** `.gitignore` does not apply
> to files uploaded through the GitHub website, so anything you upload becomes public immediately.

## Build the private CV (with your phone number)

One-time setup:

1. Install MiKTeX (https://miktex.org/download). During setup, allow it to install missing packages automatically.
2. Check it in a new terminal: `pdflatex --version`
3. Create `_private\contact.tex` in the repository folder containing one line:
   `\def\cvphone{YOUR PHONE NUMBER}` (replace the capitals with your number, including the country code). Git ignores the whole `_private\` folder.

Then, from the repository folder:

```powershell
py _build\site.py cv --private     # -> _private\cv-private.pdf  (with phone)
py _build\site.py cv               # -> _private\cv-public-preview.pdf  (preview of the public version)
```

The script refuses to run if `_private\` is not ignored by git, and never prints your number.

Without the script (same result):

```powershell
cd cv
pdflatex -jobname=cv-private -output-directory=..\_private "\input{../_private/contact.tex}\input{main.tex}"
pdflatex -jobname=cv-private -output-directory=..\_private "\input{../_private/contact.tex}\input{main.tex}"
```

Overleaf settings to match the workflow: pdfLaTeX. If you switch to XeLaTeX or LuaLaTeX, set
`latexmk_use_xelatex: true` in the workflow.

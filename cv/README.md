# CV source

Put your CV's LaTeX files here, with the main file named `main.tex`. Include any `.cls`, `.sty`, `.bib` or images it needs.

Every push that changes this folder runs `.github/workflows/build-cv.yml`. The workflow compiles the PDF and commits it to the site root as `cv.pdf`, so https://gaganamd.github.io/cv.pdf always serves the latest version.

From Overleaf (free plan): Menu → Download → Source. Unzip the download, then on github.com open this folder → Add file → Upload files → drop the files in → Commit.

Overleaf build settings to match: if your project uses XeLaTeX or LuaLaTeX, set `latexmk_use_xelatex: true` in the workflow.

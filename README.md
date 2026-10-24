# gaganamd.github.io

Personal research site of Gagana M D, served by GitHub Pages from `main` with no build step.

## Structure

| File | Purpose |
|---|---|
| `index.html` | Home: research-first summary, selected work, contact |
| `research.html` | All research, with a status label for each project |
| `detection-is-not-containment.html` | Case study for the main public research artifact |
| `projects.html` | Filterable project archive with code links |
| `writing.html` | Technical write-ups and articles |
| `about.html` | Background, experience, education, community |
| `speaking.html`, `speaking.js` | Talks, workshops, community programs; optional photo gallery |
| `consulting.html` | Scoped evaluation-review work |
| `styles.css`, `script.js` | Shared styles; small enhancements (mobile menu, filters, redirects for old `#anchors`) |
| `404.html`, `robots.txt`, `sitemap.xml` | Housekeeping |

Every page renders fully without JavaScript. Header and footer are repeated in each file, so update all pages when changing navigation.

## Editing rules

- Only add claims that a reviewer can check, or label them clearly as in progress or not public.
- Don't call a submission accepted until there's a decision.
- The portrait is intentionally disabled (commented out in `index.html`). Don't add a placeholder.
- The historical Shakti cohort metrics in `speaking.html` stay commented out until the current program ends.
- Speaking photos: add real event photos to `assets/speaking/` and list them in `speaking.js`.

## Checks

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

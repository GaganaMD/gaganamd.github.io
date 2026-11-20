# Research projects

One Markdown file per project. The YAML front matter (between the `---` lines) holds the fields; the
body holds the description paragraphs for the Research page, one HTML paragraph per line.

| Field | Meaning |
|---|---|
| `id` | Anchor on the Research page (`research.html#id`). Never change an existing one: other pages link to it. |
| `section` | `main` (Projects), `earlier` (Before and beside AI safety), `ongoing` (In progress list) or `home-only` (homepage list only) |
| `order` | Position within its section |
| `tag`, `title` | Small label and heading (HTML allowed) |
| `role` | The "My part" line (HTML, including `<strong>My part:</strong>`) |
| `text` | For `ongoing` items: the sentence after the title |
| `details` | Optional "Method, results and limits" box: `summary` and a list of `facts` (`dt` label, `dd` HTML) |
| `side` | Right-hand panel, in order: `{status, class}` (class `done` or `ongoing`), `{text}`, or `{links: [{label, url}]}` |
| `home` | Optional homepage "Current research" item: `order`, `tag`, `peer` (green tag), `class` (`planned`), `title`, `when`, `text` |

Keep wording, numbers and credits exactly as published; edit the text, then rebuild and check.

# Gagana M D — Research Portfolio

Personal research portfolio focused on AI safety. It is a simple static website designed to work directly with GitHub Pages—there is no build step, package manager, or framework.

## Repository structure

```text
index.html     Page content and semantic structure
styles.css     Visual design and responsive layout
script.js      Optional links and the mobile navigation
assets/        Put a CV PDF or other small site assets here
README.md      This guide
```

## Edit the content

Most text is in `index.html`. Search for the section you want, such as `Selected Research`, and update its heading, context, description, or tags.

Keep research claims precise. Do not turn workshop work or a submission into an accepted publication unless that status is confirmed.

## Add personal links

Open `script.js` and update the `links` object:

```js
const links = {
  github: "https://github.com/your-username",
  email: "you@example.com",
  cv: "assets/gagana-md-cv.pdf",
};
```

The site intentionally hides any blank link. This means visitors never see unfinished buttons or placeholder URLs. For a CV, put the PDF in `assets/` and use its relative path as above.

## Add a project link

In `script.js`, find the relevant project key inside `projectLinks`, then add only the links that exist:

```js
"agent-trace": {
  code: "https://github.com/your-username/agent-trace",
  project: "https://example.com/project-page"
},
```

Available labels are `paper`, `code`, `project`, and `results`. A blank or missing link stays hidden.

## Add another project

1. Copy one `<article class="project">…</article>` block in the `Selected Research` section of `index.html`.
2. Change its number, title, context, description, and tags.
3. Give the project-links container a new `data-project-links` value.
4. Add the matching key to `projectLinks` in `script.js`.

## Add research writing later

The `Research & Writing` section is already present but hidden because there are no finalized entries. When there is a verified paper, preprint, submission, or work in progress, add its content in `index.html`, then remove `is-hidden` from that section. State the status accurately.

## Run locally

You can open `index.html` directly in a browser. For a small local web server, from this folder run:

```powershell
python -m http.server 8000
```

Then visit `http://localhost:8000`. Stop the server with `Ctrl+C`.

## First commit

After creating an empty GitHub repository, open PowerShell in this folder and run:

```powershell
git init
git add index.html styles.css script.js README.md assets
git commit -m "Create AI safety research portfolio"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/YOUR-REPOSITORY-NAME.git
git push -u origin main
```

Replace the all-caps parts with your GitHub username and repository name. If Git was already initialized, skip `git init`.

## Deploy with GitHub Pages

For a personal site at `https://YOUR-GITHUB-USERNAME.github.io/`, name the repository exactly `YOUR-GITHUB-USERNAME.github.io`.

1. On GitHub, open the repository.
2. Select **Settings** → **Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select the `main` branch and the `/ (root)` folder, then click **Save**.
5. Wait for the Pages deployment confirmation. The site address appears on the same screen.

For later edits, use the usual Git workflow: `git status`, `git add`, `git commit -m "Describe the change"`, and `git push`. GitHub Pages republishes after the push.

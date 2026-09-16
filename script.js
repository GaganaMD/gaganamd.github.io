/*
 * Personal links and project links live here so the visible site never shows
 * unfinished URLs. Add a complete URL to make its matching link appear.
 */
const links = {
  github: "https://github.com/GaganaMD", // TODO: e.g. https://github.com/your-username
  email: "gaganaaa.dev@gmail.com", // TODO: e.g. hello@example.com (do not include 'mailto:')
  linkedin: "https://www.linkedin.com/in/gaganamd/", // TODO: e.g. assets/gagana-md-cv.pdf
};

const projectLinks = {
  "intervention-aware-monitoring": { /* paper: "", code: "", project: "", results: "" */ },
  "world-models-physical-ai": { /* paper: "", code: "", project: "", results: "" */ },
  "secret-loyalties": { /* paper: "", code: "", project: "", results: "" */ },
  "agent-trace": { /* paper: "", code: "", project: "", results: "" */ },
  "latent-manifold-sandbox": { /* paper: "", code: "", project: "", results: "" */ },
};

function externalAttributes(url) {
  return /^https?:\/\//.test(url) ? ' target="_blank" rel="noreferrer"' : "";
}

document.querySelectorAll("[data-link]").forEach((element) => {
  const key = element.dataset.link;
  let url = links[key];
  if (key === "email" && url) url = `mailto:${url}`;
  if (!url) return;
  element.href = url;
  if (/^https?:\/\//.test(url)) {
    element.target = "_blank";
    element.rel = "noreferrer";
  }
  element.classList.remove("is-hidden");
});

document.querySelectorAll("[data-project-links]").forEach((container) => {
  const itemLinks = projectLinks[container.dataset.projectLinks] || {};
  Object.entries(itemLinks).forEach(([label, url]) => {
    if (!url) return;
    const link = document.createElement("a");
    link.href = url;
    link.innerHTML = `${label.charAt(0).toUpperCase() + label.slice(1)} <span aria-hidden="true">↗</span>`;
    if (/^https?:\/\//.test(url)) { link.target = "_blank"; link.rel = "noreferrer"; }
    container.append(link);
  });
});

const menuButton = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");
menuButton.addEventListener("click", () => {
  const open = navLinks.classList.toggle("is-open");
  menuButton.setAttribute("aria-expanded", String(open));
  menuButton.textContent = open ? "Close" : "Menu";
});
navLinks.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
  navLinks.classList.remove("is-open"); menuButton.setAttribute("aria-expanded", "false"); menuButton.textContent = "Menu";
}));

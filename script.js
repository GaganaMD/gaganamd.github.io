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

/*
 * Broader project archive. Add URLs only when they are ready to publish;
 * blank links are not rendered. A project may belong to more than one category.
 */
const projectArchive = [
  {
    title: "Intervention-Aware Monitoring",
    categories: ["safety"],
    description: "Exploring monitoring and control mechanisms for AI agents operating around restricted actions and safety-critical boundaries, connecting agent control with systems-security ideas such as fail-closed authorization, privilege separation, and provenance.",
    tags: ["AI Control", "Monitoring", "Agent Security"],
    links: { github: "", paper: "", demo: "", report: "" },
  },
  {
    title: "Secret Loyalties",
    categories: ["safety"],
    description: "An agent-evaluation project studying whether hidden loyalties and competing objectives can be detected when evaluators have limited observability into an agent’s behaviour.",
    tags: ["Agent Evaluation", "Hidden Objectives", "Auditing"],
    links: { github: "", paper: "", demo: "", report: "" },
  },
  {
    title: "Agent-Trace",
    categories: ["evaluations"],
    description: "Investigating how safety-relevant information changes when agent activity is reconstructed from incomplete traces rather than observed through native tool events.",
    tags: ["Agent Traces", "Observability", "Evaluation"],
    links: { github: "", paper: "", demo: "", report: "" },
  },
  {
    title: "World Models in Physical AI",
    categories: ["evaluations"],
    description: "Evaluating whether generated world models preserve decision-relevant structure using planning, reachability, reversibility, controlled perturbations, trace equivalence, and planning-regret transfer.",
    tags: ["World Models", "Evaluation", "Planning"],
    links: { github: "", paper: "", demo: "", report: "" },
  },
  {
    title: "Latent Manifold Reasoning Sandbox",
    categories: ["evaluations"],
    description: "An experimental sandbox studying how reasoning-related representations behave under structured routing operations compared with isotropic perturbations, using geometric measures such as neighbourhood overlap, path distortion, and angular change.",
    tags: ["Representation Geometry", "Manifolds", "Reasoning", "Interpretability"],
    links: { github: "", paper: "", demo: "", report: "" },
  },
  {
    title: "SnapInspect AI",
    categories: ["evaluations", "vision"],
    description: "A multi-device edge AI evaluation project focused on measuring practical deployment behaviour across devices, including latency, throughput/FPS, CPU usage, and memory consumption.",
    tags: ["Edge AI", "Benchmarking", "Evaluation", "Computer Vision"],
    links: { github: "", paper: "", demo: "", report: "" },
  },
  {
    title: "Fog-Assisted UAV Routing / Split Inference",
    categories: ["rl"],
    context: "DREAM Lab, IISc",
    description: "Research on resource-constrained autonomous systems involving fog-assisted UAV routing and reinforcement-learning-based split inference.",
    tags: ["Reinforcement Learning", "UAV", "Edge Computing", "Split Inference"],
    links: { github: "", paper: "", demo: "", report: "" },
  },
];

const projectCategories = [
  { id: "safety", number: "01", title: "AI Safety, Control & Monitoring" },
  { id: "evaluations", number: "02", title: "Evaluations & Benchmarking" },
  { id: "vision", number: "03", title: "Computer Vision & Edge AI" },
  { id: "rl", number: "04", title: "Reinforcement Learning & Autonomous Systems" },
  // TODO: Add Gagana's hyperspectral unmixing project(s) before enabling this category.
  { id: "hyperspectral", number: "05", title: "Hyperspectral Imaging & Representation Learning" },
];

const writingEntries = [
  {
    title: "AI Safety & Mechanistic Interpretability",
    description: "An introduction to why evaluating increasingly agentic AI systems requires looking beyond task performance, and how mechanistic interpretability can help move from blind trust toward a better understanding of model behaviour.",
    platform: "WiBD India Insights / LinkedIn · Gagana M D’s contribution in the July edition",
    date: "July 2026",
    url: "https://www.linkedin.com/pulse/wibd-insights-july-2026-edition-women-in-big-data-india-qd8yc/",
    tags: ["AI Safety", "Interpretability", "Evaluation"],
  },
  // TODO: Add Gagana's additional article: { title, description, platform, date, url, tags }
  // TODO: Add X articles / long-form posts: { title, description, platform: "X", date, url, tags }
];

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

function appendLinks(container, links, labels) {
  Object.entries(links).forEach(([key, url]) => {
    if (!url) return;
    const link = document.createElement("a");
    link.href = url;
    link.target = "_blank";
    link.rel = "noreferrer";
    link.innerHTML = `${labels[key]} <span aria-hidden="true">↗</span>`;
    container.append(link);
  });
}

const archiveContainer = document.querySelector(".project-archive");
const categoryNav = document.querySelector(".category-nav");
let activeCategory = "all";

function renderProjectArchive() {
  archiveContainer.innerHTML = "";
  projectCategories.forEach((category) => {
    const projects = projectArchive.filter((project) => project.categories.includes(category.id) && (activeCategory === "all" || activeCategory === category.id));
    if (!projects.length) return;
    const group = document.createElement("section");
    group.className = "archive-group";
    group.innerHTML = `<div class="archive-heading"><p>${category.number}</p><h3>${category.title}</h3></div>`;
    projects.forEach((project) => {
      const item = document.createElement("article");
      item.className = "archive-project";
      item.innerHTML = `${project.context ? `<p class="archive-context">${project.context}</p>` : ""}<h4>${project.title}</h4><p>${project.description}</p><ul class="tags" aria-label="Topics">${project.tags.map((tag) => `<li>${tag}</li>`).join("")}</ul><div class="project-links"></div>`;
      appendLinks(item.querySelector(".project-links"), project.links, { github: "GitHub", paper: "Paper", demo: "Demo", report: "Report" });
      group.append(item);
    });
    archiveContainer.append(group);
  });
}

projectCategories.filter((category) => projectArchive.some((project) => project.categories.includes(category.id))).forEach((category) => {
  const button = document.createElement("button");
  button.type = "button";
  button.dataset.category = category.id;
  button.textContent = `${category.number} ${category.title}`;
  categoryNav.append(button);
});

categoryNav.addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) return;
  activeCategory = button.dataset.category;
  categoryNav.querySelectorAll("button").forEach((item) => item.classList.toggle("is-active", item === button));
  renderProjectArchive();
});

if (categoryNav.firstElementChild) categoryNav.firstElementChild.classList.add("is-active");
renderProjectArchive();

const writingContainer = document.querySelector(".writing-list");
writingEntries.forEach((entry) => {
  const item = document.createElement("article");
  item.className = "writing-entry";
  item.innerHTML = `<p class="writing-meta">${entry.platform} · ${entry.date}</p><h3>${entry.title}</h3><p>${entry.description}</p><ul class="tags" aria-label="Topics">${entry.tags.map((tag) => `<li>${tag}</li>`).join("")}</ul><div class="project-links"></div>`;
  appendLinks(item.querySelector(".project-links"), { article: entry.url }, { article: "Article" });
  writingContainer.append(item);
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

import pathlib
from build import contact, EMAIL

P = pathlib.Path(__file__).parent / "pages"
r = lambda n: (P / n).read_text(encoding="utf-8")

PERSON = {
    "@context": "https://schema.org", "@type": "Person", "name": "Gagana M D",
    "url": "https://gaganamd.github.io/", "image": "https://gaganamd.github.io/assets/img/gagana-md.jpg", "email": f"mailto:{EMAIL}",
    "jobTitle": "AI safety researcher",
    "knowsAbout": ["AI safety", "AI control", "Agent monitoring", "AI evaluations", "Reinforcement learning", "Post-AGI governance", "Multi-agent safety", "Mechanistic interpretability"],
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "Acharya Institute of Technology"},
    "sameAs": ["https://github.com/GaganaMD", "https://www.linkedin.com/in/gaganamd/", "https://orcid.org/0009-0003-2594-1026"],
}

# ---- News (homepage) -------------------------------------------------------
# Edit _content/news.yml: one entry per item, with date "YYYY-MM" or "YYYY-MM-DD" and one line of Markdown text.
# Newest first is applied automatically (an exact day sorts above a bare month); the first NEWS_VISIBLE items show, the rest
# go under "Older news".
import datetime
from render import load_yaml, inline_md
NEWS_VISIBLE = 5

def news_html():
    items = [dict(date=str(x["date"]), text=inline_md(x["text"])) for x in load_yaml("news.yml")]
    items = sorted(items, key=lambda x: x["date"], reverse=True)  # stable: same-month order kept
    def li(x):
        d = datetime.date(int(x["date"][:4]), int(x["date"][5:7]), 1)
        return f'<li><time datetime="{x["date"]}">{d:%b %Y}</time><span>{x["text"]}</span></li>'
    first, rest = items[:NEWS_VISIBLE], items[NEWS_VISIBLE:]
    out = '<ul class="ac-news">' + "".join(li(x) for x in first) + "</ul>"
    if rest:
        out += ('\n  <details class="ac-older"><summary>Older news</summary><ul class="ac-news">'
                + "".join(li(x) for x in rest) + "</ul></details>")
    return out

home = lambda: r("index.html").replace("@@NEWS@@", news_html())

PAGES = [
    dict(fname="index.html",
         title="Gagana M D · AI safety research: agent monitoring and evaluations",
         desc="Gagana M D is an early-career AI safety researcher working on monitoring and evaluating AI agents. Publications, reports and code for each completed project.",
         body=home() + contact(body="Email is the easiest way to reach me. I'm always glad to hear from people working on similar questions, and from people just starting out in AI safety."), jsonld=PERSON),
    dict(fname="research.html", title="Research · Gagana M D",
         desc="AI safety research by Gagana M D on agent monitoring, AI control, world-model evaluation and auditing under limited observability, with the status of each project.",
         body=r("research.html") + contact()),
    dict(fname="detection-is-not-containment.html", title="Detection Is Not Containment · Gagana M D",
         desc="Case study: measuring whether an AI monitor detects a prohibited action early enough to prevent it, and what false alarms cost, in a synthetic authorization environment.",
         body=r("detection-is-not-containment.html") + contact(), og_type="article"),
    dict(fname="projects.html", title="Projects · Gagana M D",
         desc="Projects and code by Gagana M D now live on the research page.",
         extra_head='\n<meta http-equiv="refresh" content="0; url=research.html#code">\n<meta name="robots" content="noindex">',
         body='<section class="page-hero wrap"><p class="eyebrow">Projects</p><h1 id="page-title">Projects have moved.</h1>'
              '<p class="lede">All projects and code are now on the <a href="research.html#code">research page</a>.</p></section>'),
    dict(fname="writing.html", title="Writing · Gagana M D",
         desc="Research write-ups and articles by Gagana M D on AI monitoring, evaluation and interpretability.",
         body=r("writing.html") + contact()),
    dict(fname="about.html", title="About · Gagana M D",
         desc="Background, experience, education and community work of Gagana M D, an early-career AI safety researcher.",
         body=r("about.html") + contact()),
    dict(fname="speaking.html", title="Speaking · Gagana M D",
         desc="Talks, workshops and community programs by Gagana M D on AI safety, evaluations, research careers and technical portfolios.",
         body=r("speaking.html") + contact(eyebrow="Speaking inquiries",
             title="Planning a session?",
             body="If you're putting together a talk, workshop or panel on AI safety, evaluations or getting into research, I'd be glad to hear about it.",
             links=[(f"mailto:{EMAIL}?subject=Speaking%20or%20workshop%20inquiry", "Let's connect")]),
         scripts=("script.js", "speaking.js")),
    dict(fname="consulting.html", title="Consulting · Gagana M D",
         desc="Scoped technical reviews of AI agent evaluations, benchmarks and monitoring by Gagana M D.",
         body=r("consulting.html") + contact(eyebrow="Project inquiries",
             title="Discuss a project",
             body="Send a short description of what you're evaluating and the decision it feeds into. I'll tell you honestly whether I'm a good fit.",
             links=[(f"mailto:{EMAIL}?subject=Evaluation%20project", "Discuss a project")])),
    dict(fname="404.html", title="Page not found · Gagana M D",
         desc="This page doesn't exist.", extra_head='\n<base href="/">\n<meta name="robots" content="noindex">',
         body='<section class="page-hero wrap"><p class="eyebrow">404</p><h1 id="page-title">That page isn\'t here.</h1>'
              '<p class="lede">The site was reorganized in October 2026. Try the <a href="index.html">home page</a>, '
              '<a href="research.html">research</a> or <a href="writing.html">writing</a>.</p></section>'),
]

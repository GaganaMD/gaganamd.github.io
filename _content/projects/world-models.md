---
# Research project. Field guide: _content/projects/README.md
id: world-models
section: main
order: 3
tag: World models · Evaluation
title: Do LLM-generated world models keep their structure?
role: <strong>My part:</strong> I implemented the evaluation pipeline, the world-model analysis library (graph analysis and structural comparison) and the test suite. Teammates built the JSON-generation tooling, the cultural-track evaluation and the reports, and contributed scenario data and prompts.
details:
  summary: Method, results and limits
  facts:
  - dt: Method
    dd: 'A 44-scenario benchmark across toy, situational, game and cultural settings. Five LLMs, three generations per model and scenario. Three evaluation lanes: mechanical validity, permutation-invariant structural matching against reference games, and qualitative coverage. Every run keeps its prompts, raw replies, generated code and validation reports.'
  - dt: Result
    dd: '410 first-pass generations across three tracks. In the game track, 134 of 135 passed a strict mechanical check, but the mean permutation-invariant structural F1 was 0.366 (median 0.18), with 28 of 134 exact matches. Repeated generations varied (within-pair SD 0.17). In the cultural track, naming the country in a norm-conflict prompt changed the generated structure for four of five models, while automated semantic scores barely moved. Executability is necessary but not sufficient: a model that runs can still hand downstream planning and neuro-symbolic reasoning the wrong structure.'
  - dt: Limits
    dd: Reference structures exist only for the nine games. The link between a game's stochasticity and lower agreement (ρ = −0.68) is exploratory, from nine games.
side:
- status: Accepted · NeurIPS 2026 NEmo workshop (poster)
  class: done
- text: 'PRISM AI Safety Research Fellowship project, May – Oct 2026 (completed). Mentored by Jobst Heitzig. My role: technical research contributor.'
- text: 'Paper: <em>Evaluating LLM-Generated World Models for Neuro-Symbolic Reasoning</em>.'
- text: S. Djaffal, A. Jamal, G. Madhugiri Devaraja, A. Pal, J. Heitzig.
- links:
  - label: arXiv preprint ↗
    url: https://arxiv.org/abs/2611.14419
  - label: NEmo listing ↗
    url: https://nemo.semantic.review/#accepted-papers
- text: Code release pending.
---
<p>If an LLM writes the environment an agent is tested in, and the environment quietly changes which states are reachable or which actions exist, any safety conclusion drawn inside it inherits that error. We tested whether LLMs can build multi-agent situations as executable partially observable stochastic games (POSGs).</p>

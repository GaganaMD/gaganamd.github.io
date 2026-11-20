---
# Research project. Field guide: _content/projects/README.md
id: interp-causal
section: earlier
order: 5
tag: Interpretability · Causal reasoning
title: Prompt sensitivity and latent drift in causal reasoning
role: <strong>My part:</strong> independent project, built to experiment with causal interpretation. Every run saves its config and a run manifest.
side:
- status: Exploratory · independent
  class: ongoing
- links:
  - label: Code ↗
    url: https://github.com/GaganaMD/Interpretability-for-Scientific-Causal-Reasoning
  - label: Limitations ↗
    url: https://github.com/GaganaMD/Interpretability-for-Scientific-Causal-Reasoning/blob/main/docs/limitations.md
---
<p>If you reword a causal-reasoning question but keep its causal structure, does a small model's answer flip, and do the flips line up with movement in its hidden states? I built synthetic vignettes covering confounding, mediation and selection bias, with variants that remove a confounder or rename terms. On Qwen2.5-0.5B-Instruct I ran prompt-stability analysis, layerwise probes and activation contrasts. Early runs showed high answer flip rates across reframings, with the largest drift under "mechanistic" prompts. Probe separability and drift are correlational, and the repository says so.</p>

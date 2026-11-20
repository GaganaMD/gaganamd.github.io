---
# Research project. Field guide: _content/projects/README.md
id: latent-manifold
section: earlier
order: 4
tag: Representations · Geometry
title: 'Latent manifold reasoning: when does a reasoning trajectory collapse?'
role: <strong>My part:</strong> independent project. All eight versions are kept, so the method changes are visible.
side:
- status: Exploratory · independent
  class: done
- links:
  - label: Code ↗
    url: https://github.com/GaganaMD/latent-manifold-reasoning
---
<p>Think of reasoning as a smooth path through a latent manifold. Forcing that path through a narrow, discrete interface (text, a tool call, a serialised state) can make it <em>collapse</em>: neighbouring states stop being neighbours, and the path takes detours the original never did. I built a sandbox to make that idea measurable. It routes trajectories through PCA embeddings of the scikit-learn digits data under a bottleneck of increasing strength, and tracks path distortion, k-nearest-neighbour preservation and excess path length.</p>
<p>Early versions had no baselines, and almost any perturbation looked like collapse. Later versions compare structured routing against isotropic noise and shuffled anchors, with bootstrap intervals and permutation tests. The result that held up: structured routing collapses local neighbourhood structure far more than noise does, <em>while</em> shortening the path. One geometric metric can look better while the trajectory becomes less faithful. This is a toy setting, not evidence about transformer hidden states.</p>

---
# Research project. Field guide: _content/projects/README.md
id: biornet
section: earlier
order: 1
tag: Signal processing · Deep learning
title: 'Hyperspectral BiorNet: a complete wavelet framework for unmixing'
role: <strong>My part:</strong> first author. I worked on the wavelet framework and the design of the activation function, and built the implementation.
side:
- status: Published · IEEE InGARSS 2025
  class: done
- links:
  - label: Paper ↗
    url: https://doi.org/10.1109/InGARSS67683.2025.11584022
  - label: Code ↗
    url: https://github.com/GaganaMD/Hyperspectral-Wavenet
---
<p>Each pixel of a hyperspectral image mixes the spectra of several materials. Unmixing recovers the pure spectra (endmembers) and their proportions (abundances), under the linear mixing model <span class="math">x ≈ E a</span>, with <span class="math">a ≥ 0</span> and <span class="math">Σa = 1</span>. The problem is ill-posed: there are more unknowns than observations, and noise and spectral variability blur the signatures.</p>
<p>BiorNet does the whole thing in the wavelet domain. A biorthogonal discrete wavelet transform splits each pixel's spectrum into approximation and detail coefficients, and the endmembers and abundances are learned from those. The network's nonlinearity is a wavelet as well: a custom biorthogonal-inspired activation,</p>
<p class="formula">φ(x) = max(0, x) · sin(5x) · e<sup>−x²/2</sup></p>
<p>This is a Gaussian-windowed oscillation, so the activation has the same localised, oscillatory shape as the basis the data is expressed in. A ReLU can't respond that way. We evaluated it on synthetic data and the HYDICE Urban benchmark against state-of-the-art unmixing models, using RMSE, spectral angle distance and spectral information divergence.</p>

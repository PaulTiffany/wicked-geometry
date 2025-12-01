# The Wicked Prior as a Bounded-Observer Manifold

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A geometric framework for analyzing how institutional authorities misclassify corrective signals as adversarial noise.**

This repository contains the formal proofs, validation code, and research artifacts corresponding to the paper:

> **The Wicked Prior as a Bounded-Observer Manifold: Atlas Fracture, Stackelberg Parentage, and Grace-Flow Repair**  
> Paul Tiffany (2025)

## Abstract

We formalize the *Wicked* Prior as an instantiation of bounded symbolic geometry under dual-horizon constraints. Oz is modeled as a bounded symbolic manifold $\mathcal{M}$ equipped with:

- An **outer projection metric** $g_{\mathrm{out}}$ (social legibility, institutional categories)
- An **inner emergence metric** $g_{\mathrm{in}}$ (truth-seeking, lived experience)

**Part I** exhibits resolution collapse $\varepsilon_{\mathrm{res}} \to 0$ that concentrates curvature and produces **atlas fracture** at the narrative climax - a measurable discontinuity where the outer chart fails to map the inner territory.

**Part II** repairs the manifold via a Ricci-type **grace flow** $\phi(\tau)$ with adaptive cadence, enabling reconciliation while preserving identity.

## Key Contributions

### 1. Atlas Fracture Detection
We demonstrate that the unmasking of the Wizard (Chapter 15 in Baum's 1900 text) constitutes a measurable discontinuity in semantic entropy - an **atlas fracture** where institutional maps fail.

![Atlas Fracture Plot](./atlas_fracture_evidence.png)

### 2. Stackelberg Parentage Paradox
A game-theoretic formalization showing how a leader (the Wizard) misclassifies their own generated corrective (Elphaba) as adversarial noise. The paradox resolves only when the leader admits generative parentage: $\pi_L \Rightarrow E \Rightarrow \pi_F$.

### 3. Grace-Flow Repair
A geometric repair process modeled as:

$$\frac{\partial g}{\partial \tau} = \phi(\tau)\big[\mathrm{Ric}^\perp(g(\tau)) + \nabla\nabla \varepsilon_{\mathrm{res}}(\tau)\big]$$

This transforms rigid categories into a shared basin of attraction (Goodness as a Lyapunov basin).

### 4. Falsifiable Predictions
Six testable predictions (P1-P6) across narrative, AI, and economic domains:

- **P1**: Dominant curvature peak aligns with climactic unmasking
- **P2**: Animal-identity concepts show connection annihilation
- **P3**: Grace flow exhibits gradual curvature dissipation
- **P4**: Reconciliation requires coupling-dependent convergence
- **P5**: Captured regulation increases concentration measures
- **P6**: True risk reduction decouples from innovation suppression

## Validation Protocol V-Baum

To empirically validate the geometric thesis, we apply `oz_fracture.py` to the original 1900 Baum text.

**Hypothesis**: The unmasking of the Wizard (Chapter 15) constitutes a measurable discontinuity in semantic entropy.

**Method**: Compute embedding curvature $\|\mathrm{Ric}\|$ over the narrative arc using sliding-window embeddings.

**Result**: The model detects semantic volatility consistent with atlas fracture at the precise narrative moment the curtain falls.

## Installation & Usage

```bash
git clone https://github.com/PaulTiffany/wicked-geometry.git
cd wicked-geometry
pip install -r requirements.txt
python oz_fracture.py
```

This will:
1. Fetch *The Wonderful Wizard of Oz* from Project Gutenberg
2. Generate sliding-window embeddings using sentence-transformers
3. Compute discrete curvature via cosine distance
4. Output `atlas_fracture_evidence.png` showing semantic entropy over the narrative arc

## Repository Structure

```
.
- main.tex             # Full paper (LaTeX)
- oz_fracture.py       # V-Baum validation protocol
- requirements.txt     # Python dependencies
- index.html           # GitHub Pages landing page
- CITATION.cff         # Citation metadata
- LICENSE              # MIT License
- README.md            # This file
```

## Core Theoretical Definitions

### Atlas Fracture
A failure to transition smoothly between inner and outer horizons ($g_{\mathrm{in}}$ and $g_{\mathrm{out}}$) at bounded resolution. Mathematically, this manifests as a blow-up in extrinsic curvature where the institutional map can no longer represent the emergent territory.

### Stackelberg Parentage Paradox
A game-theoretic condition where a "Leader" (the Wizard) misclassifies their own generated corrective (Elphaba) as adversarial noise. Resolution requires admitting generative parentage.

### Grace Flow $\phi(\tau)$
A geometric repair process that restores the manifold via a Ricci-type flow with adaptive cadence, allowing reconciliation by transforming rigid categories into a shared basin of attraction.

### Resolution Floor $\varepsilon_{\mathrm{res}}$
The observer's representational bandwidth constraint. As $\varepsilon_{\mathrm{res}} \to 0$, identities are forced into low-dimensional categories, producing geometric stress and curvature concentration.

## Applications

### AI Alignment
- **Resolution floors as spectral minima**: Prevent catastrophic forgetting by imposing minimum singular values
- **Grace scheduling**: Time-varying multi-loss flows for capability/safety tradeoffs
- **Connection preservation**: Monitor and penalize transport failure between concept embeddings

### Economic & Regulatory
- **Regulatory capture detection**: Measure concentration shifts and innovation suppression under policy changes
- **First-mover misalignment**: Identify when stated objectives ($J_{\mathrm{pub}}$) diverge from realized dynamics ($J_{\mathrm{priv}}$)

### Narrative Analysis
- **Cross-narrative validation**: Test geometric quality metrics on culturally resonant story corpora
- **Predictive frameworks**: Use curvature profiles to predict narrative climaxes

## Falsification Criteria

Each prediction comes with explicit falsification conditions:

- **P1 fails** if curvature peaks drift >2 scenes from the climax across embedding models
- **P2 fails** if Animal concepts maintain full transport connectivity
- **P3 fails** if repair occurs as discontinuous jumps rather than gradual flows
- **P4 fails** if convergence is independent of coupling strength
- **P5 fails** if concentration doesn't increase under captured regulation
- **P6 fails** if innovation suppression correlates with genuine risk reduction

## Citation

If you use this framework or code, please cite:

```bibtex
@article{tiffany2025wicked,
  title={The Wicked Prior as a Bounded-Observer Manifold: Atlas Fracture, Stackelberg Parentage, and Grace-Flow Repair},
  author={Tiffany, Paul},
  year={2025},
  month={11},
  url={https://paultiffany.github.io/wicked-geometry/}
}
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Related Work

This research is part of the broader **Compitum** research program exploring bounded observer manifolds and institutional geometry.

See more at [compitum.space](https://compitum.space)

## Contact

For questions, collaboration, or feedback:
- **GitHub Issues**: [github.com/PaulTiffany/wicked-geometry/issues](https://github.com/PaulTiffany/wicked-geometry/issues)
- **Website**: [compitum.space](https://compitum.space)

# V-Baum Validation: Empirical Test of Dual-Horizon Theory

## Claim
Removing an institutional optical filter produces a measurable semantic discontinuity (atlas fracture) in narrative embedding space.

## Method
- Corpus: L. Frank Baum, *The Wonderful Wizard of Oz* (Project Gutenberg epub/55), 212,653 characters.
- Embedding: sentence-transformers/all-MiniLM-L6-v2.
- Window: 1000-character windows, 200-character stride.
- Curvature: cosine distance between successive window embeddings.
- Peak detection: prominence threshold ≥ 2.0 (standardized).

## Result
- Dominant peak at Chapter 19 (“Attacked by the Fighting Trees”), where Emerald City spectacles are removed.
- Window index: 909; prominence: 0.1993; curvature: 0.2472.
- Interpretation: matches predicted `ε_res -> 0` event; supports atlas fracture at filter removal.

## Falsification
- Prediction fails if dominant peak drifts >2 scenes from the unmasking/filter-removal moment or if peaks are unstable across embedding models.

## Replication
- Code: `oz_fracture.py` (runtime <5 minutes on a laptop with internet for text fetch).
- Outputs: `atlas_fracture_evidence.png`, `vbaum_analysis_report.txt`.

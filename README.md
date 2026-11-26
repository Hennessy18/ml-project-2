# Clustering States by Rural Health-Infrastructure Shortfall

**Student:** Uddey Kanojia | **Roll No.:** 24020570044  
**Serial No.:** 39 | **Problem No.:** 12 | **Group:** 12  
**Domain:** Health / Infrastructure

A case study of State/UT rural health infrastructure and staffing shortfall using official Government of India data. The repository structure follows the friend's `ML-Project` repository (data / report / results / src) but the analysis and dataset are specific to this assigned problem.

## Data source and reference period
- data.gov.in catalogue: https://www.data.gov.in/catalog/rural-health-statistics-2019
- Ministry of Health and Family Welfare, *Rural Health Statistics 2018–19*: https://www.mohfw.gov.in/sites/default/files/Final%20RHS%202018-19_0.pdf
- Reference period: rural health data up to 31 March 2019; population requirement estimate as of 1 July 2019.

The CSV contains State/UT-wise SC, PHC and CHC facility shortfall percentages and derived staffing shortfall percentages for allopathic doctors at rural PHCs and specialists at rural CHCs. It is not synthetic data. `*` surplus is treated as 0 shortfall. Not-applicable / zero denominator values are missing and excluded from clustering.

## Setup
Python 3.10 or later is recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python src/run_analysis.py
```

## Generated outputs
The script creates:
- `results/state_cluster_assignments.csv`
- `results/cluster_profiles.csv`
- `results/k_selection_metrics.csv`
- `results/state_shortfall_ranking.csv`
- `results/analysis_summary.json`
- `results/pca_cluster_plot.png`
- `results/state_shortfall_ranking.png`
- `results/hierarchical_dendrogram.png`
- `report/journal_report.md` (generated with executed metrics and cluster memberships)

## Methods
Five percentage indicators are standardised. K-means uses K=3 and random seed 42. The script also evaluates silhouette/inertia for K=2–6 and compares the K=3 K-means result with Ward hierarchical clustering using silhouette and Davies–Bouldin metrics. PCA is used for visualisation, not as the clustering input.

## Important
Cluster labels are descriptive and not official government categories. This is a historical State/UT-level case study, not a current 2026 assessment or causal policy evaluation. Verify all transcribed data against the official source before submission.


from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, dendrogram

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "rural_health_shortfall_2019.csv"
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

FEATURES = [
    "SC_shortfall_pct", "PHC_shortfall_pct", "CHC_shortfall_pct",
    "PHC_doctors_shortfall_pct", "CHC_specialists_shortfall_pct"
]

def main():
    raw = pd.read_csv(DATA)
    clean = raw.dropna(subset=FEATURES).copy()
    X = clean[FEATURES].astype(float)
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    # Silhouette sweep documents the K choice; K=3 is retained for
    # interpretable low/moderate/high profiles and matches the assigned report draft.
    sweep = []
    for k in range(2, min(7, len(clean))):
        km = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = km.fit_predict(Xs)
        sweep.append({"k": k, "silhouette": float(silhouette_score(Xs, labels)),
                     "inertia": float(km.inertia_)})
    pd.DataFrame(sweep).to_csv(OUT / "k_selection_metrics.csv", index=False)

    k = 3
    km = KMeans(n_clusters=k, random_state=42, n_init=20)
    klabels = km.fit_predict(Xs)
    clean["KMeans_cluster_id"] = klabels

    # Relabel clusters by average standardized/actual shortfall across features.
    means = clean.groupby("KMeans_cluster_id")[FEATURES].mean()
    rank = means.mean(axis=1).sort_values().index.tolist()
    label_map = {cluster_id: ["Low shortfall", "Moderate shortfall", "High shortfall"][i]
                 for i, cluster_id in enumerate(rank)}
    clean["KMeans_cluster"] = clean["KMeans_cluster_id"].map(label_map)

    # Hierarchical clustering (Ward linkage, Euclidean distance).
    hmodel = AgglomerativeClustering(n_clusters=k, linkage="ward")
    hlabels = hmodel.fit_predict(Xs)
    clean["Hierarchical_cluster_id"] = hlabels
    hmeans = clean.groupby("Hierarchical_cluster_id")[FEATURES].mean()
    hrank = hmeans.mean(axis=1).sort_values().index.tolist()
    hmap = {cluster_id: ["Low shortfall", "Moderate shortfall", "High shortfall"][i]
            for i, cluster_id in enumerate(hrank)}
    clean["Hierarchical_cluster"] = clean["Hierarchical_cluster_id"].map(hmap)
    clean.to_csv(OUT / "state_cluster_assignments.csv", index=False)

    # Cluster profiles.
    profile = clean.groupby("KMeans_cluster")[FEATURES].mean().round(2)
    profile["State_UT_count"] = clean.groupby("KMeans_cluster")["State_UT"].count()
    profile.to_csv(OUT / "cluster_profiles.csv")

    metrics = {
        "dataset_rows": int(len(raw)),
        "rows_used_for_clustering": int(len(clean)),
        "excluded_incomplete_rows": int(len(raw) - len(clean)),
        "feature_count": len(FEATURES),
        "kmeans_k": k,
        "kmeans_silhouette": float(silhouette_score(Xs, klabels)),
        "kmeans_davies_bouldin": float(davies_bouldin_score(Xs, klabels)),
        "hierarchical_k": k,
        "hierarchical_silhouette": float(silhouette_score(Xs, hlabels)),
        "hierarchical_davies_bouldin": float(davies_bouldin_score(Xs, hlabels)),
        "cluster_counts": clean["KMeans_cluster"].value_counts().to_dict(),
        "feature_names": FEATURES,
        "note": "Cluster IDs are arbitrary; names assigned by ascending mean feature shortfall."
    }
    (OUT / "analysis_summary.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    # PCA biplot-style scatter (scores only; labels show state names).
    pca = PCA(n_components=2, random_state=42)
    pcs = pca.fit_transform(Xs)
    clean["PC1"], clean["PC2"] = pcs[:, 0], pcs[:, 1]
    plt.figure(figsize=(10, 7))
    for label, group in clean.groupby("KMeans_cluster"):
        plt.scatter(group["PC1"], group["PC2"], label=label, s=60)
        for _, row in group.iterrows():
            plt.annotate(row["State_UT"], (row["PC1"], row["PC2"]), fontsize=7, alpha=.8)
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)")
    plt.title("PCA view of rural health-infrastructure shortfall clusters")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "pca_cluster_plot.png", dpi=220)
    plt.close()

    # State ranking by simple mean across the five standardized input indicators.
    ranking = clean[["State_UT"] + FEATURES].copy()
    ranking["Mean_shortfall_index_pct"] = ranking[FEATURES].mean(axis=1)
    ranking = ranking.sort_values("Mean_shortfall_index_pct", ascending=False)
    ranking.to_csv(OUT / "state_shortfall_ranking.csv", index=False)
    plt.figure(figsize=(10, 10))
    plt.barh(ranking["State_UT"], ranking["Mean_shortfall_index_pct"])
    plt.gca().invert_yaxis()
    plt.xlabel("Mean of five shortfall indicators (%)")
    plt.title("State/UT shortfall indicator ranking (descriptive index)")
    plt.tight_layout()
    plt.savefig(OUT / "state_shortfall_ranking.png", dpi=220)
    plt.close()

    # Dendrogram for hierarchical method.
    Z = linkage(Xs, method="ward")
    plt.figure(figsize=(13, 7))
    dendrogram(Z, labels=clean["State_UT"].tolist(), leaf_rotation=90, leaf_font_size=7)
    plt.title("Ward hierarchical clustering dendrogram")
    plt.ylabel("Ward linkage distance")
    plt.tight_layout()
    plt.savefig(OUT / "hierarchical_dendrogram.png", dpi=220)
    plt.close()

    # Generated journal draft populated from the executed outputs.
    counts = clean["KMeans_cluster"].value_counts().to_dict()
    report = f"""# Clustering States by Rural Health-Infrastructure Shortfall
## Case study: State/UT profiles using Rural Health Statistics 2018–19

**Student:** Uddey Kanojia  
**University Roll No.:** 24020570044  
**Assignment No.:** 39 (serial no. in allocation sheet)  
**Problem No.:** 12  
**Group:** 12  
**Domain:** Health / Infrastructure  
**Article type:** Case Study — policy-oriented descriptive analysis

### Abstract
This case study examines differences in rural health infrastructure and health-worker shortfall across Indian States and Union Territories using the Government of India’s Rural Health Statistics 2018–19, with data reported up to 31 March 2019 and rural population estimates for 1 July 2019. Five indicators were used: SC, PHC and CHC facility shortfall percentages; allopathic doctor shortfall percentage at rural PHCs; and specialist-doctor shortfall percentage at rural CHCs. K-means clustering (K=3) and Ward hierarchical clustering were applied after standardisation. The executed analysis used {len(clean)} complete State/UT records from {len(raw)} source rows. K-means silhouette score was {metrics['kmeans_silhouette']:.3f}; hierarchical silhouette score was {metrics['hierarchical_silhouette']:.3f}. Clusters are descriptive profiles, not official classifications or causal findings.

**Keywords:** rural health infrastructure; health-worker shortfall; K-means; hierarchical clustering; PCA; India; SDG 3; SDG 10

## 1. Introduction
Rural health systems rely on Sub-Centres (SCs), Primary Health Centres (PHCs) and Community Health Centres (CHCs), each serving different levels of care. Uneven facility and staffing shortfalls can limit access to preventive, primary and referral services. A multi-indicator comparison is therefore more informative than considering a single facility count.

## 2. Objectives
1. Compile State/UT-wise infrastructure and staffing shortfall indicators from official public data.
2. Standardise the indicators and apply K-means clustering.
3. Compare K-means with Ward hierarchical clustering.
4. Use silhouette score and cluster profiles to assess and interpret the groupings.
5. Identify relative shortfall profiles and discuss planning implications and limitations.

## 3. Dataset and variables
The primary source is the Ministry of Health and Family Welfare, *Rural Health Statistics 2018–19*. Table 8 reports rural SC, PHC and CHC shortfall percentages. Table 19 reports allopathic doctors at rural PHCs, and Table 28 reports total specialists at rural CHCs. The report states that information was provided by States/UTs and is current to 31 March 2019.

### 3.1 Features
- SC shortfall (%)
- PHC shortfall (%)
- CHC shortfall (%)
- PHC allopathic doctor shortfall (% of required posts)
- CHC specialist shortfall (% of required posts)

For staffing indicators, percentage shortfall was derived as `100 × shortfall count / required posts`. A source-reported surplus (`*`) was coded as zero shortfall. Not-applicable or zero-denominator values were retained as missing and excluded from the complete-case clustering; no missing feature was invented.

## 4. Methodology
The workflow was: official source table → data transcription and validation → cleaning → percentage derivation for staffing → standardisation → K-means and hierarchical clustering → silhouette evaluation → cluster profiles and PCA visualisation.

All five features were standardised using z-scores. K-means was fitted with K=3 and random seed 42. The K value is used for three interpretable shortfall bands; the script also records silhouette and inertia for K=2 through K=6. Ward hierarchical clustering was fitted to the same standardised features with three clusters. Software cluster numbers are arbitrary, so labels were assigned in ascending order of the average feature shortfall.

## 5. Results and analysis
The executed script retained **{len(clean)}** complete State/UT records and excluded **{len(raw)-len(clean)}** incomplete records. The K-means silhouette score was **{metrics['kmeans_silhouette']:.3f}** and Davies–Bouldin index was **{metrics['kmeans_davies_bouldin']:.3f}**. The hierarchical silhouette score was **{metrics['hierarchical_silhouette']:.3f}** and Davies–Bouldin index was **{metrics['hierarchical_davies_bouldin']:.3f}**.

### 5.1 K-means cluster membership
{chr(10).join('- **'+str(name)+'** ('+str(count)+' States/UTs): '+', '.join(clean.loc[clean['KMeans_cluster']==name,'State_UT'].tolist()) for name,count in counts.items())}

### 5.2 Cluster profiles
See `results/cluster_profiles.csv` for the mean of each input indicator by cluster. The cluster names describe relative averages across the five indicators and should not be interpreted as government classifications.

### 5.3 Visual analysis
- `results/pca_cluster_plot.png` presents a two-component PCA projection of the standardised features.
- `results/hierarchical_dendrogram.png` presents the Ward linkage structure.
- `results/state_shortfall_ranking.png` presents a simple equal-weight mean across the five indicators; it is a descriptive index only.

## 6. Discussion
The clustering is useful for summarising States/UTs with similar combinations of facility and staffing gaps. A high cluster mean can indicate multiple dimensions of shortfall, while a state may have a comparatively low facility gap but a high specialist staffing gap. The cluster profiles should therefore be read feature by feature rather than as a single definitive ranking.

## 7. Conclusion
This case study demonstrates a reproducible unsupervised-learning workflow using official, historical rural health statistics. K-means and hierarchical clustering produce relative State/UT shortfall profiles that may help communicate infrastructure and staffing disparities. The analysis does not establish causes, measure healthcare quality or predict future shortages.

## 8. Future scope
- Extend the analysis to district-level data to reveal within-State disparities.
- Add nurses, ANMs, pharmacists, laboratory technicians and other staffing indicators from the same publication.
- Compare multiple Rural Health Statistics editions to study changes over time.
- Test alternative values of K, clustering methods and feature weights.
- Build a Power BI or Python dashboard for filtering by facility and staffing indicator.

## 9. Limitations
The data are historical (2019 reference period), State/UT aggregates hide local variation, and shortfall counts do not measure service quality, medicines, travel time or utilisation. Surplus is treated as zero shortfall. K-means is sensitive to scaling and K; the three-cluster solution is selected for interpretability. Clusters are descriptive and should not be used as standalone policy decisions.

## Data availability
Source catalogue: https://www.data.gov.in/catalog/rural-health-statistics-2019  
Official report: https://www.mohfw.gov.in/sites/default/files/Final%20RHS%202018-19_0.pdf  
The data file in this repository is a transcription/derived analysis table based on the cited official report; the staffing percentages are calculated from reported shortfall counts and required posts.

## References
1. Ministry of Health and Family Welfare, Government of India. *Rural Health Statistics 2018–19*. Published 24 December 2019. Table 8, Table 19 and Table 28.
2. data.gov.in. *Rural Health Statistics 2019* catalogue.
3. Government of India, Ministry of Health and Family Welfare. *Rural Health Statistics 2018–19*, notes on `*` (surplus), NA and not applicable.

## Declaration
This project uses publicly available government data for academic analysis. The source data, derived features, cleaning decisions and executed outputs are documented in this repository. The student should verify the final figures and follow the course policy for disclosure of AI-assisted work.
"""
    (ROOT / "report" / "journal_report.md").write_text(report, encoding="utf-8")

if __name__ == "__main__":
    main()

# Clustering States by Rural Health-Infrastructure Shortfall
## Case study: State/UT profiles using Rural Health Statistics 2018–19

**Student:** Uddey Kanojia  
**University Roll No.:** 24020570044  
**Assignment No.:** 39 (serial no. in allocation sheet)  
**Problem No.:** 12  
**Group:** 12  
**Domain:** Health / Infrastructure  
**Article type:** Case Study — policy-oriented descriptive analysis

### Abstract
This case study examines differences in rural health infrastructure and health-worker shortfall across Indian States and Union Territories using the Government of India’s Rural Health Statistics 2018–19, with data reported up to 31 March 2019 and rural population estimates for 1 July 2019. Five indicators were used: SC, PHC and CHC facility shortfall percentages; allopathic doctor shortfall percentage at rural PHCs; and specialist-doctor shortfall percentage at rural CHCs. K-means clustering (K=3) and Ward hierarchical clustering were applied after standardisation. The executed analysis used 33 complete State/UT records from 36 source rows. K-means silhouette score was 0.445; hierarchical silhouette score was 0.445. Clusters are descriptive profiles, not official classifications or causal findings.

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
The executed script retained **33** complete State/UT records and excluded **3** incomplete records. The K-means silhouette score was **0.445** and Davies–Bouldin index was **0.851**. The hierarchical silhouette score was **0.445** and Davies–Bouldin index was **0.851**.

### 5.1 K-means cluster membership
- **Moderate shortfall** (18 States/UTs): Arunachal Pradesh, Chhattisgarh, Goa, Gujarat, Himachal Pradesh, Kerala, Manipur, Mizoram, Nagaland, Odisha, Rajasthan, Sikkim, Tamil Nadu, Tripura, Uttarakhand, A & N Islands, D & N Haveli, Lakshadweep
- **High shortfall** (11 States/UTs): Assam, Bihar, Haryana, Jharkhand, Madhya Pradesh, Maharashtra, Meghalaya, Punjab, Uttar Pradesh, West Bengal, Puducherry
- **Low shortfall** (4 States/UTs): Andhra Pradesh, Jammu & Kashmir, Karnataka, Telangana

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

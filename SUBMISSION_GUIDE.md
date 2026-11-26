# Submission guide

## Correct assignment identity
- Student: Uddey Kanojia
- University Roll No.: 24020570044
- Allocation sheet serial number: 39
- Assigned Problem No.: 12
- Group: 12
- Project: Clustering states by rural health-infrastructure shortfall

**Important:** The allocation workbook lists serial no. 39 and Problem No. 12. Your earlier PDF shows assignment number 39 in the project metadata; use **Problem No. 12** in the final journal, and serial no. 39 only where the form asks for the allocation serial number.

## What is included
- `data/rural_health_shortfall_2019.csv`: original-source-derived State/UT dataset, not synthetic.
- `src/run_analysis.py`: full reproducible pipeline.
- `results/`: outputs created by executing the script.
- `report/journal_report.md` and `report/journal_report.pdf`: generated journal draft.
- `README.md`: GitHub overview and exact run instructions.

## Before submission
1. Open the official MoHFW report and verify the transcribed source values.
2. Install the packages and run `python src/run_analysis.py` from the repository root.
3. Confirm the output files are regenerated and the metrics match `results/analysis_summary.json`.
4. Read the journal and correct any source/transcription issue you find.
5. Add the repository to your own GitHub account and submit the public URL.

## Publish to GitHub
Create a **public** repository named `Rural-Health-Infrastructure-Clustering` on your own GitHub account. Do not upload your friend's repository as your own or claim their code/data as yours.

From the extracted project folder:

```bash
git init
git add .
git commit -m "Initial rural health infrastructure clustering project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Rural-Health-Infrastructure-Clustering.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Then open the repository in a browser and verify the README, data, source code, journal and result figures are visible. Submit that URL.

## Academic integrity
This is a prepared starter package based on the allocated topic and cited public data. Verify the data and generated findings yourself, and follow your instructor's policy for AI assistance disclosure. Do not submit unverified results.

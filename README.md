# Air Quality Analysis — Applied Statistics Course Project

Statistical analysis of air pollution patterns across Indian cities (Option A).

**Data:** CPCB daily ambient air quality, 2015, for Gujarat, Odisha and West Bengal (data.gov.in).
Pollutants: SO2, NO2, RSPM/PM10, PM2.5 (µg/m³). Analysis file: `data/clean/air_quality_final.csv`
(3,778 complete station-day records, 2015-01-01 to 2015-12-31).

## Structure

```
data/raw/        original CPCB files — never edited
data/clean/      analysis-ready files + cleaning log and summaries (M1)
src/             shared code: figure style (style.py), data loading (data.py), CPCB AQI (aqi.py)
results/         every table produced by the notebooks (CSV, prefixed m2_ … m5_)
notebooks/
  01_collection_cleaning.ipynb   M1  Data Lead
  02_eda_normality.ipynb         M2  EDA Lead
  03_tests_anova.ipynb           M3  Inference Lead
  04_correlation_factor.ipynb    M4  Multivariate Lead
  05_regression_models.ipynb     M5  Regression Lead
figures/         exported figures (PNG, 200 dpi, style in docs/style_guide.md)
slides/          presentation deck (air_quality_presentation.pptx) and build_deck.py
docs/            roadmap, data dictionary, style guide, Q&A, synthesis
```

## Headline results

See [docs/synthesis.md](docs/synthesis.md) for the full interpretation.

- Kolkata's typical PM2.5 is **1.44×** Cuttack's (Welch t, 95% CI 1.34–1.56, d = 0.79); winter is **1.59×** the monsoon at the same stations.
- State (η² = 0.17) and season (η² = 0.08) both matter, and they interact (Welch ANOVA, Games-Howell).
- Pollutants are right-skewed; a log transform (Box-Cox λ ≈ 0) fixes most of it.
- One latent "particulate load" factor (KMO 0.58, parallel analysis → 1 factor, 54% of variance).
- State, season, site type and SO2 explain 49% of log PM2.5; logistic models classify AQI > 100 days with AUC 0.85.

## Reproducing

```
pip install -r requirements.txt
cd notebooks
jupyter nbconvert --to notebook --execute --inplace 01_collection_cleaning.ipynb 02_eda_normality.ipynb 03_tests_anova.ipynb 04_correlation_factor.ipynb 05_regression_models.ipynb
cd ..
python slides/build_deck.py
```

Notebooks 02–05 read `data/clean/air_quality_final.csv` and write to `figures/` and `results/`.
Notebook 01 (M1) rebuilds  from . Run 04 before 05 (05 uses the factor scores).

## Working rules

- Everyone reads the same clean file, produced only by M1.
- Fix a random seed for anything random.
- Commit small changes often with clear messages; don't edit someone else's notebook without telling them.
- Same variable names and units everywhere.


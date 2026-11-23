# Air Quality Analysis — Applied Statistics Course Project

Statistical analysis of air pollution patterns across Indian cities (Option A).

**Data:** CPCB daily ambient air quality, 2015, for Gujarat, Odisha and West Bengal (data.gov.in).
Pollutants: SO2, NO2, RSPM/PM10, PM2.5 (µg/m³). Analysis file: `data/clean/air_quality_final.csv`
(3,778 complete station-day records, 2015-01-01 to 2015-12-31).

## Structure

```
data/raw/        original CPCB files — never edited
data/clean/      analysis-ready files + cleaning log and summaries (M1)
notebooks/
  01_collection_cleaning.ipynb   M1  Data Lead
  02_eda_normality.ipynb         M2  EDA Lead
  03_tests_anova.ipynb           M3  Inference Lead
  04_correlation_factor.ipynb    M4  Multivariate Lead
  05_regression_models.ipynb     M5  Regression Lead
figures/         exported figures (consistent style, see style guide)
slides/          presentation deck
docs/            roadmap, data dictionary, Q&A
```

## Working rules

- Everyone reads the same clean file, produced only by M1.
- Fix a random seed for anything random.
- Commit small changes often with clear messages; don't edit someone else's notebook without telling them.
- Same variable names and units everywhere.

## Setup

```
pip install -r requirements.txt
```

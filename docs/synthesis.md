# What it all means: interpretation synthesis (M4)

**Data:** 3,778 daily (24-hour) readings from 71 CPCB monitoring stations in 30 cities across Gujarat, Odisha
and West Bengal, 2015. Pollutants: SO2, NO2, PM10 and PM2.5 (µg/m³). AQI was computed with the CPCB
National AQI formula from these four pollutants.

## Answers to the research questions

| # | Question | Answer in one line | Key numbers |
|---|---|---|---|
| 1 | Two groups: does PM2.5 differ between two cities, or between two periods? | **Yes.** Kolkata is clearly more polluted than Cuttack, and winter is clearly worse than the monsoon. | Kolkata 1.44× Cuttack (95% CI 1.34–1.56), Welch p < 0.001, d = 0.79. Winter 1.59× monsoon at the same stations (CI 1.39–1.82), d_z = 1.13 |
| 2 | 3+ groups: does PM2.5 differ across states and seasons? | **Yes.** West Bengal is highest, then Odisha, then Gujarat. Season matters too, and the seasonal swing differs by state. | Welch F = 494, η² = 0.17 (states). η² = 0.075 (seasons). Interaction partial η² = 0.11 |
| 3 | Are concentrations normal? Does a log help? | **No**, they are strongly right-skewed. **A log transform fixes most of the skew** for PM2.5 and PM10, but not for SO2 (detection floor) or NO2. | Skewness of PM2.5 drops from 2.8 to 0.2. Box-Cox λ ≈ 0 |
| 4 | Which pollutants move together? | **PM2.5 and PM10**, strongly. The gases are only weakly linked to them overall, but in West Bengal everything rises and falls together. | r = 0.76 (PM10–PM2.5). r = 0.84–0.94 in West Bengal |
| 5 | Hidden factors? | **One clear factor**, "particulate pollution". A second "combustion gases" factor (SO2, NO2) appears in an exploratory model. With only 4 pollutants this is limited. | KMO 0.58, Bartlett p < 0.001. 1 factor = 54% of variance (2 factors = 76%) |
| 6a | What explains PM2.5 (multiple regression)? | **Where (state), when (season), what kind of site, and SO2.** Together they explain about half the variation. | R² = 0.49. West Bengal ×2.6 Gujarat. Winter ×1.42 monsoon. Doubling SO2 → +25% PM2.5 |
| 6b | Can we classify bad-air days (logistic regression)? | **Yes, well**, without even using PM10 or PM2.5. | AUC 0.85 for AQI > 100. AUC 0.92 for AQI > 200 |
| 7 | Do stations cluster? | **Yes, into 4 profiles.** These follow geography and industry: the Gujarat network, the Kolkata area with Odisha industrial hubs, clean coastal Odisha towns, and the Odisha mining/steel belt. | k = 4, silhouette 0.53 |

## The story in five sentences

1. Air quality in these three states is **not uniformly bad**. Most days are "Satisfactory" (62%), but 31% are
   "Moderate or worse", and almost all of the worst days are in **West Bengal and industrial Odisha**.
2. **Season is the single most consistent driver.** PM2.5 is highest in winter and after the monsoon, and lowest
   in July–August, at 32 of 39 stations. This fits monsoon rain washing particles out and winter temperature
   inversions trapping them.
3. **Place matters more than anything else.** State explains the largest share of the variation, and West Bengal
   (the Kolkata area) is around 2.6× Gujarat for the same gas levels and season.
4. **Particulates dominate.** PM10 or PM2.5 sets the AQI on almost every day (PM10 on 77% of days, PM2.5 on 23%).
   The two particulates form one shared factor.
5. Days that cross the "Moderate" (AQI > 100) and "Poor" (AQI > 200) lines are predictable from **season, location
   and gas levels**. That makes simple early-warning rules feasible.

## Statistical vs practical significance

With thousands of observations almost every test gives p < 0.001, so we judge results by their **size**:

- **Large:** state differences (ratios of 1.5–2.6×) and the winter–monsoon difference (1.6×, d_z = 1.1). These
  are big enough to matter for health. West Bengal's mean PM2.5 (65 µg/m³) is above the 24-hour Indian standard
  of 60.
- **Moderate:** industrial vs residential sites (about 1.15×).
- **Small, not meaningful:** weekday vs weekend (0.88×, d = −0.25). This is probably caused by which stations
  happen to sample on weekends.

## Limitations (say these out loud)

1. **One year (2015), three states, manual stations.** We cannot generalise to all of India or to today.
2. **Missing PM2.5 in West Bengal.** 74% of its records had no PM2.5. The West Bengal results describe 4 cities,
   mostly around Kolkata, not the whole state.
3. **Gujarat data are unusually smooth** (CV of only 10–16%, almost no PM10–PM2.5 correlation). The Gujarat vs
   Odisha difference also disappears when we compare station means. Treat Gujarat results with caution.
4. **AQI is partial and circular.** Our AQI uses 4 of the 8 official pollutants, so it is a lower bound. Because
   AQI is computed from the pollutants, regressing AQI on them proves nothing. That is why our main model
   predicts PM2.5 instead.
5. **Repeated measurements.** Readings from the same station are correlated. We handled this with city-day
   averages, paired tests, station-mean ANOVAs and station-clustered standard errors, but it still limits how
   "independent" our n really is.
6. **No weather data, no causality.** Wind, rain and temperature drive pollution, and they are only captured
   indirectly through season. All results are associations, not causes.
7. **Factor analysis with 4 variables** can support only one well-identified factor (KMO 0.58 is mediocre).

## Future work

- Add meteorology (rainfall, wind speed, temperature) and more pollutants (CO, O3) from CAAQMS continuous
  stations.
- Use several years to separate trends from seasonal cycles, for example with a time-series model.
- Use mixed-effects models (stations nested in cities) instead of clustered standard errors.

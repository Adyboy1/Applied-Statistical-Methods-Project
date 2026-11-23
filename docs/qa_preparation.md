# Q&A preparation (M3)

Likely viva questions with short answers. Everyone should be able to answer all of these.

## Data

**1. Where does the data come from and why is it acceptable?**
It comes from CPCB's National Air Quality Monitoring Programme, as published on data.gov.in, which is one of
the sources the professor allowed. It is not from Kaggle. It contains daily 24-hour readings for 2015 from
three states.

**2. Why didn't you use the real-time AQI API?**
The real-time catalogue gives only the latest snapshot. Building a time series from it would have taken
weeks of collection. The historical daily files give a full year with seasonal variation.

**3. How did you handle missing data?**
We used complete-case analysis: 2,192 of 5,970 records (37%) were dropped, almost all of them West Bengal
rows with no PM2.5. We documented this (cleaning log, missingness heatmap) and stated that the West Bengal
results represent 4 cities.

**4. Why is SO2 stuck at 2 µg/m³ so often?**
2 µg/m³ is the reporting floor (detection limit) of the measurement method. 29% of SO2 values sit there, so
SO2 is left-censored. That is why no transform makes it normal.

**5. How did you compute AQI?**
We used the CPCB National AQI. For each pollutant, a sub-index is found by linear interpolation between the
official breakpoints. AQI is the maximum sub-index. We had 4 pollutants, which meets CPCB's minimum of 3
including a particulate.

## Normality and transforms

**6. Why test normality at all?**
t-tests, ANOVA and OLS inference assume normally distributed errors. The checks tell us whether to
transform the data or use non-parametric alternatives.

**7. All your normality tests reject. Doesn't that mean you can't use t-tests?**
With n ≈ 3,800, normality tests detect even trivial departures. We judged by skewness and Q-Q plots. After
the log transform, PM2.5 skewness is 0.19 and the Q-Q plot is nearly straight. With large samples the
central limit theorem makes t and F tests robust anyway, and we also ran Mann-Whitney and Kruskal-Wallis
as checks.

**8. Why log and not Box-Cox?**
Box-Cox estimated λ = −0.10 for PM2.5 and 0.11 for PM10, both close to 0, and λ = 0 is the log. The log
also has an easy interpretation: differences become ratios of geometric means.

**9. What is a geometric mean, and why report it?**
It is exp(mean of logs), the "typical" value of skewed data. Unlike the arithmetic mean, it is not pulled
up by a few extreme days.

## Tests

**10. Why Welch's t-test instead of Student's?**
Welch's test does not assume equal variances, and Levene's test showed the variances differ (p < 0.001).
Welch loses almost nothing when variances are equal, so it is a safe default.

**11. Why did you average to city-days for Kolkata vs Cuttack?**
Stations in the same city on the same day share the same weather, so they are not independent. Averaging
gives one observation per city per day.

**12. Why a paired test for winter vs monsoon?**
The same stations appear in both seasons. Pairing removes station-to-station differences and tests only the
within-station change.

**13. What is a p-value?**
It is the probability of seeing a difference at least this large if H0 (no difference) were true. A small
p-value means the data are unlikely under H0. It does not measure the size or importance of the effect.

**14. Everything is significant. So what?**
That is why we report effect sizes and confidence intervals. Kolkata vs Cuttack has d = 0.79 (large).
Weekday vs weekend has d = 0.25 (small, and probably an artefact).

**15. Why Welch ANOVA and Games-Howell rather than ordinary ANOVA and Tukey?**
The variances differ across groups (Levene p < 0.001). Welch ANOVA and Games-Howell do not assume equal
variances. We also show Tukey for comparison.

**16. What do η² and ω² mean?**
They give the share of variance in log PM2.5 explained by the grouping. η² = 0.17 means state explains 17%.
ω² is a less biased version; here it is almost identical.

**17. Why did Gujarat vs Odisha stop being significant on station means?**
With 71 stations instead of 3,778 station-days, the test is honest about how much independent information
we have. The difference is real at the day level but not consistent across stations.

**18. What does the state × season interaction mean?**
The seasonal effect is not the same everywhere. West Bengal swings from about 37 to 100 µg/m³ over the
year, while Gujarat barely changes.

## Factor analysis

**19. Why are KMO and Bartlett needed?**
Bartlett checks that the variables are correlated at all, which they are (p < 0.001). KMO checks that the
correlations are due to shared factors rather than pairs of variables. KMO = 0.58 is mediocre, so the
factor analysis is exploratory.

**20. How did you choose the number of factors?**
Eigenvalues above 1 (Kaiser), the scree elbow, and parallel analysis against random data. All three give
one factor.

**21. Why show a two-factor model if you only retain one?**
It is interpretable: particulates vs combustion gases. But with 4 variables, a 2-factor ML model has −1
degrees of freedom and is not identified, so we label it descriptive only.

**22. What is varimax rotation?**
An orthogonal rotation that makes each variable load strongly on as few factors as possible, so the factors
are easier to name. It does not change the total variance explained.

**23. Factor analysis vs PCA?**
PCA summarises total variance. FA models only the shared variance and treats the rest as unique error. They
agree here.

## Regression

**24. Why not just regress AQI on the pollutants?**
AQI is calculated from those pollutants, so the high R² (0.92) is guaranteed and tells us nothing. We show
it only to make that point. Our main model predicts PM2.5 from gases and context.

**25. Why leave PM10 out of the PM2.5 model?**
PM2.5 is part of PM10 (r = 0.76). Including it would be near-circular and would cause multicollinearity.

**26. How do you interpret the log SO2 coefficient of 0.32?**
It is an elasticity: 1% more SO2 goes with 0.32% more PM2.5, so doubling SO2 means about 25% more PM2.5.

**27. What diagnostics did you check?**
- VIF: at most 3.3, so no problematic multicollinearity.
- Breusch-Pagan: the residuals are heteroscedastic.
- Durbin-Watson 0.71: residuals from the same station are correlated.
- Residual Q-Q plot: mildly heavy-tailed.
- Cook's distance: maximum 0.007, so no influential points.
Because of the heteroscedasticity and correlated residuals, we use station-clustered robust standard errors.

**28. R² is only 0.49. Is that bad?**
Not for this kind of environmental data without weather variables. It means state, season, site type and
gas levels explain half the day-to-day variation. The rest is weather and local events.

**29. Why did NO2 become non-significant?**
NO2 is much higher in West Bengal, so it overlaps with the state effect. Once we account for state and
station clustering, NO2 adds little.

## Logistic regression and clustering

**30. Why AQI > 100 rather than "Poor or worse" as the main outcome?**
Poor-or-worse days are rare (5.6%) and never occur in Gujarat or in the monsoon. That causes perfect
separation, so we model it as a secondary analysis with a simpler specification.

**31. What does AUC = 0.85 mean?**
If you pick one bad day and one good day at random, the model gives the bad day a higher risk 85% of the
time. 0.5 is chance and 1 is perfect.

**32. Why is AUC lower (0.75) on held-out stations?**
When entire stations are unseen, the model cannot learn station-specific levels. 0.75 is the honest figure
for new stations.

**33. How did you choose k = 4 clusters?**
We used the silhouette score, taking the smallest k within 0.02 of the best value (parsimony). k-means and
Ward hierarchical clustering broadly agree.

**34. Can you claim causality, e.g. "industry causes PM2.5"?**
No. This is observational data. Associations could be confounded by weather, geography or monitoring
practice.

"""Build the presentation deck from the exported figures and results.

Run from the project root:  python slides/build_deck.py
Output: slides/air_quality_presentation.pptx
"""
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
OUT = ROOT / "slides" / "air_quality_presentation.pptx"

# Palette: smog slate dominant, vermillion accent (matches the figure style guide)
DARK = RGBColor(0x1F, 0x2A, 0x36)
MID = RGBColor(0x4A, 0x5A, 0x6A)
LIGHT_BG = RGBColor(0xEE, 0xF1, 0xF4)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT = RGBColor(0xD5, 0x5E, 0x00)
MUTED = RGBColor(0x6B, 0x75, 0x80)
HEAD, BODY = "Cambria", "Calibri"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
W, H = 13.333, 7.5


def bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def text(slide, x, y, w, h, runs, size=16, color=DARK, font=BODY, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, italic=False):
    """runs: str or list of paragraphs; a paragraph is a str or list of (text, {opts})."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    paras = runs if isinstance(runs, list) else [runs]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(6)
        segs = para if isinstance(para, list) else [(para, {})]
        for seg, opt in segs:
            r = p.add_run()
            r.text = seg
            f = r.font
            f.name = opt.get("font", font)
            f.size = Pt(opt.get("size", size))
            f.bold = opt.get("bold", bold)
            f.italic = opt.get("italic", italic)
            f.color.rgb = opt.get("color", color)
    return tb


def bullets(slide, x, y, w, h, items, size=16, color=DARK):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(10)
        segs = item if isinstance(item, list) else [(item, {})]
        first = True
        for seg, opt in segs:
            r = p.add_run()
            r.text = ("•  " if first else "") + seg
            first = False
            r.font.name = BODY
            r.font.size = Pt(opt.get("size", size))
            r.font.bold = opt.get("bold", False)
            r.font.color.rgb = opt.get("color", color)
    return tb


def title(slide, t, presenter=None):
    text(slide, 0.6, 0.35, W - 2.6, 0.9, t, size=30, font=HEAD, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    if presenter:
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(W - 1.75), Inches(0.55), Inches(1.15), Inches(0.42))
        pill.fill.solid(); pill.fill.fore_color.rgb = LIGHT_BG; pill.line.fill.background()
        tf = pill.text_frame; tf.margin_left = tf.margin_right = Inches(0.05)
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = presenter
        r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = MID; r.font.name = BODY


def picture(slide, name, x, y, max_w, max_h):
    path = FIG / f"{name}.png"
    iw, ih = Image.open(path).size
    scale = min(max_w / iw, max_h / ih)
    w, h = iw * scale, ih * scale
    return slide.shapes.add_picture(str(path), Inches(x + (max_w - w) / 2), Inches(y + (max_h - h) / 2), Inches(w), Inches(h))


def card(slide, x, y, w, h, big, label, big_color=ACCENT, fill=LIGHT_BG):
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    box.fill.solid(); box.fill.fore_color.rgb = fill; box.line.fill.background()
    box.adjustments[0] = 0.08
    text(slide, x + 0.2, y + 0.12, w - 0.4, h * 0.55, big, size=30, font=HEAD, bold=True, color=big_color,
         anchor=MSO_ANCHOR.BOTTOM)
    text(slide, x + 0.2, y + h * 0.6, w - 0.4, h * 0.38, label, size=13, color=MUTED)


def so_what(slide, msg, y=6.55):
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(y), Inches(W - 1.2), Inches(0.6))
    box.fill.solid(); box.fill.fore_color.rgb = DARK; box.line.fill.background()
    box.adjustments[0] = 0.3
    text(slide, 0.85, y, W - 1.7, 0.6, [[("So what?  ", {"bold": True, "color": ACCENT}), (msg, {"color": WHITE})]],
         size=15, anchor=MSO_ANCHOR.MIDDLE)


def new(color=WHITE):
    s = prs.slides.add_slide(BLANK)
    bg(s, color)
    return s


# 1 Title -------------------------------------------------------------------
s = new(DARK)
text(s, 0.8, 1.6, 11.5, 1.6, "Where and when is the air worst?", size=44, font=HEAD, bold=True, color=WHITE)
text(s, 0.8, 3.0, 11.5, 1.0, "Statistical analysis of air pollution across 30 cities in Gujarat, Odisha and West Bengal (CPCB, 2015)",
     size=20, color=RGBColor(0xC8, 0xD0, 0xD8))
text(s, 0.8, 5.2, 11.5, 0.5, "Team Smog Squad  ·  Applied Statistical Methods  ·  November 2026", size=16, color=ACCENT, bold=True)
text(s, 0.8, 5.7, 11.5, 0.5, "M1 Data  ·  M2 EDA  ·  M3 Inference  ·  M4 Multivariate  ·  M5 Regression", size=14,
     color=RGBColor(0xC8, 0xD0, 0xD8))
s.notes_slide.notes_text_frame.text = ("M5: Welcome. We studied 3,778 daily air-quality readings from 71 monitoring stations "
                                       "to find where and when pollution is worst, and what goes with it.")

# 2 Problem and research questions ------------------------------------------------
s = new()
title(s, "Why air quality, and what we asked", "M4")
text(s, 0.6, 1.45, 4.6, 0.5, "Why it matters", size=20, font=HEAD, bold=True)
bullets(s, 0.6, 2.0, 4.6, 3.8, [
    "PM2.5 reaches deep into the lungs; India's 24-h limit is 60 µg/m³",
    "Pollution varies by place and season, so policy needs to know where and when",
    "Public CPCB data let us test this with the methods from the course",
], size=16)
qs = [("1", "Do two cities or two seasons differ?", "t-tests"),
      ("2", "Do states and seasons differ?", "ANOVA"),
      ("3", "Are pollutants normally distributed?", "normality tests"),
      ("4", "Which pollutants move together?", "correlation"),
      ("5", "Are there hidden factors?", "factor analysis"),
      ("6", "What explains PM2.5 and bad-AQI days?", "regression, logistic"),
      ("7", "Do stations form groups?", "clustering")]
for i, (n, q, m) in enumerate(qs):
    y = 1.45 + i * 0.68
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5.8), Inches(y), Inches(0.5), Inches(0.5))
    c.fill.solid(); c.fill.fore_color.rgb = ACCENT if i < 6 else MUTED; c.line.fill.background()
    tf = c.text_frame; tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = n; r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = BODY
    text(s, 6.5, y + 0.02, 4.4, 0.5, q, size=16, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 10.9, y + 0.02, 1.9, 0.5, m, size=13, color=MUTED, italic=True, anchor=MSO_ANCHOR.MIDDLE)
s.notes_slide.notes_text_frame.text = ("M4: Fine particles are the main health risk from air pollution. We asked seven questions, "
                                       "each matched to a method from the syllabus; question 7 is a bonus.")

# 3 Data -------------------------------------------------------------------------
s = new()
title(s, "Data: one year of CPCB daily monitoring", "M1")
stats_ = [("3,778", "complete station-days"), ("71", "monitoring stations"), ("30", "cities in 3 states"), ("2015", "Jan–Dec, ~2 samples/week")]
for i, (b, l) in enumerate(stats_):
    card(s, 0.6 + i * 3.08, 1.5, 2.85, 1.55, b, l)
text(s, 0.6, 3.45, 6.0, 0.5, "Source and variables", size=20, font=HEAD, bold=True)
bullets(s, 0.6, 4.0, 6.0, 2.4, [
    "CPCB National Air Quality Monitoring Programme, via data.gov.in (OGD licence)",
    "SO2, NO2, PM10, PM2.5 as 24-hour averages in µg/m³",
    "AQI computed with the CPCB National AQI formula",
], size=16)
text(s, 7.0, 3.45, 5.7, 0.5, "Why this dataset", size=20, font=HEAD, bold=True)
bullets(s, 7.0, 4.0, 5.7, 2.4, [
    "Allowed source (not Kaggle), well documented",
    "A full year gives seasons; the live API gives only a snapshot",
    "3 states give contrast: coastal industry, mining belt, a megacity",
], size=16)
so_what(s, "Enough data for every method in the course, with real seasonal and regional contrast")
s.notes_slide.notes_text_frame.text = ("M1: Each row is one station on one day. We used historical files rather than the live API "
                                       "because the live API only returns the latest reading.")

# 4 Cleaning ---------------------------------------------------------------------
s = new()
title(s, "Cleaning: 5,970 raw rows → 3,778 analysis rows", "M1")
picture(s, "m2_missingness_heatmap", 0.5, 1.35, 8.2, 5.0)
steps = ["Combined 3 state files (5,970 rows)", "Trimmed text, upper-cased city names",
         "Parsed dates (0 invalid)", "Negative readings set to missing",
         "Complete cases kept: 3,778 rows (63%)"]
for i, st in enumerate(steps):
    y = 1.5 + i * 0.9
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.0), Inches(y), Inches(0.45), Inches(0.45))
    c.fill.solid(); c.fill.fore_color.rgb = DARK; c.line.fill.background()
    p = c.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = str(i + 1); r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = WHITE
    text(s, 9.6, y - 0.05, 3.3, 0.6, st, size=15, anchor=MSO_ANCHOR.MIDDLE)
so_what(s, "74% of West Bengal rows lacked PM2.5, so West Bengal results describe the Kolkata area (4 cities)")
s.notes_slide.notes_text_frame.text = ("M1: Almost all missing data is PM2.5 in West Bengal. We used complete cases and say so openly. "
                                       "The full cleaning log is in data/clean/cleaning_log.csv.")

# 5 EDA ----------------------------------------------------------------------------
s = new()
title(s, "Pollution peaks in winter and dips in the monsoon", "M2")
picture(s, "m2_timeseries_particulates", 0.5, 1.35, 8.4, 5.0)
card(s, 9.2, 1.5, 3.6, 1.45, "65 µg/m³", "mean PM2.5 in West Bengal, above the 60 limit")
card(s, 9.2, 3.15, 3.6, 1.45, "×2.8", "Nov vs Aug PM2.5 in West Bengal (103 vs 37)")
card(s, 9.2, 4.8, 3.6, 1.45, "Flat", "Gujarat all year (CV 16%): unusually smooth data", big_color=MID)
so_what(s, "Place and season drive pollution; Gujarat's data need to be read with caution")
s.notes_slide.notes_text_frame.text = ("M2: Monthly means by state. Odisha and West Bengal follow a U-shape: worst Nov–Feb, "
                                       "best Jul–Aug, consistent with monsoon rain washing particles out. Gujarat barely moves.")

# 6 Normality ---------------------------------------------------------------------
s = new()
title(s, "Skewed data: a log transform fixes most of it", "M2")
picture(s, "m2_qq_hist_log", 0.5, 1.35, 8.4, 5.0)
rows = [("PM2.5", "2.81", "0.19"), ("PM10", "2.72", "-0.24"), ("NO2", "2.06", "0.56"), ("SO2", "1.27", "-0.16*")]
tbl = s.shapes.add_table(len(rows) + 1, 3, Inches(9.2), Inches(1.5), Inches(3.6), Inches(2.2)).table
for j, hdr in enumerate(["Skewness", "Raw", "Log"]):
    tbl.cell(0, j).text = hdr
for i, r_ in enumerate(rows, start=1):
    for j, v in enumerate(r_):
        tbl.cell(i, j).text = v
for i in range(len(rows) + 1):
    for j in range(3):
        c = tbl.cell(i, j)
        c.fill.solid(); c.fill.fore_color.rgb = DARK if i == 0 else (LIGHT_BG if i % 2 else WHITE)
        for p in c.text_frame.paragraphs:
            for r in p.runs:
                r.font.size = Pt(14); r.font.name = BODY; r.font.bold = i == 0
                r.font.color.rgb = WHITE if i == 0 else DARK
bullets(s, 9.2, 4.0, 3.6, 2.4, [
    "Shapiro-Wilk, D'Agostino, Anderson-Darling and Lilliefors all reject on raw data",
    "Box-Cox λ ≈ 0, so log is the right transform",
    "*SO2 stuck at a 2 µg/m³ floor",
], size=14)
so_what(s, "Use log values with non-parametric checks; with n ≈ 3,800 the tests flag even tiny departures")
s.notes_slide.notes_text_frame.text = ("M2: Raw skewness of 1.3–2.8 drops to about 0.2 for particulates after logging, and the Q-Q plots "
                                       "become nearly straight. The formal tests still reject at this sample size, so we rely on the plots "
                                       "and skewness. SO2 cannot be normalised because 29% of values sit at the detection floor.")

# 7 Two-sample --------------------------------------------------------------------
s = new()
title(s, "Kolkata breathes 44% more PM2.5 than Cuttack", "M3")
picture(s, "m3_two_sample_kolkata_cuttack", 0.5, 1.35, 8.4, 5.0)
card(s, 9.2, 1.5, 3.6, 1.45, "1.44×", "Kolkata vs Cuttack, 95% CI 1.34–1.56 (Welch p < 0.001, d = 0.79)")
card(s, 9.2, 3.15, 3.6, 1.45, "1.59×", "winter vs monsoon at the same 39 stations (paired t, d = 1.13)")
card(s, 9.2, 4.8, 3.6, 1.45, "32 / 39", "stations are worse in winter (Wilcoxon p < 0.001)", big_color=MID)
so_what(s, "Both differences are large, not just significant: effect sizes are 0.8 to 1.1")
s.notes_slide.notes_text_frame.text = ("M3: H0 is equal mean log PM2.5. Levene rejects equal variances, so we used Welch's t-test on "
                                       "city-day averages. Mann-Whitney agrees. Winter vs monsoon is paired by station. "
                                       "Weekday vs weekend was small (d = 0.25) and likely a sampling artefact.")

# 8 ANOVA ------------------------------------------------------------------------
s = new()
title(s, "States and seasons differ, and they interact", "M3")
picture(s, "m3_interaction_state_season", 0.5, 1.35, 8.4, 5.0)
card(s, 9.2, 1.5, 3.6, 1.45, "η² = 0.17", "state, Welch F(2, 1507) = 494; Kruskal-Wallis agrees")
card(s, 9.2, 3.15, 3.6, 1.45, "η² = 0.08", "season, Welch F(3, 1839) = 104")
card(s, 9.2, 4.8, 3.6, 1.45, "ηp² = 0.11", "state × season interaction, two-way ANOVA", big_color=MID)
so_what(s, "West Bengal is 1.9× Gujarat (Games-Howell); Gujarat vs Odisha is not robust at station level")
s.notes_slide.notes_text_frame.text = ("M3: Unequal variances, so Welch ANOVA with Games-Howell post-hoc. Repeating on 71 station means, "
                                       "West Bengal still differs from both, but Gujarat vs Odisha has p = 0.07. "
                                       "The interaction: the seasonal swing is large in West Bengal and flat in Gujarat.")

# 9 Correlation --------------------------------------------------------------------
s = new()
title(s, "PM2.5 and PM10 move together; the gases only loosely", "M4")
picture(s, "m4_correlation_heatmap", 0.5, 1.35, 8.4, 5.0)
card(s, 9.2, 1.5, 3.6, 1.45, "r = 0.76", "PM10–PM2.5, the strongest pair")
card(s, 9.2, 3.15, 3.6, 1.45, "r = 0.84–0.94", "within West Bengal: everything rises together")
card(s, 9.2, 4.8, 3.6, 1.45, "r = 0.19", "PM10–PM2.5 within Gujarat: suspicious", big_color=MID)
so_what(s, "Pooled correlations hide very different state patterns, so check within groups")
s.notes_slide.notes_text_frame.text = ("M4: Pearson on log values, Spearman on raw values, and they agree. Within West Bengal all four "
                                       "pollutants are strongly correlated, suggesting one shared driver such as winter inversions.")

# 10 Factor analysis --------------------------------------------------------------
s = new()
title(s, "One hidden factor: overall particulate load", "M4")
picture(s, "m4_factor_loadings", 0.5, 1.35, 8.4, 5.0)
bullets(s, 9.2, 1.5, 3.6, 4.8, [
    [("Bartlett ", {"bold": True}), ("χ² = 4,423, p < 0.001", {})],
    [("KMO 0.58 ", {"bold": True}), ("is mediocre with only 4 variables", {})],
    [("Scree, Kaiser and parallel analysis ", {"bold": True}), ("all retain 1 factor (54%)", {})],
    [("Exploratory 2-factor varimax: ", {"bold": True}), ("particulates (44%) + combustion gases SO2/NO2 (31%)", {})],
], size=15)
so_what(s, "Pollution here is mostly one dimension, particulate load; West Bengal fits it best (79% of variance)")
s.notes_slide.notes_text_frame.text = ("M4: One-factor ML loadings: PM2.5 0.88, PM10 0.86, NO2 0.40, SO2 0.33. A two-factor ML model "
                                       "is not identified with 4 variables, so the varimax solution is descriptive. PCA agrees.")

# 11 Regression -------------------------------------------------------------------
s = new()
title(s, "Place, season and SO2 explain half of PM2.5", "M5")
picture(s, "m5_coefficients", 0.5, 1.35, 8.4, 5.0)
card(s, 9.2, 1.5, 3.6, 1.45, "R² = 0.49", "log PM2.5 model, F(9, 3768) = 396; AIC favours every block")
card(s, 9.2, 3.15, 3.6, 1.45, "×2.6", "West Bengal vs Gujarat, other factors held equal")
card(s, 9.2, 4.8, 3.6, 1.45, "+25%", "PM2.5 when SO2 doubles (elasticity 0.32)", big_color=MID)
so_what(s, "We predict PM2.5 rather than AQI, because AQI is built from the pollutants (R² 0.92 would be circular)")
s.notes_slide.notes_text_frame.text = ("M5: Diagnostics: VIF at most 3.3; Breusch-Pagan and Durbin-Watson flagged heteroscedasticity and "
                                       "within-station correlation, so we used station-clustered robust SEs. Max Cook's D is 0.007. "
                                       "NO2 drops out once state is controlled.")

# 12 Logistic + clusters ---------------------------------------------------------------
s = new()
title(s, "Bad-air days are predictable without using PM at all", "M5")
picture(s, "m5_logistic_roc_confusion", 0.5, 1.35, 8.4, 5.0)
card(s, 9.2, 1.5, 3.6, 1.45, "AUC 0.85", "AQI > 100: 81% accuracy vs 69% baseline")
card(s, 9.2, 3.15, 3.6, 1.45, "AUC 0.92", "AQI > 200: sensitivity 86%, specificity 86%")
card(s, 9.2, 4.8, 3.6, 1.45, "OR ≈ 18", "winter vs monsoon odds of AQI > 100", big_color=MID)
so_what(s, "Season, place and gas levels could drive a simple early-warning rule; AUC on unseen stations is 0.75")
s.notes_slide.notes_text_frame.text = ("M5: Predictors are log NO2, log SO2, season, site type and state, with a 70/30 split (seed 42). "
                                       "Bonus: k-means gives 4 station profiles (silhouette 0.53), see appendix.")

# 13 Findings and limitations ----------------------------------------------------------
s = new()
title(s, "What it all means", "M4 · M5")
text(s, 0.6, 1.45, 6.0, 0.5, "Key findings", size=22, font=HEAD, bold=True, color=ACCENT)
bullets(s, 0.6, 2.05, 6.0, 4.3, [
    "The Kolkata area is the hotspot: 1.4–2.6× other places",
    "Winter is about 1.6× the monsoon at the same stations",
    "Pollution is mostly one dimension: particulate load",
    "Season, place and SO2 explain about half of PM2.5",
    "Bad-AQI days are predictable (AUC 0.85–0.92)",
], size=17)
text(s, 7.0, 1.45, 5.8, 0.5, "Limitations", size=22, font=HEAD, bold=True, color=MID)
bullets(s, 7.0, 2.05, 5.8, 4.3, [
    "One year, 3 states, manual stations",
    "West Bengal PM2.5 mostly missing; Gujarat data unusually smooth",
    "Partial AQI (4 of 8 pollutants)",
    "No weather data: associations, not causes",
    "Repeated station measures (handled with clustered SEs)",
], size=17)
so_what(s, "Target winter, the Kolkata area and industrial Odisha first; add weather data next")
s.notes_slide.notes_text_frame.text = ("M4 and M5: Future work: add meteorology and CO/O3 from continuous stations, use several years, "
                                       "and fit mixed-effects models with stations nested in cities.")

# 14 Thank you ------------------------------------------------------------------
s = new(DARK)
text(s, 0.8, 2.2, 11.5, 1.2, "Thank you. Questions?", size=44, font=HEAD, bold=True, color=WHITE)
text(s, 0.8, 4.4, 11.7, 1.6, [
    "Data: Central Pollution Control Board (CPCB), NAMP daily data 2015, via Open Government Data Platform India "
    "(data.gov.in), Government Open Data Licence – India.",
    "Code, notebooks and figures: github.com/Adyboy1/Applied-Statistical-Methods-Project",
], size=14, color=RGBColor(0xC8, 0xD0, 0xD8))
s.notes_slide.notes_text_frame.text = "All: see docs/qa_preparation.md for likely questions."

# Appendix ----------------------------------------------------------------------
for name, ttl, note in [
    ("m5_station_clusters", "Appendix: four station pollution profiles",
     "k-means with k = 4 (silhouette 0.53): the Gujarat network; the Kolkata area plus Angul, Talcher and Cuttack; clean coastal "
     "Odisha; the Odisha mining and steel belt."),
    ("m5_ols_diagnostics", "Appendix: regression diagnostics", "Residuals vs fitted, Q-Q, scale-location and Cook's distance."),
    ("m4_scree_parallel", "Appendix: scree plot and parallel analysis", "Only the first eigenvalue beats random data."),
    ("m2_boxplot_pm25_by_city", "Appendix: PM2.5 by city", "Dashed line: the 24-hour standard of 60 µg/m³."),
]:
    s = new()
    title(s, ttl)
    picture(s, name, 0.6, 1.35, W - 1.2, 5.8)
    s.notes_slide.notes_text_frame.text = note

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")

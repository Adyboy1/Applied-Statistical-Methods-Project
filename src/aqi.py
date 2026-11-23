"""Indian National AQI (CPCB, 2014) sub-indices from 24-hour concentrations.

AQI = max(sub-indices). Only SO2, NO2, PM10 and PM2.5 are available here
(CO, O3, NH3 and Pb are not in the 2015 manual-station files), which meets
CPCB's minimum of three pollutants including one particulate.
Sub-indices use piecewise-linear interpolation between the CPCB breakpoints.
"""
import numpy as np
import pandas as pd

AQI_BREAKS = [0, 50, 100, 200, 300, 400, 500]
CONC_BREAKS = {
    "PM10": [0, 50, 100, 250, 350, 430, 600],
    "PM25": [0, 30, 60, 90, 120, 250, 380],
    "NO2": [0, 40, 80, 180, 280, 400, 800],
    "SO2": [0, 40, 80, 380, 800, 1600, 2400],
}
CATEGORIES = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]


def sub_index(conc, pollutant):
    c = np.clip(np.asarray(conc, dtype=float), 0, CONC_BREAKS[pollutant][-1])
    return np.interp(c, CONC_BREAKS[pollutant], AQI_BREAKS)


def category(aqi):
    return pd.cut(aqi, [-0.1, 50, 100, 200, 300, 400, 500.1], labels=CATEGORIES)


def add_aqi_columns(df):
    df = df.copy()
    subs = pd.DataFrame({p: sub_index(df[p], p) for p in CONC_BREAKS}, index=df.index)
    df["AQI"] = subs.max(axis=1).round(1)
    df["AQI_driver"] = subs.idxmax(axis=1)
    df["AQI_category"] = category(df["AQI"])
    return df

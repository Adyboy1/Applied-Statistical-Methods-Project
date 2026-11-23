"""Shared loading helpers so every notebook uses the same variables and names."""
import numpy as np
import pandas as pd

from .style import ROOT

CLEAN = ROOT / "data" / "clean" / "air_quality_final.csv"
MASTER = ROOT / "data" / "clean" / "air_quality_master.csv"

POLLUTANTS = ["SO2", "NO2", "PM10", "PM25"]
RENAME = {
    "Sampling Date": "date",
    "State": "state",
    "City/Town/Village/Area": "city",
    "Location of Monitoring Station": "location",
    "Type of Location": "location_type",
    "Station_ID": "station",
    "Stn Code": "stn_code",
    "Agency": "agency",
    "RSPM/PM10": "PM10",
    "PM 2.5": "PM25",
}
SEASON_ORDER = ["Winter", "Summer", "Monsoon", "Post-monsoon"]
STATE_ORDER = ["Gujarat", "Odisha", "West Bengal"]

# Indian meteorological seasons (IMD convention)
_SEASON = {12: "Winter", 1: "Winter", 2: "Winter",
           3: "Summer", 4: "Summer", 5: "Summer",
           6: "Monsoon", 7: "Monsoon", 8: "Monsoon", 9: "Monsoon",
           10: "Post-monsoon", 11: "Post-monsoon"}
_LOC = {"Industrial Area": "Industrial",
        "Residential, Rural and other Areas": "Residential",
        "RIRUO": "Mixed (RIRUO)"}


def _tidy(df):
    df = df.rename(columns=RENAME)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month
    df["season"] = pd.Categorical(df["month"].map(_SEASON), SEASON_ORDER, ordered=True)
    df["weekday"] = df["date"].dt.dayofweek < 5
    df["location_class"] = df["location_type"].map(_LOC)
    return df


def load_clean(add_logs=True, add_aqi=True):
    df = _tidy(pd.read_csv(CLEAN))
    if add_logs:
        for p in POLLUTANTS:
            df[f"log_{p}"] = np.log(df[p])
    if add_aqi:
        from .aqi import add_aqi_columns
        df = add_aqi_columns(df)
    return df


def load_master():
    return _tidy(pd.read_csv(MASTER))

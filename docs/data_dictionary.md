# Data dictionary

**Source:** Central Pollution Control Board (CPCB), National Air Quality Monitoring Programme (NAMP),
daily manual-station data for 2015, published on data.gov.in (Open Government Data Licence – India).
Files: `cpcb_dly_aq_gujarat-2015.csv`, `cpcb_dly_aq_odisha-2015.csv`, `cpcb_dly_aq_west_bengal-2015.csv`.

**Analysis file:** `data/clean/air_quality_final.csv` (produced by M1, `notebooks/01_collection_cleaning.ipynb`).

| | |
|---|---|
| Unit of observation | one station on one sampling day (24-hour average) |
| Rows | 3,778 complete records (from 5,970 raw) |
| Stations / cities / states | 71 / 30 / 3 |
| Window | 1 Jan 2015 – 31 Dec 2015 (363 distinct sampling dates) |
| Sampling | NAMP manual sampling, roughly twice a week per station (not every day) |

## Variables in the CSV

| Column (raw name) | Name used in code | Type | Unit | Description |
|---|---|---|---|---|
| Stn Code | `stn_code` | text | – | CPCB station code (not unique across states) |
| Sampling Date | `date` | date | – | Date of the 24-h sample |
| State | `state` | category | – | Gujarat, Odisha, West Bengal |
| City/Town/Village/Area | `city` | category | – | City, upper-cased by M1 |
| Location of Monitoring Station | `location` | text | – | Station address |
| Agency | `agency` | category | – | Agency running the station (state PCBs, NEERI) |
| Type of Location | `location_type` | category | – | `Industrial Area`, `Residential, Rural and other Areas`, `RIRUO` (CPCB code for a mixed residential/industrial/rural/other zone) |
| SO2 | `SO2` | float | µg/m³ | Sulphur dioxide, 24-h mean |
| NO2 | `NO2` | float | µg/m³ | Nitrogen dioxide, 24-h mean |
| RSPM/PM10 | `PM10` | float | µg/m³ | Respirable suspended particulate matter (≤10 µm) |
| PM 2.5 | `PM25` | float | µg/m³ | Fine particulate matter (≤2.5 µm) |
| Station_ID | `station` | text | – | `State_StnCode_Location`, unique station key built by M1 |

## Derived variables (created in `src/data.py` and `src/aqi.py`)

| Name | Definition |
|---|---|
| `month` | Calendar month of `date` |
| `season` | IMD seasons: Winter (Dec–Feb), Summer (Mar–May), Monsoon (Jun–Sep), Post-monsoon (Oct–Nov) |
| `weekday` | True for Monday–Friday |
| `location_class` | Industrial / Residential / Mixed (RIRUO) |
| `log_SO2`, `log_NO2`, `log_PM10`, `log_PM25` | Natural log of each pollutant (all values are > 0) |
| `AQI` | Indian National AQI = max of the CPCB sub-indices for SO2, NO2, PM10, PM2.5 (piecewise-linear between CPCB 2014 breakpoints) |
| `AQI_driver` | Pollutant giving the highest sub-index |
| `AQI_category` | Good (0–50), Satisfactory (51–100), Moderate (101–200), Poor (201–300), Very Poor (301–400), Severe (401–500) |

## Known data-quality notes

- **West Bengal PM2.5:** 74% of West Bengal rows had no PM2.5 and were removed by complete-case filtering
  (638 of 2,497 kept, 4 of 13 cities). West Bengal results describe the stations that do measure PM2.5
  (mostly Kolkata, Howrah, Barrackpore, Durgapur), not the whole state.
- **SO2 detection floor:** 29% of SO2 values equal 2 µg/m³, the reporting floor of the method. SO2 is
  therefore censored at the low end; normality tests on SO2 are not meaningful without accounting for this.
- **AQI is partial:** the official AQI also uses CO, O3, NH3 and Pb, which are not in these files. Our AQI
  is a lower bound of the official AQI on each day.
- **Not every day:** each station samples ~twice a week, so consecutive rows of a station are 3–4 days apart.

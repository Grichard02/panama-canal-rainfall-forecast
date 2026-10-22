
from pathlib import Path
import requests
import pandas as pd
import numpy as np

# Punto de referencia aproximado en el lago Gatún
LATITUDE = 9.25
LONGITUDE = -79.90

URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

params = {
    "parameters": "PRECTOTCORR,T2M",
    "community": "AG",
    "longitude": LONGITUDE,
    "latitude": LATITUDE,
    "start": "19810101",
    "end": "20260930",
    "format": "JSON"
}

response = requests.get(URL, params=params, timeout=120)
response.raise_for_status()

payload = response.json()
variables = payload["properties"]["parameter"]

df = pd.DataFrame({
    "precip_mm_day": variables["PRECTOTCORR"],
    "temp_c": variables["T2M"]
})

df.index = pd.to_datetime(df.index, format="%Y%m%d")
df.index.name = "date"
df = df.sort_index()

# Sustituir códigos de valores faltantes
df = df.replace([-999, -999.0], np.nan)

Path("data/raw").mkdir(parents=True, exist_ok=True)
df.to_csv("data/raw/gatun_weather_daily.csv")

print(df.head())
print("\nRegistros:", len(df))
print("\nValores faltantes:")
print(df.isna().sum())
print("\nUnidades:", payload.get("parameters", {}))

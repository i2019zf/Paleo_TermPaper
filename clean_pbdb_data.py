import pandas as pd
import numpy as np

df = pd.read_csv("gabi_raw.csv", low_memory=False)
print(f"Records loaded: {len(df)}")

cols_needed = ["occurrence_no", "accepted_name", "lat", "lng",
               "max_ma", "min_ma", "early_interval"]
cols_needed = [c for c in cols_needed if c in df.columns]
df = df[cols_needed].copy()

before = len(df)
df = df.dropna(subset=["lat", "lng"])
print(f"Dropped {before - len(df)} rows with missing coordinates")

before = len(df)
df = df.dropna(subset=["max_ma", "min_ma"])
print(f"Dropped {before - len(df)} rows with missing age data")

df["mid_ma"] = (df["max_ma"] + df["min_ma"]) / 2

before = len(df)
df = df[(df["mid_ma"] >= 0.5) & (df["mid_ma"] <= 12)]
print(f"Dropped {before - len(df)} rows outside time window")

df["continent"] = np.where(df["lat"] >= 10, "North America", "South America")
print(f"\nContinent split:")
print(df["continent"].value_counts())

bins   = np.arange(0.5, 12.5, 1.0)
labels = np.arange(1.0, 12.0, 1.0)
df["time_bin"] = pd.cut(df["mid_ma"], bins=bins, labels=labels)
df["time_bin"] = df["time_bin"].astype(float)

print(f"\nRecords per time bin:")
print(df.groupby("time_bin")["occurrence_no"].count().to_string())

df.to_csv("gabi_clean.csv", index=False)
print(f"\nSaved gabi_clean.csv — {len(df)} records total")

print("\nSampling bias preview:")
bias = df.groupby(["time_bin", "continent"])["occurrence_no"].count().unstack(fill_value=0)
print(bias)

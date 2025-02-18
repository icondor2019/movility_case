import pandas as pd
import numpy as np
import pyarrow.parquet as pq
import h3


def process_parquet_in_chunks(file_path, batch_size):
    parquet_file = pq.ParquetFile(file_path)

    results = []

    # breakpoint()
    # Procesar por chunks
    for batch in parquet_file.iter_batches(batch_size):
        df = batch.to_pandas()  # Convertir batch a Pandas DataFrame
        df["hex_id"] = df.apply(lambda row: h3.latlng_to_cell(row["lat"], row["lon"], 8), axis=1)
        # df = raw_df.loc[raw_df['hex_id'].isin(hex_list)]
        df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")

        # Extraer la hora, día y semana ISO
        df["hour"] = df["datetime"].dt.hour
        df["day"] = df["datetime"].dt.day
        df['month'] = df["datetime"].dt.month
        df['week_day'] = df["datetime"].dt.day_name()
        df["iso_week"] = df["datetime"].dt.isocalendar().week
        df['holidays'] = np.where(df["iso_week"].isin([52, 1]), 1, 0)
        df['black_friday'] = np.where(df["iso_week"].isin([48]), 1, 0)
        # df['holyweek'] = np.where(df["iso_week"].isin([15, 16]), 1, 0)
        df['valentine'] = np.where((df["day"].isin([13, 14, 15]) & (df["month"].isin([2]))), 1, 0)
        df['mothers_day'] = np.where((df["day"].isin([11, 12, 13]) & (df["month"].isin([5]))), 1, 0)
        df['weekend'] = np.where(df["week_day"].isin(['Saturday', 'Sunday']), 1, 0)
        df['friday'] = np.where(df["week_day"].isin(['Friday']), 1, 0)
        df['night'] = np.where(df["hour"].isin([19, 20, 21, 22, 23]), 1, 0)
        df['friday_night'] = np.where((df["week_day"].isin(['Friday'])) & (df["hour"].isin([19, 20, 21, 22, 23])), 1, 0)

        summary = df.groupby(["hex_id"]).agg({"holidays": "sum", "black_friday": "sum",
                                            "valentine": "sum", "mothers_day": "sum", "weekend": "sum",
                                            "friday": "sum", "night": "sum", "friday_night": "sum",
                                            "device_id": "nunique"}).reset_index()
        results.append(summary)
        # break

    return pd.concat(results, ignore_index=True)

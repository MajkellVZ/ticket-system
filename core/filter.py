import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATA_URL = os.getenv("DATA_URL")
def load_data() -> pd.DataFrame:
    try:
        df = pd.read_csv(DATA_URL, parse_dates=['sys_created_on', 'sys_updated_on'])
        return df
    except Exception as e:
        print(f"An error occurred while trying to load the data: {e}")

def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    df_filtered = df.copy()

    if filters.get("priority"):
        df_filtered = df_filtered[df_filtered["priority"].isin(filters["priority"])]

    if filters.get("category"):
        df_filtered = df_filtered[df_filtered["category"].isin(filters["category"])]

    if filters.get("subcategory"):
        df_filtered = df_filtered[df_filtered["subcategory"].isin(filters["subcategory"])]

    if filters.get("assignment_group"):
        df_filtered = df_filtered[df_filtered["assignment_group"].isin(filters["assignment_group"])]

    if filters.get("state"):
        df_filtered = df_filtered[df_filtered["state"].isin(filters["state"])]

    if filters.get("created_range"):
        start, end = filters["created_range"]
        df_filtered = df_filtered[(df_filtered["sys_created_on"] >= start) & (df_filtered["sys_created_on"] <= end)]

    if filters.get("updated_range"):
        start, end = filters["updated_range"]
        df_filtered = df_filtered[(df_filtered["sys_updated_on"] >= start) & (df_filtered["sys_updated_on"] <= end)]

    return df_filtered


if __name__ == "__main__":
    print(load_data())
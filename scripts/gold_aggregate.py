import pandas as pd
from pathlib import Path

def run_gold_aggregate(**context):
    # Pull silver file path from XCom
    silver_file = context["ti"].xcom_pull(
        key="silver_file",
        task_ids="silver_transform"
    )

    if not silver_file:
        raise ValueError("No silver file found")

    # Read silver CSV
    df = pd.read_csv(silver_file)

    # Aggregate by origin_country
    agg = (
        df.groupby("origin_country")
        .agg(
            total_flights=("icao24", "count"),
            avg_velocity=("velocity", "mean"),
            on_ground=("geo_altitude", "sum"),
            #on_ground=("geo_altitude", lambda x: (x == 0).sum())

        )
        .reset_index()
    )

    # Save to gold layer
    gold_path = Path(silver_file.replace("silver", "gold"))
    agg.to_csv(gold_path, index=False)

    # Push gold file path to XCom for downstream tasks
    context["ti"].xcom_push(key="gold_file", value=str(gold_path))
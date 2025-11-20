# fetch_neo_data.py
import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from dotenv import load_dotenv

# Lataa .env-tiedoston asetukset
load_dotenv()

API_KEY = os.getenv("NASA_API_KEY")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME")

# Luo MySQL-engine mysqlconnectorilla
engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")

def fetch_neo_data():
    """Hakee NASA NEO API:n datan viime päivälle."""
    start_date = datetime.utcnow().date()
    end_date = start_date

    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={API_KEY}"
    print(f"Fetching data from NASA API: {url}")
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    neo_list = []
    for date_str, neos in data.get("near_earth_objects", {}).items():
        for neo in neos:
            for approach in neo.get("close_approach_data", []):
                neo_list.append({
                    "neo_id": neo.get("id"),
                    "name": neo.get("name"),
                    "diameter_min_km": neo.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_min"),
                    "diameter_max_km": neo.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_max"),
                    "velocity_km_s": float(approach.get("relative_velocity", {}).get("kilometers_per_second", 0)),
                    "miss_distance_km": float(approach.get("miss_distance", {}).get("kilometers", 0)),
                    "close_approach_date": pd.to_datetime(
                        approach.get("close_approach_date_full", approach.get("close_approach_date"))
                    ),
                    "is_hazardous": int(neo.get("is_potentially_hazardous_asteroid", False))
                })

    df = pd.DataFrame(neo_list)
    print(f"Fetched {len(df)} NEOs")
    return df

def save_to_db(df):
    """Tallentaa NEO-datan MySQL-tietokantaan."""
    if not df.empty:
        df.to_sql('neo_objects', con=engine, if_exists='append', index=False)
        print("Data saved to database")
    else:
        print("No new data to save")

if __name__ == "__main__":
    df = fetch_neo_data()
    save_to_db(df)

import argparse
import json
import os
from datetime import date, datetime

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CONGRESS_GOV_API_KEY")
BASE_URL = "https://api.congress.gov/v3"


def fetch_sponsored_legislation(bioguide_id):
    url = f"{BASE_URL}/member/{bioguide_id}/sponsored-legislation"
    params = {"api_key": API_KEY, "limit": 250}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def save_raw(candidate, filename, data, source_url):
    out_dir = os.path.join("data", "raw", candidate)
    os.makedirs(out_dir, exist_ok=True)

    data_path = os.path.join(out_dir, filename)
    with open(data_path, "w") as f:
        json.dump(data, f, indent=2)

    meta_path = os.path.join(out_dir, filename.replace(".json", ".meta.json"))
    with open(meta_path, "w") as f:
        json.dump(
            {"source_url": source_url, "retrieved_date": str(date.today())},
            f,
            indent=2,
        )

    print(f"Saved {data_path} and its .meta.json sidecar")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True, help="candidate slug, e.g. ossoff")
    parser.add_argument("--bioguide", required=True, help="bioguide ID, e.g. O000174")
    args = parser.parse_args()

    if not API_KEY:
        raise SystemExit("CONGRESS_GOV_API_KEY is not set in .env")

    data = fetch_sponsored_legislation(args.bioguide)
    source_url = f"{BASE_URL}/member/{args.bioguide}/sponsored-legislation"
    save_raw(args.candidate, "sponsored_legislation.json", data, source_url)


if __name__ == "__main__":
    main()
import argparse
import json
import os
from datetime import date

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOVINFO_API_KEY")
SEARCH_URL = "https://api.govinfo.gov/search"


def search_congressional_record(member_name, page_size=20):
    body = {
        "query": f'collection:CREC AND "{member_name}"',
        "pageSize": str(page_size),
        "offsetMark": "*",
        "sorts": [{"field": "score", "sortOrder": "DESC"}],
    }
    response = requests.post(
        SEARCH_URL,
        params={"api_key": API_KEY},
        json=body,
    )
    response.raise_for_status()
    return response.json()


def save_raw(candidate, data, source_query):
    out_dir = os.path.join("data", "raw", candidate)
    os.makedirs(out_dir, exist_ok=True)

    data_path = os.path.join(out_dir, "congressional_record_search.json")
    with open(data_path, "w") as f:
        json.dump(data, f, indent=2)

    meta_path = os.path.join(out_dir, "congressional_record_search.meta.json")
    with open(meta_path, "w") as f:
        json.dump(
            {
                "source_url": SEARCH_URL,
                "search_query": source_query,
                "retrieved_date": str(date.today()),
            },
            f,
            indent=2,
        )

    print(f"Saved {data_path} and its .meta.json sidecar")

def fetch_granule_text(txt_link):
    response = requests.get(txt_link, params={"api_key": API_KEY})
    response.raise_for_status()
    return response.text


def save_granule_text(candidate, granule_id, text, source_url):
    out_dir = os.path.join("data", "raw", candidate)
    os.makedirs(out_dir, exist_ok=True)

    filename = f"crec_{granule_id}.txt"
    data_path = os.path.join(out_dir, filename)
    with open(data_path, "w") as f:
        f.write(text)

    meta_path = os.path.join(out_dir, filename.replace(".txt", ".meta.json"))
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
    parser.add_argument("--member-name", help='exact name to search for, e.g. "Ossoff"')
    parser.add_argument("--granule-id", help="fetch full text for one specific granule from the last search")
    args = parser.parse_args()

    if not API_KEY:
        raise SystemExit("GOVINFO_API_KEY is not set in .env")

    if args.granule_id:
        search_path = os.path.join("data", "raw", args.candidate, "congressional_record_search.json")
        with open(search_path) as f:
            search_data = json.load(f)
        match = next((r for r in search_data["results"] if r["granuleId"] == args.granule_id), None)
        if not match:
            raise SystemExit(f"granuleId {args.granule_id} not found in saved search results")
        text = fetch_granule_text(match["download"]["txtLink"])
        save_granule_text(args.candidate, args.granule_id, text, match["download"]["txtLink"])
    elif args.member_name:
        data = search_congressional_record(args.member_name)
        query = f'collection:CREC AND "{args.member_name}"'
        save_raw(args.candidate, data, query)
    else:
        raise SystemExit("provide either --member-name (to search) or --granule-id (to fetch one result's text)")


if __name__ == "__main__":
    main()
import argparse
import json
import os
import re
from datetime import date

import requests


def strip_html(html):
    text = re.sub(r"<script.*?</script>", "", html, flags=re.DOTALL)
    text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_and_save(candidate, index, url):
    out_dir = os.path.join("data", "raw", candidate)
    os.makedirs(out_dir, exist_ok=True)

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )    
    response.raise_for_status()
    text = strip_html(response.text)

    filename = f"transcript_{index:02d}.txt"
    data_path = os.path.join(out_dir, filename)
    with open(data_path, "w") as f:
        f.write(text)

    meta_path = os.path.join(out_dir, filename.replace(".txt", ".meta.json"))
    with open(meta_path, "w") as f:
        json.dump(
            {"source_url": url, "retrieved_date": str(date.today())},
            f,
            indent=2,
        )

    print(f"Saved {data_path} and its .meta.json sidecar")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--urls", required=True, help="path to a text file, one URL per line")
    args = parser.parse_args()

    with open(args.urls) as f:
        urls = [line.strip() for line in f if line.strip()]

    for i, url in enumerate(urls, start=1):
        fetch_and_save(args.candidate, i, url)


if __name__ == "__main__":
    main()
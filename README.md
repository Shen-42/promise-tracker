# Promise Tracker

Tracks how often the top 10 candidates by Polymarket odds for the 2028 U.S. presidential election (frozen September 11, 2026) follow through on the specific, publicly documented promises they've made in their current or most recent electoral campaign.

Full rules for what counts as a promise, how statuses are assigned, and how confidence is reported are in METHODOLOGY.md — read that before the data.

## Setup

git clone <this repo>
cd promise-tracker
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

## Running the pipeline for one candidate

python scripts/fetch_congress.py --candidate ossoff
python scripts/fetch_transcripts.py --candidate ossoff --urls urls.txt
python scripts/extract.py --candidate ossoff
python scripts/validate_extraction.py --candidate ossoff
python scripts/dedupe.py --candidate ossoff
python scripts/validate_schema.py --candidate ossoff

## Contributing

See CONTRIBUTING.md for how to add sources or research a candidate.

## License

TBD

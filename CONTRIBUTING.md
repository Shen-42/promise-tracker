# Contributing

## Before you add a promise

Read METHODOLOGY.md in full, particularly:
- Section 2 (what counts as a promise) and Section 3 (atomicity)
- Section 4 (a promise needs a primary-source source_url, not a news paraphrase)
- Section 5 (status vocabulary - use only these values)

## Workflow

1. Create a branch named candidate/<name> for new research, or fix/<short-description> for corrections.
2. Add raw source documents to data/raw/<candidate>/ with a .meta.json sidecar recording source_url and retrieved_date.
3. Run the extraction and validation scripts (see README).
4. Open a pull request. CI runs validate_schema.py automatically - it must pass before merging.
5. If you're unsure whether an entry is atomic enough, or a status is genuinely ambiguous, open an Issue rather than guessing - tag it needs-review.

## Reporting a duplicate or disagreement

If two entries about the same promise conflict, work through the four-cause checklist in METHODOLOGY.md Section 9 before merging or splitting them, and note which cause applied in your commit message.

## What this project only uses

Public campaign statements, transcripts, bill text, and public FEC/Congress.gov records. Do not add anything sourced from private communications or unverified claims.

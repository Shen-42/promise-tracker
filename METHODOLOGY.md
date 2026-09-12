# Methodology

Last updated: 2026-09-12
Version: 0.1

## 1. Scope of candidates

Candidates tracked are the top 10 by implied probability on Polymarket's "Presidential Election Winner 2028" market, as of September 11, 2026, frozen at that date. The candidate list does not update as odds shift after this date; a new snapshot list constitutes a new version of this project, not a silent edit to this one.

As of the freeze date: JD Vance, Alexandria Ocasio-Cortez, Jon Ossoff, Marco Rubio, Gavin Newsom, Kamala Harris, Josh Shapiro, Pete Buttigieg, Donald Trump, Ron DeSantis.

## 2. What counts as a "promise"

A promise is a specific, discrete, publicly documented commitment made by the candidate - not a general value statement, not a prediction, not a criticism of an opponent. "I'll cut taxes for small businesses" qualifies; "the economy needs to be stronger" does not.

Since none of the ten have declared a 2028 candidacy, promises are drawn from each person's most recent or current electoral campaign for the office they hold. This is logged per candidate as campaign on each promise entry. If a person declares for 2028, their 2028 campaign promises become a new tracked set and do not merge with or replace the prior set.

## 3. Atomicity rule

One promise per entry, one discrete commitment per promise. A sentence bundling three commitments is split into three entries. Test before entering: can this promise resolve to a status independently of the sentence around it? If not, split further or discard.

## 4. Sourcing rule

Every promise requires:
- A source_url pointing to a primary source - campaign platform page, speech or debate transcript, bill text, official statement. A news article paraphrasing what a candidate "promised" is not an acceptable primary source.
- A date_made. If the primary source has no publish date, the entry is still included, with date_made set to null and a note flagging it as undated.

## 5. Status vocabulary

- not_yet_rated - default status for every new entry
- in_the_works - proposed, sponsored, or campaigned on, but not enacted
- stalled - no movement, due to opposition, gridlock, or shifted priorities
- compromise - a modified version of the promise was enacted
- promise_kept - the specific commitment was fulfilled, evidenced by a signed bill, enacted policy, or completed action
- promise_broken - the candidate explicitly abandoned or acted against the promise
- flagged_not_atomic - entry is too vague to ever resolve to a status as worded

Executives are held to actual signed or implemented outcomes for promise_kept. Legislators can be rated on sponsorship and votes even without passage.

## 6. Sample size and confidence reporting

Every published promise-kept percentage is a proportion, and its reliability depends on sample size in a specific, calculable way.

Applicability check: a normal approximation to a proportion is considered reasonable when n times p is at least 10 and n times (1-p) is at least 10, where p is the observed kept rate.

Interval method: confidence intervals use the Wilson score interval rather than the plain normal approximation.

Reporting thresholds:
- n under 10: publish the raw count only, no percentage
- n 10-29: publish the percentage with its Wilson interval, flagged as low-confidence
- n 30-59: publish the percentage with its Wilson interval, standard caveat
- n 60 or more: publish the percentage with its Wilson interval, no special caveat

No quota: there is no fixed target promise count per candidate.

## 7. Executive vs. legislator capacity weighting

Capacity is tracked as a separate, explicitly labeled field rather than blended into the headline kept/total percentage.

Tiers: President or Governor = weight 1.0 (Trump, DeSantis, Newsom, Shapiro). Cabinet Secretary = weight 0.6 (Rubio). Vice President = weight 0.5 (Vance). Senator = weight 0.3 (Ossoff). House member = weight 0.2 (AOC). No current office = weight 0.1 (Harris, Buttigieg).

These weights are a stated judgment call, not a statistically derived quantity.

## 8. Claim-matching for deduplication

The same promise often appears with different wording across sources. Before these are counted as separate entries, they are checked for duplication using TF-IDF vectorization compared by cosine similarity. Pairs at or above a 0.5 similarity threshold are flagged as likely duplicates and reviewed by a human before merging.

This threshold is adapted from Lee, Xiong, Seo and Lee (2023), see Section 13 References.

## 9. Resolving rating disagreements

Check for these causes, in order, before concluding a disagreement is genuine: status-vocabulary granularity, differing focus, similar but not identical commitments, and timing differences.

## 10. Known limitation: coverage will not match other trackers

This project's promise inventory for a given candidate is not expected to match what an independently-run tracker would compile for the same person.

## 11. Update and audit trail

Every status change is logged in the entry's status_history array. Prior status entries are never deleted, only appended to.

## 12. Changelog

- v0.1 (2026-09-12): Initial methodology. Candidate list frozen from Polymarket odds, September 11, 2026.

## 13. References

- Lee, S., Xiong, A., Seo, H., and Lee, D. (2023). Fact-checking fact checkers: A data-driven approach. Harvard Kennedy School Misinformation Review, 4(5).

# Football Analysis Search Engine

A lightweight football analysis search engine focused on:

- Europe's **major five domestic leagues**:
  - Premier League
  - La Liga
  - Bundesliga
  - Serie A
  - Ligue 1
- Major **UEFA tournaments**:
  - UEFA Champions League
  - UEFA Europa League
  - UEFA Europa Conference League

It returns the best match candidates for:

1. **Over 2.5 goals** probability
2. **Both Teams To Score (BTTS)** probability

## Run as a website

```bash
python3 app.py
```

Then open `http://127.0.0.1:5000`.

## Run the CLI script

```bash
python3 football_search_engine.py
```

## Programmatic usage

```python
from football_search_engine import search_matches, format_results

# Top UEFA-only matches with stricter thresholds
matches = search_matches(
    competition_query="UEFA",
    minimum_over_2_5=0.68,
    minimum_btts=0.62,
    limit=5,
)
print(format_results(matches))
```

## Tests

```bash
pytest -q
```

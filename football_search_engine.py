"""Football analysis search engine focused on Europe's top five leagues and UEFA tournaments.

The engine helps identify teams/matches with the strongest chances for:
- Over 2.5 total goals
- Both Teams To Score (BTTS)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

ALLOWED_COMPETITIONS = {
    "Premier League",
    "La Liga",
    "Bundesliga",
    "Serie A",
    "Ligue 1",
    "UEFA Champions League",
    "UEFA Europa League",
    "UEFA Europa Conference League",
}


@dataclass(frozen=True)
class MatchAnalysis:
    competition: str
    home_team: str
    away_team: str
    over_2_5_probability: float
    btts_probability: float

    @property
    def combined_score(self) -> float:
        """Simple ranking signal (higher means more attractive for both markets)."""
        return round((self.over_2_5_probability + self.btts_probability) / 2, 3)


# Curated sample dataset (0.0-1.0 probabilities)
MATCH_POOL: List[MatchAnalysis] = [
    MatchAnalysis("Premier League", "Manchester City", "Tottenham", 0.78, 0.67),
    MatchAnalysis("Premier League", "Liverpool", "Newcastle", 0.74, 0.64),
    MatchAnalysis("La Liga", "Barcelona", "Girona", 0.71, 0.61),
    MatchAnalysis("Bundesliga", "Bayern Munich", "Bayer Leverkusen", 0.8, 0.7),
    MatchAnalysis("Bundesliga", "Borussia Dortmund", "RB Leipzig", 0.76, 0.69),
    MatchAnalysis("Serie A", "Atalanta", "Inter", 0.73, 0.66),
    MatchAnalysis("Ligue 1", "PSG", "Monaco", 0.79, 0.71),
    MatchAnalysis("UEFA Champions League", "Real Madrid", "Manchester City", 0.72, 0.7),
    MatchAnalysis("UEFA Champions League", "Bayern Munich", "Arsenal", 0.69, 0.63),
    MatchAnalysis("UEFA Europa League", "Liverpool", "Atalanta", 0.7, 0.64),
    MatchAnalysis("UEFA Europa Conference League", "Fiorentina", "Aston Villa", 0.68, 0.62),
]


def search_matches(
    competition_query: str = "",
    minimum_over_2_5: float = 0.65,
    minimum_btts: float = 0.6,
    limit: int = 10,
    source: Iterable[MatchAnalysis] = MATCH_POOL,
) -> List[MatchAnalysis]:
    """Return top matches ranked by combined Over 2.5 + BTTS probabilities.

    - `competition_query`: optional partial text filter (e.g. "uefa", "bundesliga").
    - thresholds are inclusive and expected in 0..1 range.
    """
    normalized_query = competition_query.strip().lower()

    filtered: List[MatchAnalysis] = []
    for match in source:
        if match.competition not in ALLOWED_COMPETITIONS:
            continue

        if normalized_query and normalized_query not in match.competition.lower():
            continue

        if match.over_2_5_probability < minimum_over_2_5:
            continue

        if match.btts_probability < minimum_btts:
            continue

        filtered.append(match)

    filtered.sort(
        key=lambda m: (m.combined_score, m.over_2_5_probability, m.btts_probability),
        reverse=True,
    )
    return filtered[:limit]


def format_results(matches: Iterable[MatchAnalysis]) -> str:
    rows = [
        "Competition | Match | Over 2.5 | BTTS | Combined",
        "---|---|---:|---:|---:",
    ]
    for m in matches:
        rows.append(
            f"{m.competition} | {m.home_team} vs {m.away_team} | "
            f"{m.over_2_5_probability:.0%} | {m.btts_probability:.0%} | {m.combined_score:.0%}"
        )
    if len(rows) == 2:
        rows.append("No matches found for the selected filters.")
    return "\n".join(rows)


if __name__ == "__main__":
    # Example run: best matches across all allowed competitions.
    print("Top match candidates for Over 2.5 + BTTS markets:\n")
    print(format_results(search_matches()))

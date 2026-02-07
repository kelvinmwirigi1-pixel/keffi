from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from football_search_engine import ALLOWED_COMPETITIONS, MATCH_POOL, search_matches


def test_only_allowed_competitions_present():
    assert all(m.competition in ALLOWED_COMPETITIONS for m in MATCH_POOL)


def test_threshold_filters_are_applied():
    matches = search_matches(minimum_over_2_5=0.75, minimum_btts=0.69)
    assert matches
    assert all(m.over_2_5_probability >= 0.75 for m in matches)
    assert all(m.btts_probability >= 0.69 for m in matches)


def test_uefa_query_returns_only_uefa_competitions():
    matches = search_matches(competition_query="uefa")
    assert matches
    assert all("uefa" in m.competition.lower() for m in matches)

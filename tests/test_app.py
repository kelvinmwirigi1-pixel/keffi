from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import render_page


def test_index_page_renders_default_results():
    body = render_page()
    assert "Football Analysis Search Engine" in body
    assert "Bayern Munich vs Bayer Leverkusen" in body


def test_index_page_applies_filters_from_query_params():
    body = render_page(
        query="UEFA",
        minimum_over_2_5="70",
        minimum_btts="64",
        limit="2",
    )
    assert "UEFA Champions League" in body
    assert "PSG vs Monaco" not in body


def test_invalid_query_params_fallback_to_defaults():
    body = render_page(minimum_over_2_5="hello", minimum_btts="world", limit="-20")
    assert "Bayern Munich vs Bayer Leverkusen" in body

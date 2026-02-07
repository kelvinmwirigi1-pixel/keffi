from __future__ import annotations

from html import escape
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from football_search_engine import ALLOWED_COMPETITIONS, MatchAnalysis, search_matches


def _parse_percentage(value: str, default: float) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return default
    return min(max(numeric / 100, 0.0), 1.0)


def _parse_limit(value: str, default: int = 10) -> int:
    try:
        numeric = int(value)
    except (TypeError, ValueError):
        return default
    return min(max(numeric, 1), 50)


def _render_rows(results: list[MatchAnalysis]) -> str:
    if not results:
        return '<div class="empty">No matches found for the selected filters.</div>'

    rows = []
    for match in results:
        rows.append(
            "<tr>"
            f"<td>{escape(match.competition)}</td>"
            f"<td>{escape(match.home_team)} vs {escape(match.away_team)}</td>"
            f"<td class='number'>{match.over_2_5_probability * 100:.0f}%</td>"
            f"<td class='number'>{match.btts_probability * 100:.0f}%</td>"
            f"<td class='number'>{match.combined_score * 100:.0f}%</td>"
            "</tr>"
        )

    return """
    <table>
      <thead>
        <tr>
          <th>Competition</th>
          <th>Match</th>
          <th class="number">Over 2.5</th>
          <th class="number">BTTS</th>
          <th class="number">Combined</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
    """.format(rows="\n".join(rows))


def render_page(query: str = "", minimum_over_2_5: str = "65", minimum_btts: str = "60", limit: str = "10") -> str:
    minimum_over_2_5_value = _parse_percentage(minimum_over_2_5, default=0.65)
    minimum_btts_value = _parse_percentage(minimum_btts, default=0.6)
    limit_value = _parse_limit(limit)

    results = search_matches(
        competition_query=query,
        minimum_over_2_5=minimum_over_2_5_value,
        minimum_btts=minimum_btts_value,
        limit=limit_value,
    )

    options = "\n".join(
        f'<option value="{escape(competition)}"></option>'
        for competition in sorted(ALLOWED_COMPETITIONS)
    )

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Football Analysis Search Engine</title>
    <style>
      body {{ font-family: Inter, system-ui, sans-serif; margin: 2rem auto; max-width: 1000px; padding: 0 1rem 3rem; }}
      .subtitle {{ color: #555; }}
      form {{ display:grid; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); gap: 1rem; margin: 1.25rem 0 1.5rem; padding: 1rem; border:1px solid #d1d5db; border-radius:12px; }}
      label {{ display:block; font-size:.9rem; font-weight:600; margin-bottom:.4rem; }}
      input,button {{ width:100%; font-size:1rem; padding:.55rem .7rem; border:1px solid #9ca3af; border-radius:8px; }}
      button {{ background:#2563eb; color:#fff; font-weight:600; cursor:pointer; }}
      table {{ width:100%; border-collapse:collapse; }}
      th,td {{ text-align:left; border-bottom:1px solid #d1d5db; padding:.65rem .45rem; }}
      .number {{ text-align:right; }}
      .empty {{ padding:1rem; border-radius:8px; background:#f3f4f6; }}
    </style>
  </head>
  <body>
    <h1>Football Analysis Search Engine</h1>
    <p class="subtitle">Filter major European leagues and UEFA tournaments for Over 2.5 + BTTS opportunities.</p>

    <form method="get">
      <div>
        <label for="competition_query">Competition filter</label>
        <input id="competition_query" name="competition_query" type="text" list="competition-suggestions" value="{escape(query)}" placeholder="e.g. UEFA or Bundesliga" />
        <datalist id="competition-suggestions">{options}</datalist>
      </div>
      <div>
        <label for="minimum_over_2_5">Minimum Over 2.5 probability (%)</label>
        <input id="minimum_over_2_5" name="minimum_over_2_5" type="number" min="0" max="100" value="{round(minimum_over_2_5_value * 100)}" />
      </div>
      <div>
        <label for="minimum_btts">Minimum BTTS probability (%)</label>
        <input id="minimum_btts" name="minimum_btts" type="number" min="0" max="100" value="{round(minimum_btts_value * 100)}" />
      </div>
      <div>
        <label for="limit">Max results</label>
        <input id="limit" name="limit" type="number" min="1" max="50" value="{limit_value}" />
      </div>
      <div style="align-self:end"><button type="submit">Search matches</button></div>
    </form>

    {_render_rows(results)}
  </body>
</html>"""


def application(environ, start_response):
    params = parse_qs(environ.get("QUERY_STRING", ""))
    page = render_page(
        query=params.get("competition_query", [""])[0],
        minimum_over_2_5=params.get("minimum_over_2_5", ["65"])[0],
        minimum_btts=params.get("minimum_btts", ["60"])[0],
        limit=params.get("limit", ["10"])[0],
    )

    data = page.encode("utf-8")
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(data)))])
    return [data]


if __name__ == "__main__":
    with make_server("0.0.0.0", 5000, application) as server:
        print("Serving Football Analysis Search Engine at http://0.0.0.0:5000")
        server.serve_forever()

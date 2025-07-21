import requests

def fetch_player_stats(player_id, season_id=None, career=False):
    """
    Fetch stats for a player for a given season or career from the NHL API.
    Returns a dict of stats, or empty dict if not found.
    """
    if not player_id:
        return {}
    if career:
        url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
        resp = requests.get(url)
        if resp.status_code != 200:
            return {}
        data = resp.json()
        stats = data.get("featuredStats", {}).get("regularSeason", {})
        if stats and "career" in stats:
            career_stats = stats["career"]
            def to_int(val):
                try:
                    return int(val)
                except (TypeError, ValueError):
                    return 0
            return {
                "goals": to_int(career_stats.get("goals", 0)),
                "assists": to_int(career_stats.get("assists", 0)),
                "points": to_int(career_stats.get("points", 0))
            }
        return {}
    else:
        if not season_id:
            return {}
        url = f"https://api-web.nhle.com/v1/player/{player_id}/game-log/{season_id}/"
        resp = requests.get(url)
        if resp.status_code != 200:
            return {}
        data = resp.json()
        goals = assists = points = 0
        for game in data.get("gameLog", []):
            stats = game.get("stats", {})
            try:
                goals += int(stats.get("goals", 0) or 0)
            except (TypeError, ValueError):
                pass
            try:
                assists += int(stats.get("assists", 0) or 0)
            except (TypeError, ValueError):
                pass
            try:
                points += int(stats.get("points", 0) or 0)
            except (TypeError, ValueError):
                pass
        return {"goals": goals, "assists": assists, "points": points}

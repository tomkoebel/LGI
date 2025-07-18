
import random
import requests

def fetch_islanders_roster():
    """
    Fetch the current NHL team roster from the NHL API.
    Returns a list of dicts: { 'name': str, 'number': str, 'position': str }
    Accepts a team abbreviation (e.g., 'NYI'). If not provided, picks a random team.
    """
    def fetch_random_team_abbr():
        url = "https://api-web.nhle.com/v1/standings/now"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        teams = [team['teamAbbrev']['default'] for team in data.get('standings', []) if 'teamAbbrev' in team]
        return random.choice(teams) if teams else 'NYI'

    def _fetch_roster(team_abbr):
        url = f"https://api-web.nhle.com/v1/roster/{team_abbr}/current"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        players = []
        for group in [data.get("forwards", []), data.get("defensemen", []), data.get("goalies", [])]:
            for player in group:
                player_info = player.get("player", {})
                name = (
                    player_info.get("fullName")
                    or (player_info.get("firstName", {}).get("default") if isinstance(player_info.get("firstName"), dict) else player_info.get("firstName"))
                    or ""
                )
                last = (
                    player_info.get("lastName", {}).get("default") if isinstance(player_info.get("lastName"), dict) else player_info.get("lastName")
                )
                if last:
                    name = (name + " " + last).strip()
                if not name:
                    first = player.get("firstName", "")
                    last = player.get("lastName", "")
                    if isinstance(first, dict):
                        first = first.get("default", "")
                    if isinstance(last, dict):
                        last = last.get("default", "")
                    name = (first + " " + last).strip()
                name = name.strip() or "N/A"

                number = str(player.get("sweaterNumber", "N/A"))

                position = None
                if isinstance(player_info.get("position"), dict):
                    position = player_info["position"].get("name")
                if not position and isinstance(player.get("position"), dict):
                    position = player["position"].get("name")
                if not position and player.get("position"):
                    position = player["position"]
                if not position:
                    if group is data.get("forwards", []):
                        position = "Forward"
                    elif group is data.get("defensemen", []):
                        position = "Defenseman"
                    elif group is data.get("goalies", []):
                        position = "Goalie"
                position = position or "N/A"
                player_id = None
                if "id" in player_info:
                    player_id = player_info["id"]
                elif "id" in player:
                    player_id = player["id"]
                players.append({
                    "name": name,
                    "number": number,
                    "position": position,
                    "id": player_id
                })
        print(f"Found {len(players)} players for {team_abbr} in API response.")
        return players

    def fetch_roster(team_abbr=None):
        if not team_abbr:
            team_abbr = fetch_random_team_abbr()
        return _fetch_roster(team_abbr)

    return fetch_roster

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

def get_random_player(team_abbr=None):
    """
    Return a random player (name, number, position) from the given team's current roster.
    If no team_abbr is provided, picks a random team.
    """
    fetch_roster = fetch_islanders_roster()
    roster = fetch_roster(team_abbr)
    if not roster:
        print("No players found in the API response. Returning None.")
        return None
    player = random.choice(roster)
    player_id = player.get("id")
    from datetime import datetime
    current_year = datetime.now().year
    prev_season = f"{current_year-2}{current_year-1}" if datetime.now().month < 9 else f"{current_year-1}{current_year}"
    if player_id:
        player["previous_season_stats"] = fetch_player_stats(player_id, prev_season)
        player["career_stats"] = fetch_player_stats(player_id, career=True)
    else:
        player["previous_season_stats"] = {}
        player["career_stats"] = {}
    return player

def get_random_players(n=1, team_abbr=None):
    """
    Return a list of n unique random players (name, number, position) from the given team's current roster.
    If no team_abbr is provided, picks a random team.
    """
    fetch_roster = fetch_islanders_roster()
    roster = fetch_roster(team_abbr)
    if not roster:
        return []
    return random.sample(roster, k=min(n, len(roster)))

if __name__ == "__main__":
    player = get_random_player()  # random team
    if player:
        print("Random NHL Player:")
        print(f"  Name: {player['name']}")
        print(f"  Number: {player['number']}")
        print(f"  Position: {player['position']}")
        if player.get('previous_season_stats'):
            stats = player['previous_season_stats']
            print(f"  Games Played: {stats.get('gamesPlayed', 0)}")
            print(f"  Previous Season: {stats.get('goals', 0)} G, {stats.get('assists', 0)} A, {stats.get('points', 0)} PTS")
        if player.get('career_stats'):
            stats = player['career_stats']
            print(f"  Career: {stats.get('goals', 0)} G, {stats.get('assists', 0)} A, {stats.get('points', 0)} PTS")
    else:
        print("No NHL player found.")
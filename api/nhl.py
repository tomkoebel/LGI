import random
import requests
from datetime import datetime
from api.stats import fetch_player_stats

def fetch_random_team_abbr():
    url = "https://api-web.nhle.com/v1/standings/now"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    teams = [team['teamAbbrev']['default'] for team in data.get('standings', []) if 'teamAbbrev' in team]
    return random.choice(teams) if teams else 'NYI'

def get_team_logo(team_abbr):
    return f"https://assets.nhle.com/logos/nhl/svg/{team_abbr}_light.svg"

def fetch_roster(team_abbr=None):
    if not team_abbr:
        team_abbr = fetch_random_team_abbr()
    url = f"https://api-web.nhle.com/v1/roster/{team_abbr}/current"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    players = []
    team_logo = get_team_logo(team_abbr)
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
            image_url = None
            if player_id:
                image_url = f"https://nhl.bamcontent.com/images/headshots/current/168x168/{player_id}.jpg"
            players.append({
                "name": name,
                "number": number,
                "position": position,
                "id": player_id,
                "image_url": image_url,
                "team_abbr": team_abbr,
                "team_logo": team_logo
            })
    return players


def get_random_player(team_abbr=None):
    roster = fetch_roster(team_abbr)
    if not roster:
        return None
    player = random.choice(roster)
    player_id = player.get("id")
    current_year = datetime.now().year
    prev_season = f"{current_year-2}{current_year-1}" if datetime.now().month < 9 else f"{current_year-1}{current_year}"
    if player_id:
        player["previous_season_stats"] = fetch_player_stats(player_id, prev_season)
        player["career_stats"] = fetch_player_stats(player_id, career=True)
        player["image_url"] = f"https://nhl.bamcontent.com/images/headshots/current/168x168/{player_id}.jpg"
    else:
        player["previous_season_stats"] = {}
        player["career_stats"] = {}
        player["image_url"] = None
    return player

def compare_random_players(team_abbr=None):
    roster = fetch_roster(team_abbr)
    if not roster or len(roster) < 2:
        return None, None
    player1, player2 = random.sample(roster, 2)
    for player in (player1, player2):
        player_id = player.get("id")
        current_year = datetime.now().year
        prev_season = f"{current_year-2}{current_year-1}" if datetime.now().month < 9 else f"{current_year-1}{current_year}"
        if player_id:
            player["previous_season_stats"] = fetch_player_stats(player_id, prev_season)
            player["career_stats"] = fetch_player_stats(player_id, career=True)
            player["image_url"] = f"https://nhl.bamcontent.com/images/headshots/current/168x168/{player_id}.jpg"
        else:
            player["previous_season_stats"] = {}
            player["career_stats"] = {}
            player["image_url"] = None
    return player1, player2

def get_random_players(n=1, team_abbr=None):
    roster = fetch_roster(team_abbr)
    if not roster:
        return []
    return random.sample(roster, k=min(n, len(roster)))

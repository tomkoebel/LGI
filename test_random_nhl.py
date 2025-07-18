import pytest
import importlib.util
import sys
import os

# Dynamically import random-isles.py as a module
spec = importlib.util.spec_from_file_location("random_nhl", os.path.join(os.path.dirname(__file__), "random-nhl.py"))
if spec is None or spec.loader is None:
    raise ImportError("Could not load random-nhl.py module spec")
random_nhl = importlib.util.module_from_spec(spec)
sys.modules["random_nhl"] = random_nhl
spec.loader.exec_module(random_nhl)

def test_fetch_roster_returns_players():
    print("Running test_fetch_roster_returns_players...")
    fetch_roster = random_nhl.fetch_islanders_roster()
    teams = ['NYI', 'TOR', 'BOS', 'CHI', 'VGK', None]  # None triggers random team
    for team in teams:
        players = fetch_roster(team)
        label = team if team else 'random'
        print(f"Fetched {len(players)} players for {label}")
        assert isinstance(players, list)
        assert len(players) > 0
        assert all('name' in p and 'number' in p and 'position' in p for p in players)

def test_fetch_roster_random_team():
    print("Running test_fetch_roster_random_team...")
    fetch_roster = random_nhl.fetch_islanders_roster()
    players = fetch_roster(None)  # None triggers random team
    print(f"Fetched {len(players)} players for a random team")
    assert isinstance(players, list)
    assert len(players) > 0

def test_get_random_player():
    print("Running test_get_random_player...")
    teams = ['NYI', 'TOR', 'BOS', 'CHI', 'VGK', None]
    for team in teams:
        player = random_nhl.get_random_player(team)
        team_label = team if team else 'random team'
        print(f"Random {team_label} player: {player['name']} #{player['number']} ({player['position']})")
        assert player is not None
        assert 'name' in player and 'number' in player and 'position' in player

def test_get_random_players():
    print("Running test_get_random_players...")
    teams = ['NYI', 'TOR', 'BOS', 'CHI', 'VGK', None]
    for team in teams:
        players = random_nhl.get_random_players(3, team)
        team_label = team if team else 'random team'
        print(f"Random {team_label} players:")
        for p in players:
            print(f"  {p['name']} #{p['number']} ({p['position']})")
        assert isinstance(players, list)
        assert len(players) == 3
        assert all('name' in p and 'number' in p and 'position' in p for p in players)

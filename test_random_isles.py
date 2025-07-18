import pytest
import importlib.util
import sys
import os

# Dynamically import random-isles.py as a module
spec = importlib.util.spec_from_file_location("random_isles", os.path.join(os.path.dirname(__file__), "random-isles.py"))
if spec is None or spec.loader is None:
    raise ImportError("Could not load random-isles.py module spec")
random_isles = importlib.util.module_from_spec(spec)
sys.modules["random_isles"] = random_isles
spec.loader.exec_module(random_isles)

def test_fetch_roster_returns_players():
    fetch_roster = random_isles.fetch_islanders_roster()
    players = fetch_roster('NYI')
    assert isinstance(players, list)
    assert len(players) > 0
    assert all('name' in p and 'number' in p and 'position' in p for p in players)

def test_fetch_roster_random_team():
    fetch_roster = random_isles.fetch_islanders_roster()
    players = fetch_roster()
    assert isinstance(players, list)
    assert len(players) > 0

def test_get_random_player():
    player = random_isles.get_random_player('NYI')
    assert player is not None
    assert 'name' in player and 'number' in player and 'position' in player

def test_get_random_players():
    players = random_isles.get_random_players(3, 'NYI')
    assert isinstance(players, list)
    assert len(players) == 3
    assert all('name' in p and 'number' in p and 'position' in p for p in players)

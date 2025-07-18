
# NHL Random Player Selector

A Python script that fetches the current roster for any NHL team from the official NHL API and randomly selects a player, displaying their name, jersey number, position, previous season stats, and career stats (if available). You can specify a team abbreviation (e.g., 'NYI', 'TOR', 'BOS'), or let the script pick a random team for you.

## Features
- Retrieves the current roster for any NHL team from the NHL API
- Selects and displays a random player’s name, number, and position
- Fetches previous season and career stats for each player (if available)
- Supports selecting one or multiple random players
- Can select a random team if none is specified

## Requirements
- Python 3.7 or higher
- `requests` library (`pip install requests`)

## Usage

Run the script from the command line:

```bash
python random-isles.py
```

You can also use the functions in your own code:

```python
from random_isles import get_random_player, get_random_players

# Get a random player from a specific team (e.g., Toronto Maple Leafs)
player = get_random_player('TOR')

# Get a random player from a random team
player = get_random_player()

# Get 3 random players from the Boston Bruins
players = get_random_players(3, 'BOS')
```

### Example output:
Random NHL Player:
  Name: Mathew Barzal
  Number: 13
  Position: Center
  Previous Season: 23 G, 40 A, 63 PTS
  Career: 113 G, 306 A, 419 PTS

## Notes
- The script uses the endpoint `https://api-web.nhle.com/v1/roster/{TEAM_ABBR}/current` for the current roster, where `TEAM_ABBR` is the team abbreviation (e.g., 'NYI', 'TOR').
- Player stats are fetched from the NHL API if a player ID is available.
- If the API structure changes, you may need to update the extraction logic in `fetch_islanders_roster()`.
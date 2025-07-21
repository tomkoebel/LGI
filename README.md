# NHL Random Player Selector

This Python script fetches the current roster for any NHL team from the official NHL API and randomly selects a player, displaying their name, jersey number, position, previous season stats, and career stats (if available). You can specify a team abbreviation (e.g., 'NYI', 'TOR', 'BOS'), or let the script pick a random team for you. The script is robust, supports both command-line and programmatic use, and is tested for all NHL teams.

## Features

- Retrieves the current roster for any NHL team from the NHL API
- Selects and displays a random player’s name, number, and position
- Fetches previous season and career stats for each player (if available)
- Supports selecting one or multiple random players
- Can select a random team if none is specified
- Handles API changes and missing data gracefully

## Requirements

- Python 3.7 or higher
- `requests` library (`pip install requests`)

## Usage

### Command Line

Run the script from the command line:

```bash
python random-nhl.py
```

This will print a random player from a random NHL team, including their name, number, position, and stats if available.

### Programmatic Usage

You can also use the functions in your own code:

```python
from random_nhl import get_random_player, get_random_players

# Get a random player from a specific team (e.g., Toronto Maple Leafs)
player = get_random_player('TOR')
print(player)

# Get a random player from a random team
player = get_random_player()
print(player)

# Get 3 random players from the Boston Bruins
players = get_random_players(3, 'BOS')
for p in players:
    print(p)
```

### Example Output

```text
Random NHL Player:
  Name: Mathew Barzal
  Number: 13
  Position: Center
  Previous Season: 23 G, 40 A, 63 PTS
  Career: 113 G, 306 A, 419 PTS
```

Or, as a dictionary (when used programmatically):

```python
{
  'name': 'Mathew Barzal',
  'number': '13',
  'position': 'Center',
  'id': 8478445,
  'previous_season_stats': {'goals': 23, 'assists': 40, 'points': 63},
  'career_stats': {'goals': 113, 'assists': 306, 'points': 419}
}
```

## Team Abbreviations

You can use any valid NHL team abbreviation (e.g., 'NYI', 'TOR', 'BOS', 'CHI', 'VGK', etc.). If you pass `None` or omit the argument, a random team will be selected.

## Output Details

- The script prints player info to the console when run directly.
- When used as a module, functions return dictionaries with player info and stats.
- If stats are not available, the relevant fields will be empty or zero.

## Error Handling & Troubleshooting

- If the NHL API is unavailable or the team abbreviation is invalid, the script will print an error or return an empty list.
- If the API structure changes, you may need to update the extraction logic in `fetch_islanders_roster()`.
- For best results, ensure you have a stable internet connection.

## API Endpoints Used

- Roster: `https://api-web.nhle.com/v1/roster/{TEAM_ABBR}/current`
- Standings (for random team): `https://api-web.nhle.com/v1/standings/now`
- Player stats: `https://api-web.nhle.com/v1/player/{player_id}/landing` and `https://api-web.nhle.com/v1/player/{player_id}/game-log/{season_id}/`

## Testing

Automated tests are provided in `test_random_nhl.py` and cover:

- Fetching rosters for specific and random teams
- Fetching random players for specific and random teams
- Ensuring all returned player dicts have the expected fields

Run tests with:

```bash
pytest -s test_random_nhl.py
```

## Flask Web App

This project includes a Flask web server that provides a user-friendly interface for viewing random NHL players and comparing two players from any team.

### Features
- Displays a random NHL player with headshot, team logo, name, number, position, previous season stats, and career stats.
- Allows comparison of two random players from the same team.
- Team logo is shown above the player's name using the official NHL SVG logo.
- Handles missing images and stats gracefully.

### How to Start the Server

1. **Install dependencies (in your virtual environment):**
   ```sh
   pip install flask requests
   ```
2. **Start the Flask server:**
   ```sh
   python3 app.py
   ```
   By default, the server runs on `http://127.0.0.1:5050`.

### What the HTML Does
- `templates/player.html`: Shows a random NHL player, their team logo, headshot, and stats. The team logo appears above the player's name.
- `templates/compare.html`: Shows two random players side-by-side for comparison, including their team logos, headshots, and stats.
- The UI is simple and modern, with images and stats clearly displayed.

### Example
Visit `http://127.0.0.1:5050` in your browser to view a random player. Click "Compare Two Players" to see a side-by-side comparison.

---

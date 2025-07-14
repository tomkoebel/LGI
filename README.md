# NY Islanders Random Player Selector

This Python script fetches the current New York Islanders roster from the official NHL API and allows you to randomly select a player, including their name, jersey number, position, previous season stats, and career stats (if available).

## Features
- Fetches the current Islanders roster from the NHL API
- Returns a random player with name, number, and position
- Attempts to fetch previous season and career stats for each player
- Includes functions to get one or multiple random Islanders

## Requirements
- Python 3.7+
- `requests` library (install with `pip install requests`)

## Usage
Run the script from the command line:

```bash
python isles.py
```

You will see output like:

```
Random NY Islander: {'name': 'Mathew Barzal', 'number': '13', 'position': 'Center', 'previous_season_stats': {...}, 'career_stats': {...}}
```

## Notes
- The script uses the endpoint `https://api-web.nhle.com/v1/roster/NYI/current` for the current roster.
- Player stats are fetched from the NHL API if a player ID is available.
- If the API structure changes, you may need to update the extraction logic in `fetch_islanders_roster()`.

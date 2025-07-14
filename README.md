# NY Islanders Random Player Selector

A Python script that fetches the current New York Islanders roster from the official NHL API and randomly selects a player, displaying their name, jersey number, position, previous season stats, and career stats (if available).

## Features
- Retrieves the current Islanders roster from the NHL API
- Selects and displays a random player’s name, number, and position
- Fetches previous season and career stats for each player (if available)
- Supports selecting one or multiple random players

## Requirements
- Python 3.7 or higher
- `requests` library (`pip install requests`)

## Usage

Run the script from the command line:

```bash
python isles.py
```

### Example output:
Random NY Islander:
  Name: Mathew Barzal
  Number: 13
  Position: Center
  Previous Season: 23 G, 40 A, 63 PTS
  Career: 113 G, 306 A, 419 PTS

## Notes
- The script uses the endpoint `https://api-web.nhle.com/v1/roster/NYI/current` for the current roster.
- Player stats are fetched from the NHL API if a player ID is available.
- If the API structure changes, you may need to update the extraction logic in `fetch_islanders_roster()`.
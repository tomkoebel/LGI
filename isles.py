from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/random-islander", methods=["GET"])
def api_random_islander():
    player = get_random_islander()
    if not player:
        return jsonify({"error": "No Islanders player found."}), 404
    # Remove None values and internal keys
    player = {k: v for k, v in player.items() if v is not None and k != 'id'}
    return jsonify(player)
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        app.run(debug=True)
    else:
        player = get_random_islander()
        if player:
            print("Random NY Islander:")
            print(f"  Name: {player['name']}")
            print(f"  Number: {player['number']}")
            print(f"  Position: {player['position']}")
            if player.get('previous_season_stats'):
                stats = player['previous_season_stats']
                print(f"  Previous Season: {stats.get('goals', 0)} G, {stats.get('assists', 0)} A, {stats.get('points', 0)} PTS")
            if player.get('career_stats'):
                stats = player['career_stats']
                print(f"  Career: {stats.get('goals', 0)} G, {stats.get('assists', 0)} A, {stats.get('points', 0)} PTS")
        else:
            print("No Islanders player found.")

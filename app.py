from flask import Flask, render_template, request, jsonify
import random_nhl

app = Flask(__name__)

@app.route('/')
def home():
    player = random_nhl.get_random_player()
    return render_template('player.html', player=player)

@app.route('/compare')
def compare():
    p1, p2 = random_nhl.compare_random_players()
    return render_template('compare.html', player1=p1, player2=p2)

@app.route('/api/player')
def api_player():
    team = request.args.get('team')
    player = random_nhl.get_random_player(team)
    return jsonify(player)

@app.route('/api/compare')
def api_compare():
    team = request.args.get('team')
    p1, p2 = random_nhl.compare_random_players(team)
    return jsonify({'player1': p1, 'player2': p2})

if __name__ == '__main__':
    app.run(debug=True)

from api import db, app
from api.models import User, Tournament, TournamentPlayers, Matches
from flask import jsonify, request, json, current_app, g

@app.route('/bracket-api/tournament/create', methods=['POST'])
def create_tournament():
  data = request.get_json() or {}
  if 'bracket' not in data:
    return jsonify({'error': 'Something went wrong.'}), 400
  if 'tournamentName' not in data:
    return jsonify({'error': 'Must include a name.'}), 400
  if 'round' not in data:
    return jsonify({'error': 'Must include a round.'}), 400

  tournament = Tournament(tournament_title=data['tournamentName'])


  # #add players
  players = []
  
  for p in data['bracket']:
    players.append(p['playerOne'])
    players.append(p['playerTwo'])
    tournament.players = (TournamentPlayers(player_name=person) for person in players)
    #tournament.players = (TournamentPlayers(player_name=person['playerOne'])for person in players)
    #tournament.players = (TournamentPlayers(player_name=person['playerTwo'])for person in players)
  #playersList = players.values()
  db.session.add(tournament)
  db.session.commit()
  return jsonify({'test': players})
  #return jsonify({'test': data['bracket']})
  #return jsonify({'test': data['round']})

@app.route('/bracket-api/tournament/getTourn', methods=['GET'])
def get_tourns():
  tournaments = Tournament.query.all()
  tournaments = Tournament.query.get(10)
  return jsonify({'tourns': tournaments.to_dict()})
  #return jsonify({'tourns': [t.to_dict() for t in tournaments]})
  #return jsonify({'test': 'worked'})

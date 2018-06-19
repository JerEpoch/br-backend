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
  players, matches = [], []
  for p in data['bracket']:
    players.append(p['playerOne'])
    players.append(p['playerTwo'])
    tournament.players = (TournamentPlayers(player_name=person) for person in players)
    #tournament.matches = [Matches(round=1, player_one=p['playerOne'], player_two=p['playerTwo'])]
  
  for p in data['bracket']:
    match = [Matches(round=1, player_one=p['playerOne'], player_two=p['playerTwo'])]
    tournament.matches.extend(match)
  
 
    #matches.append(tournament)
    #tournament.players = (TournamentPlayers(player_name=person['playerOne'])for person in players)
  #tournament.matches = (Matches(round=data['round']))

  #round = Matches(round=data['round'])
  #round=data['round']
  #tournament.matches.round = round
  #playersList = players.values()
  db.session.add(tournament)
  db.session.commit()
  return jsonify({'test': players}), 200
  #return jsonify({'test': data['bracket']})
  #return jsonify({'test': data['round']})

@app.route('/bracket-api/tournament/getAllTournaments', methods=['GET'])
def get_tourns():
  #tournaments = Tournament.query.all()
  #tournaments = Tournament.query.get(10)
  tournaments = Tournament.query.filter_by(is_completed=False)
  #return jsonify({'tourns': tournaments.to_dict()})
  return jsonify({'tourns': [t.to_dict() for t in tournaments]})

@app.route('/bracket-api/tournament/<int:id>/', methods=['GET'])
def get_tournament(id):
  tournament = Tournament.query.get(id)

  return jsonify({'tournament': tournament.to_dict()})

@app.route('/bracket-api/tournament', methods=["POST"])
def set_match_winner():
  data = request.get_json() or {}


  tournamentId = data["tournamentId"]
  round = data["round"]
  tournament = Tournament.query.get(tournamentId)
  match = tournament.matches
  print(match[0].round)
  # match_round = match.round
  # print(match_round)
  
  #print(match)

  for match in tournament.matches:
    print(match.round)
 
  return jsonify({'data': data})
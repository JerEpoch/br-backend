#from api import db, app
from api.main import bp
from api.models import User, Tournament, TournamentPlayers, Matches
from flask import jsonify, request, json, current_app, g
from flask_jwt_extended import get_jwt_identity, jwt_required

@bp.route('/bracket-api/tournament/create', methods=['POST'])
@jwt_required
def create_tournament():
  data = request.get_json() or {}

  current_user = get_jwt_identity()
  user = User.query.filter_by(username=current_user).first()
  #print(user.id)
  #return jsonify({'data': user})
  if not user:
    return jsonify({'error': 'Invalid creditentials'}), 401

  if 'bracket' not in data:
    return jsonify({'error': 'Something went wrong.'}), 400
  if 'tournamentName' not in data:
    return jsonify({'error': 'Must include a name.'}), 400
  if 'round' not in data:
    return jsonify({'error': 'Must include a round.'}), 400

  tournament = Tournament(tournament_title=data['tournamentName'])
  title = 'Round ' + str(data['round'])
  tournament.user_id = user.id
  # #add players
  players = []
  for p in data['bracket']:
    players.append(p['playerOne'])
    players.append(p['playerTwo'])
    tournament.players = (TournamentPlayers(player_name=person) for person in players)
    #tournament.matches = [Matches(round=1, player_one=p['playerOne'], player_two=p['playerTwo'])]
  
  for p in data['bracket']:
    match = [Matches(round=1, title=title, player_one=p['playerOne'], player_two=p['playerTwo'])]
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
  return jsonify({'data': tournament.to_dict()}), 200
  #return jsonify({'test': data['bracket']})
  #return jsonify({'test': data['round']})

@bp.route('/bracket-api/tournament/getAllTournaments', methods=['GET'])
def get_tourns():
  #tournaments = Tournament.query.all()
  #tournaments = Tournament.query.get(10)
  tournaments = Tournament.query.filter_by(is_completed=False)
  completedTournaments = Tournament.query.filter_by(is_completed=True)
  #return jsonify({'tourns': tournaments.to_dict()})
  return jsonify({'tourns': [t.to_dict() for t in tournaments], 'completedTourns': [t.to_dict() for t in completedTournaments]})

# @app.route('/bracket-api/tournament/<int:id>/<int:round>', methods=['GET'])
# def get_match_round(id, round):
#   pass

@bp.route('/bracket-api/tournament/<int:id>/', methods=['GET'])
def get_tournament(id):
  tournament = Tournament.query.get(id)
  # for match in tournament.matches:
  #   print(match.round)

  return jsonify({'tournament': tournament.to_dict()})

@bp.route('/bracket-api/tournament/tournadmin/<int:id>/', methods=['GET'])
@jwt_required
def check_tourn_admin(id):
  current_user = get_jwt_identity()
  user = User.query.filter_by(username=current_user).first()

  if not user:
    return jsonify({'error': 'User not found. Please login or signup.'})
  
  tournament = Tournament.query.get(id)
  if tournament.user_id != user.id:
    return jsonify({'data': False})
  else:
    return jsonify({'data': True})
  
  return jsonify({'error': 'There was a problem getting information.'})

@bp.route('/bracket-api/tournament', methods=["POST"])
@jwt_required
def set_match_winner():
  data = request.get_json() or {}
  # check for errors in info
  if 'players' not in data:
    return jsonify({'error': 'Something went wrong. Players for match not found.'}), 400
  if 'round' not in data:
    return jsonify({'error': 'Something went. Match round was not found.'}), 400
  if 'tournamentId' not in data:
    return jsonify({'error': 'Something went. Tournament ID was not found.'}), 400



  tournamentId = data["tournamentId"]
  round = data["round"]
  title = 'Round ' + str(round)
  tournament = Tournament.query.get(tournamentId)

  for match in tournament.matches:
    match.round_completed = True


  if data["finalMatch"]:
    match = [Matches(round=round, title='Winner', player_one=data['players'][0]['playerOne'])]
    tournament.matches.extend(match)
    tournament.is_completed=True
    
  else:
    for p in data["players"]:
      match = [Matches(round=round, title=title, player_one=p['playerOne'], player_two=p['playerTwo'])]
      tournament.matches.extend(match)

 
  #db.session.add(tournament)
  db.session.commit()



  # match_round = match.round
  # print(match_round)
  #check_tourn = Tournament.query.get(tournamentId)
  #print(match)
  #return jsonify({'data': data['players'][0]['playerOne']})
  return jsonify({'data': tournament.to_dict()})


# @bp.route('/bracket-api/api')
# def api():
#     return json.dumps({"msg": "hello from api"})
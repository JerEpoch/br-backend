from api.main import bp
from api import db
from api.models import MemberNewsPost, User
from flask import jsonify, request, json, current_app, g
from flask_jwt_extended import get_jwt_identity, jwt_required

@bp.route('/bracket-api/communitynews/newpost', methods=['POST', 'GET'])
@jwt_required
def create_newsPost():
  data = request.get_json() or {}

  if 'news_title' not in data or not data['news_title']:
    return jsonify({'error': 'You did not include a title for your news post. Please correct and submit again.'}), 400
  if 'news_post' not in data or not data['news_post']:
    return jsonify({'error': 'You did not include a body for your news post. Please correct and submit again.'}), 400

  newsPost = MemberNewsPost()
  current_user = get_jwt_identity()
  if current_user:
    try:
      user = User.query.filter_by(username=current_user).first()
      newsPost.user_id = user.id
      newsPost.from_dict(data)
      db.session.add(newsPost)
      db.session.commit()
      return jsonify({'data': 'added post'})
    except:
      return jsonify({'error': 'Something went wrong with adding your news post.'}), 400
  else:
    return jsonify({'error': 'No current user.'})

  #return jsonify({'data': data})


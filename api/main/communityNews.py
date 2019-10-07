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
      newsPost.user = user.username
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


@bp.route('/bracket-api/communitynews/getnewsposts', methods=['GET'])
def get_allNewsPosts():
  #pagination stuff
  page = request.args.get('page', 1, type=int)
  #paged_news = MemberNewsPost.query.paginate(page, current_app.config['POSTS_PER_PAGE'], False).items
  paged_news = MemberNewsPost.query.order_by(MemberNewsPost.publish_date.desc()).filter_by(is_announcement = False).paginate(page, current_app.config['POSTS_PER_PAGE'], False).items
  test_news  = MemberNewsPost.query.order_by(MemberNewsPost.publish_date.desc()).filter_by(is_announcement = False).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
  test_thing = [t.to_dict() for t in test_news.items]
  #pNews = [p.to_dict() for p in paged_news]
  next_url = test_news.next_num if test_news.has_next else None
  total_pages = test_news.total
  #pnews = json.dumps({'paged': paged_news})
  # for pageNews in paged_news.items:
  #   p_news
  #end pagination stuff
  #allNewsPosts = MemberNewsPost.query.order_by(MemberNewsPost.publish_date.desc()).filter_by(is_announcement = False)
  # payload = {'data': [n.to_dict() for n in allNewsPosts], 'pageData': pNews}
  # return jsonify(payload)
  #return jsonify({'data': [n.to_dict() for n in allNewsPosts]}, {'pageData': pNews})
  payload = {'data': test_thing, 'nextUrl': next_url, 'totalPages': total_pages, 'page_sent': page, 'postsPerPage': current_app.config['POSTS_PER_PAGE']}
  return jsonify(payload)

@bp.route('/bracket-api/communitynews/getnewspost/<int:id>', methods=['GET'])
def get_newspost(id):
  news_post = MemberNewsPost.query.get(id)
  return jsonify({'data': news_post.to_dict()})

@bp.route('/bracket-api/communitynews/getannouncements', methods=['GET'])
def get_announcements():
  announcements = MemberNewsPost.query.order_by(MemberNewsPost.publish_date.desc()).filter_by(is_announcement = True).limit(5)
  return jsonify({'data': [a.to_dict() for a in announcements]})

@bp.route('/bracket-api/communitynews/deletepost')
def delete_posts():
  posts = MemberNewsPost.query.all()
  for p in posts:
    db.session.delete(p)
    db.session.commit()

  posts = MemberNewsPost.query.all()
  return jsonify({'data': posts})

#https://stackoverflow.com/questions/33705697/alembic-integrityerror-column-contains-null-values-when-adding-non-nullable

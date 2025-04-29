from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User
from app.middleware import role_required

bp = Blueprint('speakers', __name__, url_prefix='/speakers')

@bp.route('/profile', methods=['POST'])
@jwt_required()
@role_required('speaker')
def update_profile():
    user_id = get_jwt_identity()
    data = request.json
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    user.expertise = data.get('expertise', user.expertise)
    user.price_per_session = data.get('price_per_session', user.price_per_session)
    db.session.commit()
    return jsonify({'msg': 'Profile updated.'})

@bp.route('/me', methods=['GET'])
@jwt_required()
@role_required('speaker')
def get_my_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    return jsonify({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'expertise': user.expertise,
        'price_per_session': user.price_per_session
    })

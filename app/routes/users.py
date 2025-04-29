from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models import User
from app.middleware import role_required

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/speakers', methods=['GET'])
@jwt_required()
@role_required('user')
def list_speakers():
    speakers = User.query.filter_by(user_type='speaker').all()
    result = []
    for s in speakers:
        result.append({
            'id': s.id,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'expertise': s.expertise,
            'price_per_session': s.price_per_session
        })
    return jsonify(result)

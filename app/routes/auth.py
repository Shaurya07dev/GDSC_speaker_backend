from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from app.utils.otp import generate_otp
from app.utils.email import send_otp_email
from flask_jwt_extended import create_access_token
import os

bp = Blueprint('auth', __name__, url_prefix='/auth')

# In-memory store for OTPs (for demo; use DB or cache in production)
otp_store = {}

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'Email already registered'}), 400

    hashed_pw = generate_password_hash(data['password'])
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=hashed_pw,
        user_type=data['user_type']
    )
    db.session.add(user)
    db.session.commit()

    otp = generate_otp()
    otp_store[user.email] = otp
    send_otp_email(user.email, otp)

    return jsonify({'msg': 'Registered. Please verify OTP sent to your email.'}), 201

@bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    if otp_store.get(user.email) == data['otp']:
        user.is_verified = True
        db.session.commit()
        otp_store.pop(user.email, None)
        return jsonify({'msg': 'Account verified.'})
    else:
        return jsonify({'msg': 'Invalid OTP'}), 400

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'msg': 'Invalid credentials'}), 401
    if not user.is_verified:
        return jsonify({'msg': 'Account not verified'}), 403

    token = create_access_token(identity=user.id, additional_claims={'user_type': user.user_type})
    return jsonify({'access_token': token})

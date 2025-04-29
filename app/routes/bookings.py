from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Booking, User
from app.middleware import role_required
from datetime import datetime, timedelta

bp = Blueprint('bookings', __name__, url_prefix='/bookings')

# Helper: Generate all possible time slots
def generate_time_slots():
    slots = []
    start = 9
    end = 16  # 4 PM
    for hour in range(start, end):
        slot = f"{hour:02d}:00-{hour+1:02d}:02d"
        slots.append(slot)
    return slots

@bp.route('/<int:speaker_id>/slots', methods=['GET'])
@jwt_required()
@role_required('user')
def get_available_slots(speaker_id):
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'msg': 'Date is required (YYYY-MM-DD)'}), 400
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'msg': 'Invalid date format'}), 400

    all_slots = generate_time_slots()
    bookings = Booking.query.filter_by(speaker_id=speaker_id, date=date).all()
    booked_slots = [b.time_slot for b in bookings]
    available_slots = [slot for slot in all_slots if slot not in booked_slots]
    return jsonify({'available_slots': available_slots})

@bp.route('/book', methods=['POST'])
@jwt_required()
@role_required('user')
def book_session():
    data = request.json
    user_id = get_jwt_identity()
    speaker_id = data.get('speaker_id')
    date_str = data.get('date')
    time_slot = data.get('time_slot')

    if not (speaker_id and date_str and time_slot):
        return jsonify({'msg': 'Missing required fields'}), 400

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'msg': 'Invalid date format'}), 400

    # Check if slot is already booked
    existing = Booking.query.filter_by(speaker_id=speaker_id, date=date, time_slot=time_slot).first()
    if existing:
        return jsonify({'msg': 'Time slot already booked'}), 409

    booking = Booking(
        user_id=user_id,
        speaker_id=speaker_id,
        date=date,
        time_slot=time_slot
    )
    db.session.add(booking)
    db.session.commit()

    # (Email and calendar integration will be added in the next step)
    return jsonify({'msg': 'Session booked successfully!'})

from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import abort

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('user_type') != role:
                abort(403, description="Forbidden: Insufficient role")
            return fn(*args, **kwargs)
        return decorator
    return wrapper

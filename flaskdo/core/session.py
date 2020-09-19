from functools import wraps
from flask import session, request, redirect, url_for


# Define my decorator function
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function

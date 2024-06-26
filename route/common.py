from functools import wraps
from flask import session, redirect, url_for, request

def login_required(f):
    """
    Decorator function to check if user is logged in or not.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is not True:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
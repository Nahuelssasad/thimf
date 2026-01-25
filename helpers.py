from functools import wraps
from flask import g, request, redirect, url_for,session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function
def allowed_file(filename,list):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in list

from flask import session, flash, url_for, redirect
from functools import wraps
from threading import Thread

# login required decorator
def login_required(f):
    """
    Login required decorator.
    :param f: view function
    :return: if is looged in, return function, else return login page.
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


def async_(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    data = []

    return render_template('index.html', table=data)


@app.route('/secret', methods=['GET', 'POST'])
@login_required
def secret():
    data = ["SECRET SAUCE"]
    return render_template('index.html', table=data)

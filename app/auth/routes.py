import os
import google.auth.transport.requests
import google.oauth2.id_token
from flask import (Blueprint, request, g, session, abort, render_template,
    redirect, url_for)

HTTP_REQUEST = google.auth.transport.requests.Request()
auth_blueprint = Blueprint('auth', __name__)


def verify_firebase_token(token):
    return google.oauth2.id_token.verify_firebase_token(token, HTTP_REQUEST)


def verify_token(token, verifyer=verify_firebase_token):
    return verifyer(token)
    

def login_with_firebase_token():
    """Authenticates user with a firebase token."""
    try:
        # expects token in format `"Authorization: Bearer " + token`
        token = request.headers['Authorization'].split(' ').pop()
    except KeyError:
        abort(400)
    claims = verify_token(token)
    if not claims:
        abort(401)
    g.claims = claims
    session['user_id'] = claims['sub']


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        login_with_firebase_token()
        return redirect(url_for('core.caronas'))


@auth_blueprint.route('/logout', methods=['POST', 'DELETE'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('core.caronas'))

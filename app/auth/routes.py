import os
import google.auth.transport.requests
import google.oauth2.id_token
from flask import Blueprint, request, g, abort, current_app

HTTP_REQUEST = google.auth.transport.requests.Request()
auth_blueprint = Blueprint('auth', __name__)


def verify_firebase_token(token):
    return google.oauth2.id_token.verify_firebase_token(token, HTTP_REQUEST)


def verify_token(token, verifyer=verify_firebase_token):
    return verifyer(token)
    

@auth_blueprint.before_app_request
def firebase_auth():
    """Authenticates user with a firebase token."""
    if os.environ.get('DISABLE_AUTH') == '1':
        # disable auth for testing purposes
        # g.claims are not set
        return
        
    try:
        # expects token in format `"Authorization: Bearer " + token`
        token = request.headers['Authorization'].split(' ').pop()
    except (KeyError, ValueError):
        abort(400)

    claims = verify_token(token)
    if not claims:
        abort(401)
    g.claims = claims # save claims to use later


@auth_blueprint.route('/auth', methods=['GET', 'POST'])
def auth():
    return "OK", 200

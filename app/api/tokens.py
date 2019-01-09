from app import db
from flask import jsonify, g
from app.api import bp
from app.api.auth import basic_auth, token_auth

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token(): # Creates a token for the user whomst requested such.
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})

@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token(): # Revokes/deletes a token once used.
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204 # Helpful for successful requests with no response body.

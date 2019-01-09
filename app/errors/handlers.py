from flask import render_template, request
from app import db
from app.errors import bp
from app.api.errors import error_response as api_error_response


# Uses content negotiation to detect whether to render JSON or HTML
# Imported the 'error_response' helper function from the API for JSON
# responses. Renamed to 'api_error_response' for clarity.


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']

@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('error/500.html'), 500

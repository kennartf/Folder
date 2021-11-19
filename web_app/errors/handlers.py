from flask import Blueprint
from flask import render_template
 

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def page_not_found(error):
    return render_template('404_error_page.html'), 404


@errors.app_errorhandler(403)
def page_not_found(error):
    return render_template('403_error_page.html'), 403


@errors.app_errorhandler(505)
def page_not_found(error):
    return render_template('505_error.html'), 505
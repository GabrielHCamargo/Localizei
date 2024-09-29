from flask import Blueprint, render_template

error = Blueprint("error", __name__)


@error.app_errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@error.app_errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


@error.app_errorhandler(405)
def method_not_allowed(error):
    return render_template("405.html"), 405

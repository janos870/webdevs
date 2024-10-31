from flask import render_template, Blueprint
from flask_login import current_user

about_bp = Blueprint("about", __name__)

@about_bp.route("/about")
def about():
    return render_template("about.html", current_user=current_user)
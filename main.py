from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from models.model import db, User
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from routes.account import account_bp
from routes.profile import profile_bp
from routes.posts import posts_bp
from routes.contact import contact_bp
from routes.about import about_bp

load_dotenv()

app = Flask(__name__)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("PG_ADMIN_DB")
db.init_app(app)
app.config["SECRET_KEY"] = os.getenv("APP_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)

with app.app_context():
    db.create_all()

app.register_blueprint(account_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(about_bp)

# For adding profile images to the comment section
gravatar = Gravatar(
    app,
    size=100,
    rating="g",
    default="retro",
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None,
)

if __name__ == "__main__":
    app.run(debug=True, port=5001)


"""
Make sure the required packages are installed: 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
"""
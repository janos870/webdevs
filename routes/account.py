from flask import (
    Flask,
    abort,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    Blueprint,
)
from flask_login import (
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from models.model import User, db
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

account_bp = Blueprint("account", __name__)


def send_confirmation_email(email):
    try:
        email_message = Message("Confirm Registration", recipients=[email])
        email_message.body = "Thank you for registering. Please confirm your email by clicking on the following link: [link]"
        mail.send(email_message)
    except Exception as e:
        print(f"SMTP Error: {e}")


# Register new users into the User database
@account_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user email is already present in the database.
        result = db.session.execute(
            db.select(User).where(User.email == form.email.data)
        )
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("account.login"))

        hash_and_salted_password = generate_password_hash(
            form.password.data, method="pbkdf2:sha256", salt_length=8
        )

        
        new_user = User(
           
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()

        # Send confirmation email
        send_confirmation_email(new_user.email)

        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("posts.get_all_posts"))
    return render_template("register.html", form=form, current_user=current_user)


@account_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(
            db.select(User).where(User.email == form.email.data)
        )
        user = result.scalar()
        if not user:
            flash("Ez az e-mail cím nem létezik, próbáld újra.")
            return redirect(url_for("account.login"))
        elif not check_password_hash(user.password, password):
            flash("Hibás jelszó, próbálkozzon újra.")
            return redirect(url_for("account.login"))
        else:
            login_user(user)
            return redirect(url_for("posts.get_all_posts"))

    return render_template("login.html", form=form, current_user=current_user)


@account_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("posts.get_all_posts"))

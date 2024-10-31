from flask import Flask, render_template, redirect, url_for, Blueprint
from models.model import User, Comment, BlogPost, db
from flask_login import login_required, current_user, logout_user

profile_bp = Blueprint("profile", __name__)


@profile_bp.route('/profile')
@login_required
def profile():
    # user_posts = BlogPost.query.filter_by(user_id=current_user.id).all()
    # print(user_posts)
    return render_template("profile.html", current_user=current_user)


@profile_bp.route('/delete_profile')
@login_required
def delete_profile():
    user = User.query.get(current_user.id)
    if user:
        # Kommentek törlése
        Comment.query.filter_by(author_id=user.id).delete()

        # Megosztott bejegyzések törlése
        BlogPost.query.filter_by(author_id=user.id).delete()

        # Felhasználó törlése az adatbázisból
        db.session.delete(user)
        db.session.commit()

        logout_user()

        # Automatikus kijelentkeztetés és átirányítás a logout útvonalra
        return redirect(url_for('account.logout'))

    else:
        abort(404)  # Felhasználó nem található vagy már törölve van

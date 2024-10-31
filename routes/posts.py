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
from forms import CreatePostForm, CommentForm
from models.model import User, BlogPost, Comment, db
from flask_login import (
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from functools import wraps
from sqlalchemy import desc
from flask_ckeditor import CKEditor
from datetime import date

posts_bp = Blueprint("posts", __name__)

# Create an admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 6:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@posts_bp.route("/")
def get_all_posts():
    posts = BlogPost.query.order_by(desc(BlogPost.date)).all()
    return render_template("index.html", all_posts=posts, current_user=current_user)


# Add a POST method to be able to post comments
@posts_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)

    # Megtekintések számának növelése, ha a GET kérés érkezik
    if request.method == "GET":
        requested_post.views += 1
        db.session.commit()

    # Add the CommentForm to the route
    comment_form = CommentForm()
    # Only allow logged-in users to comment on posts
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("account.login"))

        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post,
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template(
        "post.html", post=requested_post, current_user=current_user, form=comment_form
    )


# Use a decorator so only an admin user can create new posts
@posts_bp.route("/new-post", methods=["GET", "POST"])
@admin_only
@login_required
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("posts.get_all_posts"))
    return render_template("make-post.html", form=form, current_user=current_user)


# Use a decorator so only an admin user can edit a post
@posts_bp.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body,
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template(
        "make-post.html", form=edit_form, is_edit=True, current_user=current_user
    )


# Use a decorator so only an admin user can delete a post
@posts_bp.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("posts.get_all_posts"))

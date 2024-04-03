from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blogbejegyzés címe", validators=[DataRequired()])
    subtitle = StringField("Felirat", validators=[DataRequired()])
    img_url = StringField("Blog kép URL-je", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog tartalma", validators=[DataRequired()])
    submit = SubmitField("Bejegyzés elküldése")


# Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Jelszó", validators=[DataRequired()])
    name = StringField("Név", validators=[DataRequired()])
    submit = SubmitField("Regisztrálj fel!")


# Create a form to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Jelszó", validators=[DataRequired()])
    submit = SubmitField("Engedj be!")


# Create a form to add comments
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Hozzászólás", validators=[DataRequired()])
    submit = SubmitField("Hozzászólás beküldése")

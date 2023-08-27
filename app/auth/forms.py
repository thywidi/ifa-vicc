from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={"class": "input input-bordered"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"class": "input input-bordered"},
    )
    submit = SubmitField(
        "Sign In",
        render_kw={"class": "btn btn-primary"},
    )


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={"class": "input input-bordered"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"class": "input input-bordered"},
    )
    passwordRepeat = PasswordField(
        "Repat Password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"class": "input input-bordered"},
    )
    submit = SubmitField(
        "Register",
        render_kw={"class": "btn btn-primary"},
    )

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValueError("Username already taken")

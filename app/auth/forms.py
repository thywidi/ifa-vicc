from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


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

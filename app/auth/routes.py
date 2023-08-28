from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app import db


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:  # type: ignore
        flash("Already logged in")
        return redirect(url_for("parking.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "error")
            return redirect(url_for("auth.login"))
        login_user(user)
        next = request.args.get("next")
        if not next or url_parse(next).netloc != "":
            next = url_for("parking.index")
        return redirect(next)
    return render_template("pages/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("parking.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:  # type: ignore
        return redirect(url_for("parking.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)  # type: ignore
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}")
        return redirect(url_for("auth.login"))
    return render_template("pages/register.html", title="Register", form=form)

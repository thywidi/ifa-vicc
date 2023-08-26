from flask import render_template, flash, redirect, url_for
from app.auth import bp
from app.auth.forms import LoginForm


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested for user {}".format(form.username.data))
        return redirect(url_for("index"))
    return render_template("pages/login.html", title="Sign In", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    return render_template("pages/register.html", title="Register")

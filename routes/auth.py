from flask import Blueprint, render_template, redirect, url_for, flash

from flask_login import login_user, logout_user, login_required

from werkzeug.security import check_password_hash

from forms.login_form import LoginForm
from models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            username=form.username.data
        ).first()

        if user and check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(user)

            flash("Login Successful!", "success")

            return redirect(url_for("main.dashboard"))

        flash("Invalid Username or Password", "danger")

    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged Out Successfully", "info")

    return redirect(url_for("auth.login"))
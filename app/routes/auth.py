from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session,
    current_app,
)
from flask_login import login_user, logout_user
from urllib.parse import urlparse

from app.models.user import User
from app.forms.login import LoginForm
from app.forms.register import RegisterForm
from app.core.security import verify_password, generate_password_hash

from app.core.db import db


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and verify_password(password, user.password):
            session['user_id'] = user.id
            session['enabled'] = True
            
            login_user(user)
            current_app.logger.info("Cliente conectado.")

            next_page = request.args.get("next")
            if next_page and is_safe_url(next_page):
                return redirect(next_page)

            return redirect(url_for("main.index"))
        else:
            flash("Credenciais inválidas. Tente novamente.", "danger")

    return render_template("login.html", form=form)


def is_safe_url(target):
    if not target:
        return False

    parsed_url = urlparse(target)

    if parsed_url.netloc == "":
        return True

    return parsed_url.netloc == request.host


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = generate_password_hash(form.password.data)
        full_name = form.name.data

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Este e-mail já está cadastrado. Por favor, use outro.", "danger")
            return render_template("cadastro.html", form=form)

        new_user = User(email=email, full_name=full_name, password=password)
        
        db.session.add(new_user)
        db.session.commit()

        flash("Cadastro realizado com sucesso! Faça login para continuar.", "success")
        current_app.logger.info(f"Novo usuário cadastrado: {email}")
        return redirect(url_for("auth.login"))

    return render_template("cadastro.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    flash("Você foi desconectado.", "success")
    current_app.logger.info("Cliente desconectado.")
    return redirect(url_for("auth.login"))

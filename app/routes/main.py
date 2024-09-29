from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user

from app.models.address import Address

main = Blueprint("main", __name__)


@main.route("/")
def index():
    if current_user.is_authenticated:
        data = {
            "address_count": Address.query.filter_by(user_id=current_user.id).count(),
            "favorite_count": Address.query.filter_by(user_id=current_user.id, favorite=True).count(),
        }
    else:
        data = {
            "address_count": 0,
            "favorite_count": 0,
        }
    return render_template("index.html", data=data)


@main.route("/meus-enderecos")
@login_required
def address():
    current_app.logger.info("Página de endereços acessada.")
    addresses = Address.query.filter_by(user_id=current_user.id).all()
    return render_template("meus-enderecos.html", addresses=addresses)


@main.route("/locais-favoritos")
@login_required
def favorite_places():
    current_app.logger.info("Página de locais favoritos acessada.")
    favorite_addresses = Address.query.filter_by(user_id=current_user.id, favorite=True).all()
    return render_template("locais-favoritos.html", addresses=favorite_addresses)

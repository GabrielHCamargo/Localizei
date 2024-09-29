from flask import Blueprint, request
from flask_login import login_required, current_user

from app.models.address import Address

from app.core.db import db

api = Blueprint("api", __name__)


@api.route("/api/cep/<cep>", methods=["POST"])
def post_cep(cep):
    data = request.get_json()
    logradouro = data.get("logradouro")
    bairro = data.get("bairro")
    localidade = data.get("localidade")
    uf = data.get("uf")

    cep_data = {
        "logradouro": logradouro,
        "bairro": bairro,
        "localidade": localidade,
        "uf": uf,
    }

    if current_user.is_authenticated:
        existing_address = Address.query.filter_by(
            user_id=current_user.id, postal_code=cep
        ).first()

        if existing_address is None:
            new_address = Address(
                user_id=current_user.id,
                street=logradouro,
                city=localidade,
                state=uf,
                country="Brasil",
                postal_code=cep,
                favorite=False,
            )
            db.session.add(new_address)
            db.session.commit()
            return {"message": True}, 201

        return {"message": "Endereço já cadastrado"}, 422
    else:
        return {"message": "Usuário não cadastrado"}, 401


@api.route("/api/favorite/<cep>", methods=["POST"])
def post_favorite(cep):
    if current_user.is_authenticated:
        address = Address.query.filter_by(
            user_id=current_user.id, postal_code=cep
        ).first()
        if address:
            address.favorite = not address.favorite
            db.session.commit()
            return {"message": True}, 200
        else:
            return {"message": "Endereço não encontrado"}, 404
    else:
        return {"message": "Usuário não autenticado"}, 401

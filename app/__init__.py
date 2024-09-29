from dotenv import load_dotenv
load_dotenv()

import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_caching import Cache
from flask_compress import Compress
from flask_session import Session
from flask_login import LoginManager

from app.core.config import Settings
from app.core.db import db


def create_app(config_class=Settings):
    app = Flask(__name__, static_url_path="/static")

    # Carregando configurações do Flask
    config_class.init_app(app)

    # Inicializa o Flask-Session
    Session(app)

    # Inicializa o Flask-Caching
    cache = Cache()
    cache.init_app(app)

    # Ativa a compressão
    compress = Compress()
    compress.init_app(app)

    # Configuração do Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Você precisa fazer login para acessar esta página."

    # Registra o user_loader
    @login_manager.user_loader
    @cache.memoize(timeout=1800)
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Configuração do logging
    if not os.path.exists("logs"):
        os.makedirs("logs", exist_ok=True)

    # Configuração do RotatingFileHandler com UTF-8
    handler = RotatingFileHandler("logs/app.log", maxBytes=10000, backupCount=3, encoding="utf-8")
    handler.setLevel(logging.INFO)  # Define o nível de logging

    # Formatação do logger para incluir arquivo e linha
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d")
    handler.setFormatter(formatter)

    # Adiciona o handler ao logger da aplicação
    app.logger.addHandler(handler)

    # Adiciona o logger global
    app.logger.setLevel(logging.INFO)

    # Inicializa o SQLAlchemy
    db.init_app(app)

    # Registro de rotas
    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.error import error
    from app.routes.api import api

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(error)
    app.register_blueprint(api)
    
    # Importação dos modelos
    with app.app_context():
        from app.models.user import User
        from app.models.address import Address
        db.create_all()
        
    return app

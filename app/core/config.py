import os
from datetime import timedelta


class Settings:
    SECRET_KEY: str = os.environ["SECRET_KEY"]
    SESSION_TYPE: str = os.environ["SESSION_TYPE"]
    SESSION_PERMANENT: bool = os.environ["SESSION_PERMANENT"]
    SESSION_USE_SIGNER: bool = os.environ["SESSION_USE_SIGNER"]
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(os.environ["PERMANENT_SESSION_LIFETIME"]))

    CACHE_TYPE: str = os.environ["CACHE_TYPE"]
    CACHE_DEFAULT_TIMEOUT: int = int(os.environ["CACHE_DEFAULT_TIMEOUT"])

    LOGGING_LEVEL: str = os.environ["LOGGING_LEVEL"]

    SQLALCHEMY_DATABASE_URI: str = os.environ["SQLALCHEMY_DATABASE_URI"]
    

    @classmethod
    def init_app(cls, app):
        """
        Inicializa o app com a configuração fornecida.
        """
        app.config.from_object(cls)


settings = Settings()

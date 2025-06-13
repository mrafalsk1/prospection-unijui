import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://username:password@localhost/postgres"
    )

    SECRET_KEY = os.getenv("SECRET_KEY", "default secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_VALIDATE = True
    RESTX_MASK_SWAGGER = False  # true para esconder em produção
    RESTX_ERROR_404_HELP = False

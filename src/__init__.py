from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from .config import Config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .api import api_bp

    app.register_blueprint(api_bp)

    from .models import Student, Event, Interaction, School, Formation

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "Student": Student,
            "Event": Event,
            "Interaction": Interaction,
            "School": School,
            "Formation": Formation,
        }

    return app

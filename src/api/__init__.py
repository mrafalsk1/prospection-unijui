from flask_restx import Api
from flask import Blueprint


from .student_controller import ns as student_ns
from .event_controller import ns as event_ns
from .interaction_controller import ns as interaction_ns
from .formation_controller import ns as formation_ns
from .school_controller import ns as school_ns

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Digite 'ApiKey <seu_token>' no valor abaixo.",
    }
}

api = Api(
    api_bp,
    version="1.0",
    title="API de Prospecção de aluno",
    description="Uma API para gerenciamento de alunos de prospeção para UNIJUÍ",
    doc="/doc/",
    authorizations=authorizations,
    security="apikey",
)


api.add_namespace(student_ns, path="/students")
api.add_namespace(event_ns, path="/events")
api.add_namespace(interaction_ns, path="/interactions")
api.add_namespace(school_ns, path="/schools")
api.add_namespace(formation_ns, path="/formations")

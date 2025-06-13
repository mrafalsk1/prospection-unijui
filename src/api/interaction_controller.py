from flask_restx import Namespace, Resource
from flask_restx.model import HTTPStatus
from flask_restx.reqparse import RequestParser
from typing import Dict, Any

from ..services import interaction_service
from ..decorators import auth, handle_service_result
from .dtos.interaction_dto import (
    get_interaction_output_fields,
    get_interaction_input_fields,
    interaction_student_summary_fields,
)
from .dtos.event_dto import event_summary_fields, event_input_fields
from .dtos.student_dto import get_student_input_fields as get_full_student_input_fields
from .dtos.school_dto import school_input_fields
from .dtos.formation_dto import formation_input_fields


ns = Namespace(
    "Interações",
    description="Operações relacionadas a interações (aluno participando de um evento)",
)

student_summary_model = ns.model("ResumoAlunoInteracao", interaction_student_summary_fields)  # type: ignore
event_summary_model = ns.model("ResumoEventoInteracao", event_summary_fields)  # type: ignore

school_input_for_student_model = ns.model("InputEscolaParaInteracao", school_input_fields)  # type: ignore
formation_input_for_student_model = ns.model("InputFormacaoParaInteracao", formation_input_fields)  # type: ignore
student_input_for_interaction_model = ns.model(
    "InputAlunoParaInteracao",
    get_full_student_input_fields(
        school_input_for_student_model, formation_input_for_student_model
    ),
)
event_input_for_interaction_model = ns.model("InputEventoParaInteracao", event_input_fields)  # type: ignore

interaction_model = ns.model(
    "Interacao",
    get_interaction_output_fields(student_summary_model, event_summary_model),
)
interaction_input_model = ns.model(
    "InteracaoInput",
    get_interaction_input_fields(
        student_input_for_interaction_model, event_input_for_interaction_model
    ),
)

list_parser = RequestParser()
list_parser.add_argument(
    "student_id", type=int, help="ID do aluno para filtrar as interações"
)
list_parser.add_argument(
    "event_id", type=int, help="ID do evento para filtrar as interações"
)


@ns.route("/")
class InteractionList(Resource):
    method_decorators = [auth(ns)]

    @ns.doc(
        description="Lista todas as interações, com filtros opcionais por aluno ou evento."
    )
    @ns.response(500, "Erro interno do servidor.")
    @ns.expect(list_parser)
    @ns.marshal_list_with(interaction_model)
    @handle_service_result(ns)
    def get(self):
        """Lista todas as interações (com filtros)"""
        args = list_parser.parse_args()
        print(args)
        student_id = args.get("student_id")
        event_id = args.get("event_id")
        print(student_id)
        return interaction_service.get_all_interactions(
            student_id=student_id, event_id=event_id
        )

    @ns.doc(
        description="Cria uma nova interação, com opção de criar aluno/evento aninhado"
    )
    @ns.response(201, "Interação criada com sucesso.")
    @ns.response(400, "Input inválido.")
    @ns.response(404, "Aluno ou Evento (via ID) não encontrado.")
    @ns.response(
        409, "Esta interação (aluno + evento) ou uma entidade aninhada já existe."
    )
    @ns.response(500, "Erro interno do servidor.")
    @ns.expect(interaction_input_model, validate=True)
    @ns.marshal_with(interaction_model, code=HTTPStatus(201))
    @handle_service_result(ns)
    def post(self):
        """Cria uma nova interação"""
        data: Dict[str, Any] = ns.payload
        return interaction_service.create_interaction(data)


@ns.route("/<int:id>")
@ns.param("id", "O identificador da interação")
class InteractionResource(Resource):
    method_decorators = [auth(ns)]

    @ns.doc(description="Busca uma interação pelo seu identificador")
    @ns.response(404, "Interação não encontrada.")
    @ns.marshal_with(interaction_model)
    @handle_service_result(ns)
    def get(self, id: int):
        """Busca uma interação pelo ID"""
        return interaction_service.get_interaction_by_id(id)

    @ns.doc(description="Deleta uma interação existente")
    @ns.response(204, "Interação deletada com sucesso.")
    @ns.response(404, "Interação não encontrada.")
    @ns.response(500, "Erro interno do servidor.")
    @handle_service_result(ns)
    def delete(self, id: int):
        """Deleta uma interação"""
        return interaction_service.delete_interaction(id)

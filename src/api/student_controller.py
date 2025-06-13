from typing import Any, Dict
from flask_restx import Namespace, Resource
from flask_restx.model import HTTPStatus

from ..services import student_service
from ..decorators import handle_service_result, auth

from .dtos.student_dto import get_student_output_fields, get_student_input_fields
from .dtos.school_dto import school_summary_fields, school_input_fields
from .dtos.formation_dto import formation_summary_fields, formation_input_fields

ns = Namespace(
    "Alunos",
    description="Operações relacionadas a alunos",
)

formation_summary_model = ns.model("ResumoFormacao", formation_summary_fields)
formation_input_fields = ns.model("FormationInput", formation_input_fields)
school_summary_model = ns.model("ResumoEscola", school_summary_fields)
school_input_fields = ns.model("EscolaInput", school_input_fields)

student_model = ns.model(
    "Aluno", get_student_output_fields(school_summary_model, formation_summary_model)
)

student_input_model = ns.model(
    "AlunoInput", get_student_input_fields(school_input_fields, formation_input_fields)
)


@ns.route("/")
@ns.doc(security="apikey")
@ns.response(401, "Não autorizado.")
class StudentList(Resource):
    method_decorators = [auth(ns)]

    @ns.doc(description="Lista todos os alunos")
    @ns.response(500, "Erro interno do servidor.")
    @ns.marshal_list_with(student_model)
    @handle_service_result(ns)
    def get(self):
        """Retorna todos os alunos"""
        return student_service.get_all_students()

    @ns.doc(description="Cria um novo aluno")
    @ns.response(201, "Aluno criado com sucesso.")
    @ns.response(400, "Input inválido.")
    @ns.response(
        409,
        "Um aluno com o e-mail ou uma escola/formação com o nome fornecido já existe.",
    )
    @ns.response(500, "Erro interno do servidor.")
    @ns.expect(student_input_model, validate=True)
    @ns.marshal_with(student_model, code=HTTPStatus(201))
    @handle_service_result(ns)
    def post(self):
        """Cria um novo aluno"""
        data: Dict[str, Any] = ns.payload
        return student_service.create_student_with_relations(data)


@ns.route("/<int:id>")
@ns.response(404, "Aluno não encontrado")
@ns.response(500, "Erro interno do servidor.")
@ns.param("id", "O identificador do aluno")
class StudentResource(Resource):
    method_decorators = [auth(ns)]

    @ns.doc(description="Busca um aluno pelo seu identificador")
    @ns.marshal_with(student_model)
    @handle_service_result(ns)
    def get(self, id):
        """Retorna um aluno pelo id"""
        return student_service.get_student_by_id(id)

    @ns.doc(description="Atualiza um aluno existente")
    @ns.response(200, "Aluno atualizado com sucesso.")
    @ns.response(400, "Input inválido.")
    @ns.response(404, "Aluno/Escola/Formação não encontrado(a)")
    @ns.response(
        409,
        "Um aluno com o e-mail fornecido já existe.",
    )
    @ns.response(500, "Erro interno do servidor.")
    @ns.expect(student_input_model, validate=True)
    @ns.marshal_with(student_model)
    @handle_service_result(ns)
    def put(self, id):
        """Atualize um aluno pelo id"""
        data: Dict[str, Any] = ns.payload
        return student_service.update_student_with_relations(id, data)

    @ns.doc(description="Deleta um aluno existente")
    @ns.response(204, "Aluno deletado com sucesso")
    @ns.response(500, "Erro interno do servidor.")
    @handle_service_result(ns)
    def delete(self, id):
        """Deleta um aluno pelo id."""
        return student_service.delete_student(id)

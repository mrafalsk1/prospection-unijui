from flask_restx import Namespace, Resource
from typing import Dict, Any

from flask_restx.api import HTTPStatus

from ..services import school_service
from ..decorators import handle_service_result, auth
from .dtos.school_dto import school_output_fields, school_input_fields

ns = Namespace("Escolas", description="Operações relacionadas a escolas")

school_model = ns.model("Escola", school_output_fields)  # type: ignore
school_input_model = ns.model("EscolaInput", school_input_fields)  # type: ignore


@ns.route("/")
class SchoolList(Resource):
    method_decorators = [auth(ns)]

    @ns.doc(description="Lista todas as escolas")
    @ns.response(500, "Erro interno do servidor.")
    @ns.marshal_list_with(school_model)
    @handle_service_result(ns)
    def get(self):
        """Lista todas as escolas"""
        return school_service.get_all_schools()

    @ns.doc(description="Cria uma nova escola")
    @ns.response(201, "Escola criada com sucesso.")
    @ns.response(409, "Uma escola com este nome já existe.")
    @ns.response(500, "Erro interno do servidor.")
    @ns.expect(school_input_model, validate=True)
    @ns.marshal_with(school_model, code=HTTPStatus(201))
    @handle_service_result(ns)
    def post(self):
        """Cria uma nova escola"""
        data: Dict[str, Any] = ns.payload
        return school_service.create_school(data)


@ns.route("/<int:id>")
@ns.param("id", "O identificador da escola")
class SchoolResource(Resource):
    method_decorators = [auth(ns)]

    @ns.doc(description="Busca uma escola pelo seu identificador")
    @ns.response(404, "Escola não encontrada.")
    @ns.marshal_with(school_model)
    @handle_service_result(ns)
    def get(self, id: int):
        """Busca uma escola pelo ID"""
        return school_service.get_school_by_id(id)

    @ns.doc(description="Atualiza uma escola existente")
    @ns.response(200, "Escola atualizada com sucesso.")
    @ns.response(404, "Escola não encontrada.")
    @ns.response(409, "Outra escola com este nome já existe.")
    @ns.response(500, "Erro interno do servidor.")
    @ns.expect(school_input_model, validate=True)
    @ns.marshal_with(school_model)
    @handle_service_result(ns)
    def put(self, id: int):
        """Atualiza uma escola"""
        data: Dict[str, Any] = ns.payload
        return school_service.update_school(id, data)

    @ns.doc(description="Deleta uma escola existente")
    @ns.response(204, "Escola deletada com sucesso.")
    @ns.response(400, "Escola não pode ser deletada pois possui alunos associados.")
    @ns.response(404, "Escola não encontrada.")
    @ns.response(500, "Erro interno do servidor.")
    @handle_service_result(ns)
    def delete(self, id: int):
        """Deleta uma escola"""
        return school_service.delete_school(id)

from flask_restx import Namespace, Resource
from typing import Dict, Any

from flask_restx.api import HTTPStatus

from ..services import formation_service
from ..decorators import auth, handle_service_result
from .dtos.formation_dto import formation_output_fields, formation_input_fields

ns = Namespace("Formações", description="Operações relacionadas a formações")

formation_model = ns.model("Formacao", formation_output_fields)  # type: ignore
formation_input_model = ns.model("FormacaoInput", formation_input_fields)  # type: ignore


@ns.route("/")
class FormationList(Resource):
    method_decorators = [auth(ns)]

    @ns.doc(description="Lista todas as formações")
    @ns.response(500, "Erro interno do servidor.")
    @ns.marshal_list_with(formation_model)
    @handle_service_result(ns)
    def get(self):
        """Lista todas as formações"""
        return formation_service.get_all_formations()

    @ns.doc(description="Cria uma nova formação")
    @ns.response(201, "Formação criada com sucesso.")
    @ns.response(409, "Uma formação com este nome já existe.")
    @ns.response(500, "Erro interno do servidor.")
    @ns.expect(formation_input_model, validate=True)
    @ns.marshal_with(formation_model, code=HTTPStatus(201))
    @handle_service_result(ns)
    def post(self):
        """Cria uma nova formação"""
        data: Dict[str, Any] = ns.payload
        return formation_service.create_formation(data)


@ns.route("/<int:id>")
@ns.param("id", "O identificador da formação")
class FormationResource(Resource):
    method_decorators = [auth(ns)]

    @ns.doc(description="Busca uma formação pelo seu identificador")
    @ns.response(404, "Formação não encontrada.")
    @ns.marshal_with(formation_model)
    @handle_service_result(ns)
    def get(self, id: int):
        """Busca uma formação pelo ID"""
        return formation_service.get_formation_by_id(id)

    @ns.doc(description="Atualiza uma formação existente")
    @ns.response(200, "Formação atualizada com sucesso.")
    @ns.response(404, "Formação não encontrada.")
    @ns.response(409, "Outra formação com este nome já existe.")
    @ns.response(500, "Erro interno do servidor.")
    @ns.expect(formation_input_model, validate=True)
    @ns.marshal_with(formation_model)
    @handle_service_result(ns)
    def put(self, id: int):
        """Atualiza uma formação"""
        data: Dict[str, Any] = ns.payload
        return formation_service.update_formation(id, data)

    @ns.doc(description="Deleta uma formação existente")
    @ns.response(204, "Formação deletada com sucesso.")
    @ns.response(
        400, "Formação não pode ser deletada pois alunos estão interessados nela."
    )
    @ns.response(404, "Formação não encontrada.")
    @ns.response(500, "Erro interno do servidor.")
    @handle_service_result(ns)
    def delete(self, id: int):
        """Deleta uma formação"""
        return formation_service.delete_formation(id)

from flask_restx import Namespace, Resource
from typing import Dict, Any

from flask_restx.api import HTTPStatus

from ..services import event_service
from ..decorators import auth, handle_service_result
from .dtos.event_dto import event_output_fields, event_input_fields

ns = Namespace("Eventos", description="Operações relacionadas a eventos")

event_model = ns.model("Evento", event_output_fields)  # type: ignore
event_input_model = ns.model("EventoInput", event_input_fields)  # type: ignore


@ns.route("/")
class EventList(Resource):
    method_decorators = [auth(ns)]

    @ns.doc(description="Lista todos os eventos")
    @ns.response(500, "Erro interno do servidor.")
    @ns.marshal_list_with(event_model)
    @handle_service_result(ns)
    def get(self):
        """Lista todos os eventos"""
        result = event_service.get_all_events()
        return result

    @ns.doc(description="Cria um novo evento")
    @ns.response(201, "Evento criado com sucesso.")
    @ns.response(400, "Formato de data inválido.")
    @ns.response(500, "Erro interno do servidor.")
    @ns.expect(event_input_model, validate=True)
    @ns.marshal_with(event_model, code=HTTPStatus(201))
    @handle_service_result(ns)
    def post(self):
        """Cria um novo evento"""
        data: Dict[str, Any] = ns.payload
        event_service.create_event(data)
        return event_service.create_event(data)


@ns.route("/<int:id>")
@ns.param("id", "O identificador do evento")
class EventResource(Resource):
    method_decorators = [auth(ns)]

    @ns.doc(description="Busca um evento pelo seu identificador")
    @ns.response(404, "Evento não encontrado.")
    @ns.marshal_with(event_model)
    @handle_service_result(ns)
    def get(self, id: int):
        """Retorna um evento pelo id"""
        return event_service.get_event_by_id(id)

    @ns.doc(description="Atualiza um evento existente")
    @ns.response(200, "Evento atualizado com sucesso.")
    @ns.response(400, "Formato de data inválido.")
    @ns.response(404, "Evento não encontrado.")
    @ns.response(500, "Erro interno do servidor.")
    @ns.expect(event_input_model, validate=True)
    @ns.marshal_with(event_model)
    @handle_service_result(ns)
    def put(self, id: int):
        """Atualize um evento pelo id"""
        data: Dict[str, Any] = ns.payload
        return event_service.update_event(id, data)

    @ns.doc(description="Deleta um evento existente")
    @ns.response(204, "Evento deletado com sucesso.")
    @ns.response(400, "Evento não pode ser deletado pois possui interações associadas.")
    @ns.response(404, "Evento não encontrado.")
    @ns.response(500, "Erro interno do servidor.")
    @handle_service_result(ns)
    def delete(self, id: int):
        """Deleta um evento pelo id"""
        return event_service.delete_event(id)

from flask_restx import OrderedModel, fields, Model
from typing import Any
from .event_dto import event_summary_fields

interaction_student_summary_fields = {
    "id": fields.Integer(description="ID do aluno"),
    "full_name": fields.String(description="Nome completo do aluno"),
}


def get_interaction_output_fields(
    student_summary_model: Model | OrderedModel,
    event_summary_model: Model | OrderedModel,
) -> dict:
    return {
        "id": fields.Integer(
            readonly=True, description="Identificador único da interação"
        ),
        "student_id": fields.Integer(required=True, description="ID do aluno"),
        "student": fields.Nested(
            student_summary_model, readonly=True, description="Detalhes do aluno"
        ),
        "event_id": fields.Integer(required=True, description="ID do evento"),
        "event": fields.Nested(
            event_summary_model, readonly=True, description="Detalhes do evento"
        ),
        "interaction_date": fields.DateTime(
            readonly=True, description="Data de criação da interação"
        ),
    }


def get_interaction_input_fields(
    student_input_model: Model | OrderedModel, event_input_model: Model | OrderedModel
) -> dict:
    return {
        "student_id": fields.Integer(description="ID de um aluno existente", example=1),
        "student": fields.Nested(
            student_input_model, description="Dados para criar um novo aluno na hora"
        ),
        "event_id": fields.Integer(description="ID de um evento existente", example=1),
        "event": fields.Nested(
            event_input_model, description="Dados para criar um novo evento na hora"
        ),
    }

from src.models.formation import Formation
from src.models.school import School
from .. import db
from ..models import Interaction, Student, Event
from typing import Dict, Any, List, Optional
from ..utils.service_utils import ServiceResult, ServiceError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from .student_service import create_student_with_relations
from .event_service import create_event
from src.services import student_service

from src.services import event_service


def get_all_interactions(
    student_id: Optional[int] = None, event_id: Optional[int] = None
) -> ServiceResult[List[Interaction]]:
    try:

        stmt = Interaction.query.options(
            joinedload(Interaction.student), joinedload(Interaction.event)  # type: ignore
        )

        if student_id:
            stmt = stmt.where(Interaction.student_id == student_id)
        if event_id:
            stmt = stmt.where(Interaction.event_id == event_id)

        interactions = stmt.order_by(Interaction.interaction_date).all()
        print(interactions)
        return ServiceResult(success=True, data=interactions)
    except Exception:
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Erro ao buscar interações.",
        )


def get_interaction_by_id(interaction_id: int) -> ServiceResult[Interaction]:
    stmt = (
        select(Interaction)
        .options(joinedload(Interaction.student), joinedload(Interaction.event))  # type: ignore
        .where(Interaction.id == interaction_id)
    )
    interaction = db.session.scalars(stmt).first()
    if not interaction:
        return ServiceResult(
            success=False,
            error_type=ServiceError.NOT_FOUND,
            message=f"Interação com ID {interaction_id} não encontrada.",
        )
    return ServiceResult(success=True, data=interaction)


def create_interaction(
    data: Dict[str, Any],
) -> (
    ServiceResult[Interaction]
    | ServiceResult[Student]
    | ServiceResult[School]
    | ServiceResult[Formation]
    | ServiceResult[Event]
):
    student_id = data.get("student_id")
    student_input = data.get("student")
    if not student_id and not student_input:
        return ServiceResult(
            success=False,
            error_type=ServiceError.INVALID_INPUT,
            message="Forneça 'student_id' ou 'student'",
        )

    final_student_id = student_id
    if student_input and not final_student_id:
        student_result = create_student_with_relations(student_input)
        if not student_result.success:
            return student_result
        if student_result.data:
            final_student_id = student_result.data.id

    if not final_student_id:
        return ServiceResult(
            success=False,
            error_type=ServiceError.INVALID_INPUT,
            message="Forneça 'student_id' ou 'student'",
        )

    student = student_service.get_student_by_id(final_student_id)
    if not student.success:
        return ServiceResult(
            success=False,
            error_type=ServiceError.NOT_FOUND,
            message=f"Aluno com ID {final_student_id} não encontrado.",
        )

    event_id = data.get("event_id")
    event_input = data.get("event")
    if not event_id and not event_input:
        return ServiceResult(
            success=False,
            error_type=ServiceError.INVALID_INPUT,
            message="Forneça 'event_id' ou 'event_input'",
        )

    final_event_id = event_id
    if event_input and not final_event_id:
        event_result = create_event(event_input)
        if not event_result.success:
            return event_result
        if event_result.data:
            final_event_id = event_result.data.id

    if not final_event_id:
        return ServiceResult(
            success=False,
            error_type=ServiceError.INVALID_INPUT,
            message="É necessário fornecer 'student_id' (ou 'student') e 'event_id' (ou 'event').",
        )

    event = event_service.get_event_by_id(final_event_id)
    if not event.success:
        return ServiceResult(
            success=False,
            error_type=ServiceError.NOT_FOUND,
            message=f"Evento com ID {final_event_id} não encontrado.",
        )

    try:
        new_interaction = Interaction()
        new_interaction = Interaction()
        new_interaction.student_id = final_student_id
        new_interaction.event_id = final_event_id

        db.session.add(new_interaction)
        db.session.commit()
        return get_interaction_by_id(new_interaction.id)
    except IntegrityError as e:
        print(e)
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.ALREADY_EXISTS,
            message="Este aluno já está registrado para este evento (interação duplicada).",
        )
    except Exception:
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível criar a interação.",
        )


def delete_interaction(
    interaction_id: int,
) -> ServiceResult[None] | ServiceResult[Interaction]:
    interaction_result = get_interaction_by_id(interaction_id)
    if not interaction_result.success:
        return interaction_result

    interaction = interaction_result.data
    try:
        db.session.delete(interaction)
        db.session.commit()
        return ServiceResult(success=True)
    except Exception:
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível deletar a interação.",
        )

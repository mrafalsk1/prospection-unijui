from .. import db
from ..models import Event
from typing import Dict, Any, List
from ..utils.service_utils import ServiceResult, ServiceError
from datetime import datetime


def get_all_events() -> ServiceResult[List[Event]]:
    try:
        events = Event.query.order_by(Event.event_date.desc()).all()
        return ServiceResult(success=True, data=events)
    except Exception:
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Erro ao buscar eventos.",
        )


def get_event_by_id(event_id: int) -> ServiceResult[Event]:
    event = db.session.get(Event, event_id)
    if not event:
        return ServiceResult(
            success=False,
            error_type=ServiceError.NOT_FOUND,
            message=f"Evento com ID {event_id} não encontrado.",
        )
    return ServiceResult(success=True, data=event)


def create_event(data: Dict[str, Any]) -> ServiceResult[Event]:
    try:
        event_date_obj = data.get("event_date")
        if isinstance(event_date_obj, str):
            event_date_obj = datetime.strptime(event_date_obj, "%Y-%m-%d").date()

        new_event = Event()
        new_event.event_name = data["event_name"]
        new_event.event_date = data["event_date"]
        new_event.event_location = data["event_location"]
        new_event.description = data["description"]

        db.session.add(new_event)
        db.session.commit()
        db.session.refresh(new_event)
        return ServiceResult(success=True, data=new_event)
    except ValueError:
        return ServiceResult(
            success=False,
            error_type=ServiceError.INVALID_INPUT,
            message="Formato de data inválido para event_date. Use AAAA-MM-DD.",
        )
    except Exception:
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível criar o evento.",
        )


def update_event(event_id: int, data: Dict[str, Any]) -> ServiceResult[Event]:
    event_result = get_event_by_id(event_id)
    if not event_result.success or not event_result.data:
        return event_result

    event = event_result.data

    event.event_name = data.get("event_name", event.event_name)
    if "event_date" in data:
        try:
            event_date_val = data.get("event_date", event.event_date)
            if isinstance(event_date_val, str):
                event.event_date = datetime.strptime(event_date_val, "%Y-%m-%d").date()
            elif event_date_val is not None:
                event.event_date = event_date_val
        except ValueError:
            return ServiceResult(
                success=False,
                error_type=ServiceError.INVALID_INPUT,
                message="Formato de data inválido para event_date. Use AAAA-MM-DD.",
            )

    event.event_location = data.get("event_location", event.event_location)
    event.description = data.get("description", event.description)

    try:
        db.session.commit()
        return ServiceResult(success=True, data=event)
    except Exception:
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível atualizar o evento.",
        )


def delete_event(event_id: int) -> ServiceResult[None] | ServiceResult[Event]:
    event_result = get_event_by_id(event_id)
    if not event_result.success or not event_result.data:
        return event_result

    event = event_result.data
    if event.interactions:
        return ServiceResult(
            success=False,
            error_type=ServiceError.DEPENDENCY_ERROR,
            message="Não é possível deletar o evento. Interações de alunos estão associadas a ele.",
        )

    try:
        db.session.delete(event)
        db.session.commit()
        return ServiceResult(success=True)
    except Exception:
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível deletar o evento.",
        )

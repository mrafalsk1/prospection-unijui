from src.services import student_service
from .. import db
from ..models import Formation
from typing import Dict, Any, List
from ..utils.service_utils import ServiceResult, ServiceError
from datetime import datetime


def get_all_formations() -> ServiceResult[List[Formation]]:
    try:
        formations = Formation.query.order_by(Formation.name).all()
        return ServiceResult(success=True, data=formations)
    except Exception:
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Erro ao buscar formações.",
        )


def get_formation_by_id(formation_id: int) -> ServiceResult[Formation]:
    formation = db.session.get(Formation, formation_id)
    if not formation:
        return ServiceResult(
            success=False,
            error_type=ServiceError.NOT_FOUND,
            message=f"Formação com ID {formation_id} não encontrada.",
        )
    return ServiceResult(success=True, data=formation)


def create_formation(data: Dict[str, Any]) -> ServiceResult[Formation]:
    if Formation.query.filter_by(name=data["name"]).first():
        return ServiceResult(
            success=False,
            error_type=ServiceError.ALREADY_EXISTS,
            message=f"Formação com o nome '{data['name']}' já existe.",
        )

    try:
        new_formation = Formation()
        new_formation.name = data["name"]
        new_formation.description = data.get("description")
        new_formation.degree_level = data.get("degree_level")

        db.session.add(new_formation)
        db.session.commit()
        db.session.refresh(new_formation)
        return ServiceResult(success=True, data=new_formation)
    except Exception as e:
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível criar a formação.",
        )


def update_formation(
    formation_id: int, data: Dict[str, Any]
) -> ServiceResult[Formation]:
    formation_result = get_formation_by_id(formation_id)
    if not formation_result.success or not formation_result.data:
        return formation_result

    formation = formation_result.data
    if "name" in data and data["name"] != formation.name:
        if Formation.query.filter(
            Formation.id != formation_id, Formation.name == data["name"]
        ).first():
            return ServiceResult(
                success=False,
                error_type=ServiceError.ALREADY_EXISTS,
                message=f"Outra formação com o nome '{data['name']}' já existe.",
            )
    formation.name = data.get("name", formation.name)
    formation.description = data.get("description", formation.description)
    formation.degree_level = data.get("degree_level", formation.degree_level)
    formation.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        return ServiceResult(success=True, data=formation)
    except Exception:
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível atualizar a formação.",
        )


def delete_formation(
    formation_id: int,
) -> ServiceResult[None] | ServiceResult[Formation]:
    formation_result = get_formation_by_id(formation_id)
    if not formation_result.success or not formation_result.data:
        return formation_result
    formation = formation_result.data
    intersted_students = student_service.get_all_students(formation_id=formation_id)
    if not intersted_students.data or not len(intersted_students.data):
        return ServiceResult(
            success=False,
            error_type=ServiceError.DEPENDENCY_ERROR,
            message="Não é possível deletar a formação. Alunos estão interessados nela.",
        )
    try:
        db.session.delete(formation)
        db.session.commit()
        return ServiceResult(success=True)
    except Exception:
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível deletar a formação.",
        )

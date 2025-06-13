from src.services import student_service
from ..utils.service_utils import ServiceError, ServiceResult
from .. import db
from ..models import School
from typing import Dict, Any, List
from datetime import datetime


def get_all_schools() -> ServiceResult[List[School]]:
    try:
        schools = School.query.order_by(School.name).all()
        return ServiceResult(success=True, data=schools)
    except Exception:
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Erro ao buscar escolas.",
        )


def get_school_by_id(school_id: int) -> ServiceResult[School]:
    school = db.session.get(School, school_id)
    if not school:
        return ServiceResult(
            success=False,
            error_type=ServiceError.NOT_FOUND,
            message=f"Escola com ID {school_id} não encontrada.",
        )
    return ServiceResult(success=True, data=school)


def create_school(data: Dict[str, Any]) -> ServiceResult[School]:
    """Cria uma nova escola."""
    if School.query.filter_by(name=data["name"]).first():
        return ServiceResult(
            success=False,
            error_type=ServiceError.ALREADY_EXISTS,
            message=f"Escola com o nome '{data['name']}' já existe.",
        )

    try:
        new_school = School()
        new_school.name = data["name"]
        new_school.city = data.get("city")

        db.session.add(new_school)
        db.session.commit()
        db.session.refresh(new_school)
        return ServiceResult(success=True, data=new_school)
    except Exception as e:
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível criar a escola.",
        )


def update_school(school_id: int, data: Dict[str, Any]) -> ServiceResult[School]:
    school_result = get_school_by_id(school_id)
    if not school_result.success or not school_result.data:
        return school_result
    school = school_result.data
    if "name" in data and data["name"] != school.name:
        if School.query.filter(
            School.id != school_id, School.name == data["name"]
        ).first():
            return ServiceResult(
                success=False,
                error_type=ServiceError.ALREADY_EXISTS,
                message=f"Outra escola com o nome '{data['name']}' já existe.",
            )

    school.name = data.get("name", school.name)
    school.city = data.get("city", school.city)
    school.updated_at = datetime.utcnow()
    try:
        db.session.commit()
        return ServiceResult(success=True, data=school)
    except Exception:
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível atualizar a escola.",
        )


def delete_school(school_id: int) -> ServiceResult[None] | ServiceResult[School]:
    school_result = get_school_by_id(school_id)
    if not school_result.success or not school_result.data:
        return school_result
    school = school_result.data

    school_students = student_service.get_all_students(school_id)
    if not school_students.data or not len(school_students.data):
        return ServiceResult(
            success=False,
            error_type=ServiceError.DEPENDENCY_ERROR,
            message="Não é possível deletar a escola. Alunos estão associados a ela.",
        )
    try:
        db.session.delete(school)
        db.session.commit()
        return ServiceResult(success=True)
    except Exception:
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível deletar a escola.",
        )

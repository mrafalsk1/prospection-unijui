from .. import db
from datetime import datetime
from ..models import Student, School, Formation
from .school_service import create_school
from .formation_service import create_formation
from sqlalchemy.orm import joinedload
from typing import Dict, Any, List, Optional
from ..utils.service_utils import ServiceResult, ServiceError
from src.services import school_service

from src.services import formation_service


def get_all_students(
    school_id: Optional[int] = None, formation_id: Optional[int] = None
) -> ServiceResult[List[Student]]:
    try:
        stmt = Student.query.options(
            joinedload(Student.school), joinedload(Student.main_formation)  # type: ignore
        )

        if school_id:
            stmt = stmt.where(Student.school_id == school_id)

        if formation_id:
            stmt = stmt.where(Student.main_formation_id == formation_id)

        students = stmt.order_by(Student.full_name).all()

        return ServiceResult(success=True, data=students)
    except Exception:
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Erro ao buscar alunos.",
        )


def get_student_by_id(id: int) -> ServiceResult[Student]:
    student = (
        db.session.query(Student)
        .options(
            joinedload(Student.school),  # type: ignore
            joinedload(Student.main_formation),  # type: ignore
        )
        .where(Student.id == id)
        .first()
    )

    if not student:
        return ServiceResult(
            success=False,
            error_type=ServiceError.NOT_FOUND,
            message=f"Aluno com ID {id} não encontrado.",
        )
    return ServiceResult(success=True, data=student)


def create_student_with_relations(
    data: Dict[str, Any],
) -> ServiceResult[Student] | ServiceResult[School] | ServiceResult[Formation]:
    print(data)
    if Student.query.filter_by(email=data["email"]).first():
        return ServiceResult(
            success=False,
            error_type=ServiceError.ALREADY_EXISTS,
            message=f"Aluno com o e-mail '{data['email']}' já existe.",
        )

    school_id = data.get("school_id")
    school = data.get("school")

    if not school_id and not school:
        return ServiceResult(
            success=False,
            error_type=ServiceError.INVALID_INPUT,
            message="Dados da Escola são obrigatórios para o cadastro",
        )

    final_school_id = school_id
    if school and not school_id:
        school_result = create_school(school)
        if not school_result.success:
            return school_result
        if school_result.data:
            final_school_id = school_result.data.id

    if not final_school_id:
        return ServiceResult(
            success=False,
            error_type=ServiceError.NOT_FOUND,
            message=f"Escola com ID {final_school_id} não encontrada.",
        )

    if not school_service.get_school_by_id(final_school_id).success:
        return ServiceResult(
            success=False,
            error_type=ServiceError.NOT_FOUND,
            message=f"Escola com ID {final_school_id} não encontrada.",
        )

    formation_id = data.get("main_formation_id")
    formation = data.get("main_formation")

    if not formation_id and not formation:
        return ServiceResult(
            success=False,
            error_type=ServiceError.INVALID_INPUT,
            message="Dados da Formação são obrigatórios para o cadastro.",
        )

    final_formation_id = formation_id
    if formation and not formation_id:
        formation_result = create_formation(formation)
        if not formation_result.success:
            return formation_result
        if formation_result.data:
            final_formation_id = formation_result.data.id

    if not final_formation_id:
        return ServiceResult(
            success=False,
            error_type=ServiceError.NOT_FOUND,
            message=f"Formação com ID {final_formation_id} não encontrada.",
        )

    if not formation_service.get_formation_by_id(final_formation_id).success:
        return ServiceResult(
            success=False,
            error_type=ServiceError.NOT_FOUND,
            message=f"Formação com ID {final_formation_id} não encontrada.",
        )
    try:
        new_student = Student()
        new_student.full_name = data["full_name"]
        new_student.email = data["email"]
        new_student.phone_number = data.get("phone_number")
        new_student.school_id = final_school_id
        new_student.main_formation_id = final_formation_id

        db.session.add(new_student)
        db.session.commit()

        created_student = get_student_by_id(new_student.id)

        return ServiceResult(success=True, data=created_student.data)
    except Exception as e:
        print(e)
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível criar o aluno devido a um erro interno.",
        )


def update_student_with_relations(
    student_id: int, data: Dict[str, Any]
) -> ServiceResult[Student] | ServiceResult[School] | ServiceResult[Formation]:
    student_result = get_student_by_id(student_id)
    if not student_result.success or not student_result.data:
        return student_result

    student = student_result.data

    if "email" in data and data["email"] != student.email:
        if Student.query.filter(
            Student.id != student_id, Student.email == data["email"]
        ).first():
            return ServiceResult(
                success=False,
                error_type=ServiceError.ALREADY_EXISTS,
                message=f"O e-mail '{data['email']}' já está registrado por outro aluno.",
            )

    if "school_id" in data or "school" in data:
        school_id = data.get("school_id")
        school_input = data.get("school")
        final_school_id = school_id
        if school_input and not final_school_id:
            school_result = create_school(school_input)
            if not school_result.success:
                return school_result
            if school_result.data:
                final_school_id = school_result.data.id
        student.school_id = final_school_id

        if not final_school_id:
            return ServiceResult(
                success=False,
                error_type=ServiceError.NOT_FOUND,
                message=f"Escola com ID {final_school_id} não encontrada.",
            )

        if not school_service.get_school_by_id(final_school_id).success:
            return ServiceResult(
                success=False,
                error_type=ServiceError.NOT_FOUND,
                message=f"Escola com ID {final_school_id} não encontrada.",
            )

    if "main_formation_id" in data or "main_formation" in data:
        formation_id = data.get("main_formation_id")
        formation_input = data.get("main_formation")
        final_formation_id = formation_id
        if formation_input and not final_formation_id:
            formation_result = create_formation(formation_input)
            if not formation_result.success:
                return formation_result
            if formation_result.data:
                final_formation_id = formation_result.data.id

        if not final_formation_id:
            return ServiceResult(
                success=False,
                error_type=ServiceError.NOT_FOUND,
                message=f"Formação com ID {final_formation_id} não encontrada.",
            )

        if not formation_service.get_formation_by_id(final_formation_id).success:
            return ServiceResult(
                success=False,
                error_type=ServiceError.NOT_FOUND,
                message=f"Formação com ID {final_formation_id} não encontrada.",
            )
        student.main_formation_id = final_formation_id

    student.full_name = data.get("full_name", student.full_name)
    student.email = data.get("email", student.email)
    student.phone_number = data.get("phone_number", student.phone_number)
    student.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        return get_student_by_id(student_id)
    except Exception:
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível atualizar o aluno.",
        )


def delete_student(student_id: int) -> ServiceResult[None] | ServiceResult[Student]:
    student_result = get_student_by_id(student_id)
    if not student_result.success:
        return student_result

    student = student_result.data

    try:
        db.session.delete(student)
        db.session.commit()
        return ServiceResult(success=True)
    except Exception:
        db.session.rollback()
        return ServiceResult(
            success=False,
            error_type=ServiceError.INTERNAL_ERROR,
            message="Não foi possível deletar o aluno.",
        )

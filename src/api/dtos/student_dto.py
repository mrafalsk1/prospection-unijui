from flask_restx import Model, OrderedModel, fields


def get_student_output_fields(
    school_summary_model: Model | OrderedModel,
    formation_summary_model: Model | OrderedModel,
) -> dict:
    return {
        "id": fields.Integer(readonly=True, description="Identificador único do aluno"),
        "full_name": fields.String(required=True, description="Nome completo do aluno"),
        "email": fields.String(
            required=True, description="Endereço de e-mail do aluno"
        ),
        "phone_number": fields.String(description="Número de telefone do aluno"),
        "school_id": fields.Integer(description="ID da escola de origem do aluno"),
        "school": fields.Nested(
            school_summary_model,
            description="Detalhes da escola do aluno",
            skip_none=True,
            allow_null=True,
        ),
        "main_formation_id": fields.Integer(
            description="ID da principal formação de interesse do aluno"
        ),
        "main_formation": fields.Nested(
            formation_summary_model,
            description="Detalhes da principal formação de interesse do aluno",
            skip_none=True,
            allow_null=True,
        ),
        "created_at": fields.DateTime(
            readonly=True, description="Data de criação do registro do aluno"
        ),
        "updated_at": fields.DateTime(
            readonly=True, description="Data da última atualização do registro do aluno"
        ),
    }


def get_student_input_fields(
    school_input_fields: Model | OrderedModel,
    formation_input_fields: Model | OrderedModel,
) -> dict:
    return {
        "full_name": fields.String(
            required=True, description="Nome completo do aluno", example="Maria Silva"
        ),
        "email": fields.String(
            required=True,
            description="Endereço de e-mail do aluno",
            example="maria.silva@email.com",
        ),
        "phone_number": fields.String(
            description="Número de telefone do aluno", example="55999998888"
        ),
        "school_id": fields.Integer(
            description="ID da escola de origem do aluno", example=1, allow_null=True
        ),
        "school": fields.Nested(
            school_input_fields,
            description="Dados de escola para cadastro.",
            skip_none=True,
            allow_null=True,
        ),
        "main_formation_id": fields.Integer(
            description="ID da principal formação de interesse do aluno",
            example=1,
            allow_null=True,
        ),
        "main_formation": fields.Nested(
            formation_input_fields,
            description="Dados de formação para cadatro",
            skip_none=True,
            allow_null=True,
        ),
    }

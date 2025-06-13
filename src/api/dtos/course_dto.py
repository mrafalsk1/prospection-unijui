from flask_restx import fields

course_output_fields = {
    "id": fields.Integer(readonly=True, description="Identificador único do curso"),
    "name": fields.String(required=True, description="Nome do curso"),
    "description": fields.String(description="Descrição do curso"),
    "level": fields.String(description="Grau do curso"),
    "created_at": fields.DateTime(
        readonly=True, description="Data de criação do registro do curso"
    ),
    "updated_at": fields.DateTime(
        readonly=True, description="Data da última atualização do registro do curso"
    ),
}

course_input_fields = {
    "name": fields.String(
        required=True, description="Nome do curso", example="Ciência da Computação"
    ),
    "description": fields.String(
        description="Descrição do curso",
        example="Fundamentos da programação utilizando Python.",
    ),
    "level": fields.String(description="Grau do curso", example="Bacharelado"),
}

course_summary_fields = {
    "id": fields.Integer(readonly=True, description="Identificador único do curso"),
    "name": fields.String(description="Nome do curso"),
}

from flask_restx import fields

school_output_fields = {
    "id": fields.Integer(readonly=True, description="Identificador único da escola"),
    "name": fields.String(required=True, description="Nome da escola"),
    "city": fields.String(description="Cidade onde a escola está localizada"),
    "created_at": fields.DateTime(
        readonly=True, description="Data de criação do registro da escola"
    ),
    "updated_at": fields.DateTime(
        readonly=True, description="Data da última atualização do registro da escola"
    ),
}

school_input_fields = {
    "name": fields.String(
        required=True, description="Nome da escola", example="Colégio Exemplo"
    ),
    "city": fields.String(description="Cidade", example="Qualquer Cidade"),
}

school_summary_fields = {
    "id": fields.Integer(readonly=True, description="Identificador único da escola"),
    "name": fields.String(description="Nome da escola"),
}

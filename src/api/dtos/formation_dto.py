from flask_restx import fields

formation_output_fields = {
    "id": fields.Integer(readonly=True, description="Identificador único da formação"),
    "name": fields.String(required=True, description="Nome da formação"),
    "description": fields.String(description="Descrição da formação"),
    "degree_level": fields.String(
        description="Grau da formação (ex: Bacharelado, Técnico, Pós-graduação)"
    ),
    "created_at": fields.DateTime(
        readonly=True, description="Data de criação do registro da formação"
    ),
    "updated_at": fields.DateTime(
        readonly=True, description="Data da última atualização do registro da formação"
    ),
}

formation_input_fields = {
    "name": fields.String(
        required=True, description="Nome da formação", example="Engenharia de Software"
    ),
    "description": fields.String(
        description="Descrição da formação",
        example="Formação completa em desenvolvimento de software e sistemas.",
    ),
    "degree_level": fields.String(
        description="Grau da formação", example="Bacharelado"
    ),
}

formation_summary_fields = {
    "id": fields.Integer(readonly=True, description="Identificador único da formação"),
    "name": fields.String(description="Nome da formação"),
}

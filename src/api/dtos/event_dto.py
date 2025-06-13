from flask_restx import fields

event_output_fields = {
    "id": fields.Integer(readonly=True, description="Identificador único do evento"),
    "event_name": fields.String(required=True, description="Nome do evento"),
    "event_date": fields.Date(required=True, description="Data do evento (AAAA-MM-DD)"),
    "event_location": fields.String(description="Local do evento"),
    "description": fields.String(description="Descrição do evento"),
    "created_at": fields.DateTime(
        readonly=True, description="Data de criação do registro do evento"
    ),
}

event_input_fields = {
    "event_name": fields.String(
        required=True, description="Nome do evento", example="Feira de Profissões 2025"
    ),
    "event_date": fields.Date(
        required=True, description="Data do evento (AAAA-MM-DD)", example="2025-10-20"
    ),
    "event_location": fields.String(
        description="Local do evento", example="Ginásio Principal do Campus"
    ),
    "description": fields.String(
        description="Descrição do evento",
        example="Feira anual de tecnologia apresentando projetos de alunos.",
    ),
}

event_summary_fields = {
    "id": fields.Integer(description="ID do evento"),
    "event_name": fields.String(description="Nome do evento"),
}

from .. import db
from datetime import datetime


class Interaction(db.Model):
    __tablename__ = "interaction"
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id", name="fk_interaction_student_id"),
        nullable=False,
        index=True,
    )
    event_id = db.Column(
        db.Integer,
        db.ForeignKey("event.id", name="fk_interaction_event_id"),
        nullable=False,
        index=True,
    )

    interaction_date = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint(
            "student_id", "event_id", name="uq_student_event_interaction"
        ),
    )

    def __repr__(self):
        return f"<Interaction StudentID:{self.student_id} EventID:{self.event_id}>"

    def to_dict(self):
        student_name = self.student.full_name if self.student else None
        event_name = self.event.event_name if self.event else None

        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": student_name,
            "event_id": self.event_id,
            "event_name": event_name,
            "interaction_date": (
                self.interaction_date.isoformat() if self.interaction_date else None
            ),
        }

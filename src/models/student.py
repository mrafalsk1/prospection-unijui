from .. import db
from datetime import datetime


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow()
    )

    school_id = db.Column(
        db.Integer,
        db.ForeignKey("school.id", name="fk_student_school_id"),
        nullable=True,
        index=True,
    )
    main_formation_id = db.Column(
        db.Integer,
        db.ForeignKey("formation.id", name="fk_student_main_formation_id"),
        nullable=True,
        index=True,
    )

    school = db.relationship("School", backref=db.backref("students", lazy="dynamic"))
    main_formation = db.relationship(
        "Formation", backref=db.backref("interested_students", lazy="dynamic")
    )

    interactions = db.relationship(
        "Interaction", backref="student", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Student {self.full_name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "school_id": self.school_id,
            "school_name": self.school.name if self.school else None,
            "main_formation_id": self.main_formation_id,
            "main_formation_name": (
                self.main_formation.name if self.main_formation else None
            ),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

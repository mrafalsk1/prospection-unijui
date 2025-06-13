from .. import db
from datetime import datetime


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(150), nullable=False, index=True)
    event_date = db.Column(db.Date, nullable=False)
    event_location = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    interactions = db.relationship(
        "Interaction", backref="event", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Event {self.event_name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "event_name": self.event_name,
            "event_date": self.event_date.isoformat() if self.event_date else None,
            "event_location": self.event_location,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

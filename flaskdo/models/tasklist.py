from ..core.database import db
from datetime import datetime


class TaskList(db.Document):
    name = db.StringField()
    description = db.StringField()
    owner_id = db.StringField()
    created_at = db.DateTimeField(default=datetime.utcnow())


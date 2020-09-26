from ..core.database import db
from datetime import datetime

class Task(db.Document):
    title = db.StringField()
    description = db.StringField()
    created_at = db.DateTimeField(default=datetime.utcnow())
    tasklist_id = db.StringField()
    task_id = db.StringField()
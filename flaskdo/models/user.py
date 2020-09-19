from ..core.database import db
from ..models.tasklist import TaskList


class User(db.Document):
    username = db.StringField()
    email = db.StringField()
    password = db.StringField()
    first_name = db.StringField()
    last_name = db.StringField()
    address = db.StringField()
    tasklists = db.ListField(db.StringField())
    # user_id =db.StringField()
    # TIMESTAMP = db.DateTimeField(default=datetime.utcnow())

    def add_tasklist(self, tasklist_id):
        self.tasklists.append(tasklist_id)

    def authenticate(self, password):
        # self.password (DB) == password (form)
        if self.password == password:
            return True
        else:
            return False

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': str(self.mongo_id),
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'tasklists': self.tasklists,
    
            # 'TIMESTAMP': self.TIMESTAMP
        }
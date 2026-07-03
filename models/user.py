from database.db import db,login_manager
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin,db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False, unique=True)

    email = db.Column(db.String(150), nullable=False, unique=True)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.Enum("admin", "teacher"),
        nullable=False,
        default="admin",
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    def __repr__(self):
        return f"<User {self.username}>"
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
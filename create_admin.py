from werkzeug.security import generate_password_hash

from app import app
from database.db import db
from models.user import User

with app.app_context():

    # Check if admin already exists
    admin = User.query.filter_by(username="admin").first()

    if admin:
        print("Admin already exists.")

    else:
        admin = User(
            username="admin",
            email="admin@gmail.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully!")
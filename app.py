from flask import Flask
from flask_migrate import Migrate

from config import Config
from database.db import db, login_manager
from routes.auth import auth
# from routes.dashboard import dashboard
from routes.main import main
from routes.marks import marks
from routes.report import report
from routes.student import student
from routes.subject import subject


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    login_manager.login_message = "Please login first."

    Migrate(app, db)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(student)
    app.register_blueprint(subject)
    app.register_blueprint(marks)
    app.register_blueprint(report)
    # app.register_blueprint(dashboard)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

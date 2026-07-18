import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Render PostgreSQL provides DATABASE_URL
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # Render may use postgres:// instead of postgresql://
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1
        )

        SQLALCHEMY_DATABASE_URI = database_url

    else:
        password = quote_plus(os.getenv("DB_PASSWORD", ""))

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://"
            f"{os.getenv('DB_USER')}:"
            f"{password}@"
            f"{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )

    SCHOOL_NAME = "ABC Public School"
    SCHOOL_ADDRESS = "Navi Mumbai, Maharashtra"
    SCHOOL_PHONE = "+91-9876543210"
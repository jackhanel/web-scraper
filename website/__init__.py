from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_APP_SECRET_KEY")

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app

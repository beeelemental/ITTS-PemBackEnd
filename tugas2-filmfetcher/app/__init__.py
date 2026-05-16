from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.main_routes import main_bp
    from app.routes.discover_routes import discover_bp
    from app.routes.film_routes import film_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(discover_bp)
    app.register_blueprint(film_bp)

    return app
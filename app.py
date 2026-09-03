from flask import Flask, jsonify
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from models import db
from routes.user_routes import user_bp
from routes.product_routes import product_bp
from routes.order_routes import order_bp
from routes.category_routes import category_bp
from routes.auth_routes import auth_bp

load_dotenv()


def create_app(config_overrides=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Allow tests (or other callers) to override config, e.g. use a test database
    if config_overrides:
        app.config.update(config_overrides)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # Register Blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return jsonify({"message": "Flask is connected to PostgreSQL!", "status": "ok"})

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)

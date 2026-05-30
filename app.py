# Flask Photobooth Application Entrypoint
from flask import Flask
from core.config import Config
from core.database import db, login_manager
from core.models import User, Photo
from core.routes.auth import auth_bp
from core.routes.user import user_bp
from core.routes.admin import admin_bp
from core.routes.photo import photo_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inisialisasi Extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(photo_bp)

    # Pastikan folder upload tersedia
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    return app

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Simple migration for profile_pic column
        try:
            db.session.execute(db.text('ALTER TABLE user ADD COLUMN profile_pic VARCHAR(200)'))
            db.session.commit()
        except Exception:
            db.session.rollback()

    app.run(debug=True)

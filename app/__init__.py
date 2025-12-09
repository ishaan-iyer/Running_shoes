from .extensions import app, db, login_manager, bcrypt
from .auth.routes import auth as auth_bp
from .main.routes import main as main_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
from app.extensions import app, db
from app.main.routes import main
from app.auth.routes import auth

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

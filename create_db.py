from app import create_app, db
from app.models import User, Property

app = create_app()

with app.app_context():
    db.create_all()

print("База данных создана!")
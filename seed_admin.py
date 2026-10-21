"""
Script untuk membuat / mengubah user menjadi admin.

Cara pakai (dari folder module-2-galeriqbal, dengan venv aktif):
    python seed_admin.py

Default membuat admin: admin@revoshop.com / 123456
Kalau email sudah ada, user tersebut di-set jadi admin.
"""

from werkzeug.security import generate_password_hash
from app import create_app
from models import db, User

ADMIN_NAME = "Admin"
ADMIN_EMAIL = "admin@revoshop.com"
ADMIN_PASSWORD = "123456"


def seed_admin():
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email=ADMIN_EMAIL).first()

        if user:
            user.role = "admin"
            user.password_hash = generate_password_hash(ADMIN_PASSWORD)
            db.session.commit()
            print(f"User '{ADMIN_EMAIL}' diupdate jadi admin.")
        else:
            admin = User(
                name=ADMIN_NAME,
                email=ADMIN_EMAIL,
                password_hash=generate_password_hash(ADMIN_PASSWORD),
                role="admin",
            )
            db.session.add(admin)
            db.session.commit()
            print(f"Admin baru dibuat: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")


if __name__ == "__main__":
    seed_admin()

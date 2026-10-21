"""
Seeder item-item Trinity untuk fitur promo bundling.

Cara pakai (dari folder module-2-galeriqbal, venv aktif):
    python seed_trinity.py

Item yang sudah ada (cocok by nama) akan dilewati, tidak diduplikasi.
"""

from app import create_app
from models import db, Product

# name, price (harga dasar), stock, description
TRINITY_ITEMS = [
    # Trinity Attack Speed / Marksman
    ("Corrosion Scythe", 1850, 30, "Memberi efek slow dan bonus attack speed bertingkat saat menyerang."),
    ("Demon Hunter Sword", 2050, 30, "Damage tambahan berdasarkan HP lawan, ampuh melawan tank."),
    ("Golden Staff", 1900, 30, "Mempercepat dan menggandakan efek pasif item serangan lain."),
    # Trinity Magic
    ("Ice Queen Wand", 2240, 25, "Memberi efek slow pada skill yang mengenai lawan."),
    ("Glowing Wand", 2010, 25, "Menambahkan efek bakar yang mengurangi HP lawan tiap detik."),
    ("Genius Wand", 2080, 25, "Mengurangi magic defense lawan yang terkena skill."),
    # Trinity Sustain / Fighter
    ("War Axe", 1900, 28, "Menambah physical attack dan efek penetrasi saat bertarung."),
    ("Brute Force Breastplate", 1950, 28, "Memberi bonus movement speed dan pertahanan tiap serangan."),
    ("Queen's Wings", 2050, 28, "Mengurangi damage besar dan memberi lifesteal saat HP rendah."),
    # Trinity Tank / Roamer
    ("Dominance Ice", 2010, 26, "Mengurangi attack speed dan mana lawan di sekitar."),
    ("Antique Cuirass", 1920, 26, "Mengurangi physical attack lawan yang menyerang."),
    ("Radiant Armor", 1740, 26, "Mengurangi sustained magic damage dari lawan."),
]


def seed_trinity():
    app = create_app()
    with app.app_context():
        added = 0
        skipped = 0
        for name, price, stock, description in TRINITY_ITEMS:
            existing = Product.query.filter_by(name=name).first()
            if existing:
                skipped += 1
                continue
            product = Product(
                name=name,
                price=price,
                stock=stock,
                description=description,
                categories_id=None,
            )
            db.session.add(product)
            added += 1

        db.session.commit()
        print(f"Selesai. Ditambahkan: {added}, dilewati (sudah ada): {skipped}")


if __name__ == "__main__":
    seed_trinity()

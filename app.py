from flask import Flask, jsonify, request
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from models import db, User, Order, Product, order_items

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# TODO 3: Initialize SQLAlchemy with the app
db.init_app(app)
migrate = Migrate(app, db)

products = [
    {"id": 1, "categories_id": 1, "name": "Blade of Despair", "price": 10000, "stock": 25, "description": "Physical Attack tinggi dengan bonus damage saat musuh HP rendah."},
    {"id": 2, "categories_id": 1, "name": "Malefic Roar", "price": 8000, "stock": 30, "description": "Physical Penetration tinggi untuk menembus armor lawan."},
    {"id": 3, "categories_id": 1, "name": "Berserker's Fury", "price": 7500, "stock": 20, "description": "Critical Damage dan Critical Chance tinggi."},
    {"id": 4, "categories_id": 1, "name": "Hunter Strike", "price": 6000, "stock": 18, "description": "Memberikan Physical Penetration dan Movement Speed."},
    {"id": 5, "categories_id": 1, "name": "Sea Halberd", "price": 9250, "stock": 15, "description": "Mengurangi efek regen dan lifesteal musuh."},
    {"id": 6, "categories_id": 2, "name": "Holy Crystal", "price": 25000, "stock": 22, "description": "Meningkatkan Magic Power secara signifikan."},
    {"id": 7, "categories_id": 2, "name": "Lightning Truncheon", "price": 12500, "stock": 19, "description": "Memberikan damage petir tambahan setiap beberapa detik."},
    {"id": 8, "categories_id": 2, "name": "Genius Wand", "price": 7500, "stock": 17, "description": "Mengurangi Magic Defense target."},
    {"id": 9, "categories_id": 2, "name": "Blood Wings", "price": 3000, "stock": 12, "description": "Magic Power sangat tinggi dengan tambahan HP."},
    {"id": 10, "categories_id": 2, "name": "Divine Glaive", "price": 8000, "stock": 14, "description": "Magic Penetration tinggi terhadap target dengan Magic Defense besar."},
    {"id": 11, "categories_id": 3, "name": "Athena Shield", "price": 8800, "stock": 20, "description": "Memberikan Magic Damage Reduction setelah menerima serangan."},
    {"id": 12, "categories_id": 3, "name": "Blade Armor", "price": 5900, "stock": 16, "description": "Memantulkan sebagian Basic Attack lawan."},
    {"id": 13, "categories_id": 3, "name": "Antique Cuirass", "price": 12350, "stock": 13, "description": "Mengurangi Physical Attack musuh yang menyerang."},
    {"id": 14, "categories_id": 3, "name": "Dominance Ice", "price": 6000, "stock": 21, "description": "Mengurangi Attack Speed dan Shield/Regen lawan."},
    {"id": 15, "categories_id": 4, "name": "Radiant Armor", "price": 9400, "stock": 18, "description": "Efektif melawan Magic Damage bertipe DPS."},
    {"id": 16, "categories_id": 4, "name": "Oracle", "price": 7250, "stock": 15, "description": "Meningkatkan efek Shield dan HP Regen."},
    {"id": 17, "categories_id": 4, "name": "Cursed Helmet", "price": 4750, "stock": 11, "description": "Memberikan Magic Damage area kepada musuh di sekitar."},
    {"id": 18, "categories_id": 5, "name": "Warrior Boots", "price": 2400, "stock": 40, "description": "Sepatu dengan tambahan Physical Defense."},
    {"id": 19, "categories_id": 5, "name": "Tough Boots", "price": 3000, "stock": 38, "description": "Sepatu dengan tambahan Magic Defense dan CC Reduction."},
    {"id": 20, "categories_id": 5, "name": "Arcane Boots", "price": 2690, "stock": 35, "description": "Sepatu dengan tambahan Magic Penetration."},
]

@app.route('/')
def index():
    return jsonify({"message": "Flask is connected to PostgreSQL!", "status": "ok"})

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "name, email, and password are required"}), 400

    new_user = User(
        name=data['name'],
        email=data['email'],
        password_hash=data['password']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None
    })

@app.route('/seed-order', methods=['POST'])
def seed_order():
    # Insert sample data: 1 order linked to multiple products (many-to-many)
    order = Order(user_id=1, total_prices=25500)
    db.session.add(order)
    db.session.flush()  # get order.id before inserting into order_items

    # Link this order to 3 products via order_items
    db.session.execute(order_items.insert().values([
        {"order_id": order.id, "product_id": 1, "quantity": 1, "product_price": 10000},
        {"order_id": order.id, "product_id": 6, "quantity": 1, "product_price": 25000},
        {"order_id": order.id, "product_id": 18, "quantity": 1, "product_price": 2400},
    ]))

    db.session.commit()

    return jsonify({
        "message": "Order created with multiple products (many-to-many)",
        "order_id": order.id,
        "products_linked": [1, 6, 18]
    }), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404

    # Query order_items to show the many-to-many data
    items = db.session.execute(
        order_items.select().where(order_items.c.order_id == order_id)
    ).fetchall()

    return jsonify({
        "order_id": order.id,
        "user_id": order.user_id,
        "total_prices": float(order.total_prices) if order.total_prices else None,
        "products": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "product_price": float(item.product_price) if item.product_price else None
            } for item in items
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)

# Importação
from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# UserMixin já possui métodos de usuários definidos
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


app = Flask(__name__)

app.config['SECRET_KEY'] = "minha_chave_123"
# falar onde está nosso banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
# Iniciando a conexão com o banco
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
# usado com swager 
CORS(app)


# modelagem
# User (id, username, password)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)
    cart = db.relationship('CartItem', backref='user', lazy=True)


# Produto(id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False) # 4.20, 1.99
    description = db.Column(db.Text, nullable=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


# Autenticação
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(username=data.get("username")).first() #-> usado quando voce quer filtrar um registro por uma coluna diferente do 'id'

    if user and data.get("password") == user.password:
            login_user(user)
            return jsonify({"message": "Logged in sucessufuly"})
    
    return jsonify({"message": "Unauthorized. Invalid credentials"}), 401
    
@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successfully"})


# rota da api, mode:lo de produtos, operação add
@app.route('/api/products/add', methods=["POST"])
@login_required 
def add_product():
    # quando o cliente vai mandar um payload (chave : valor)
    data = request.json
    # verifica se existe nome e preço
    if 'name' in data and 'price' in data:
        # MODELO
        # achar os valores de 'data'. O get ele vai tentar procurar o valor passado, 
        # caso não ache ele vai retornar o que voce colocou
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        # adiciona o produto
        db.session.add(product)
        # commit
        db.session.commit()
        return jsonify({'message': "Product added sucessfully"})
    return jsonify({'message': "Invalid product data"}), 400#-> dados do produto invalido

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit() 
        return jsonify({'message': "Product deleted sucessfully"})
    return jsonify({'message': "Product not found"}), 404 #-> não encontrado

@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message": "Product not found"}), 404

@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    data = request.json
    if 'name' in data:
        product.name = data['name']

    if 'price' in data:
        product.price = data['price']

    if 'description' in data:
        product.description = data['description']

    # aqui o que voce precisa fazer é apenas um commit para que atualize o banco de dados
    db.session.commit()
    return jsonify({'message': 'Product update successufully'})

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
        product_list.append(product_data)
    return jsonify(product_list)

# adicionar ao carrinho
@app.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    # Usuário
    user = User.query.get(int(current_user.id))
    # Produto
    product = Product.query.get(product_id)

    if user and product:
        cart_item = CartItem(user_id=user.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message': "Item added to the cart successfully"})
    return jsonify({'message': "Failed to add item to the cart"}), 400

# remover do carrinho
@app.route('/api/cart/remove/<int:product_id>', methods=["DELETE"])
@login_required
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': "Item removed from the cart successfully"})
    return jsonify({'message': "Failed to remove item from the cart"}), 400
    
# visualização do carrinho
@app.route('/api/cart', methods=["GET"])
@login_required
def view_cart():
    # Usuário
    user = User.query.get(int(current_user.id))
    cart_items = user.cart
    cart_content = []
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        cart_content.append({
            "id": cart_item.id,
            "user_id": cart_item.user_id,
            "product_id": cart_item.product_id,
            "product_name": product.name,
            "product_price": product.price
        })
    return jsonify(cart_content)

# Checkout
@app.route('/api/cart/checkout', methods=["POST"])
@login_required
def checkout():
    user = User.query.get(int(current_user.id))
    cart_items = user.cart
    for cart_item in cart_items:
        db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'checkout successful. Cart has been cleared.'})


if __name__ == "__main__":
    app.run(debug=True)

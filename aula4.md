# Construção da API de E-commerce

## vamos criar um model que será nosso carrinho
- o cliente tem direito a um carrinho só
- vamos utilizar os produtos cadastrados no e-commerce
- precisamos saber quem é o usuário que está adicionando ao carrinho

## Criando a classe CarItem

        class CartItem(db.Model):
            id = db.column(db.Integer, primary_key = True)
            user_id = db.column(db.Integer, db.ForeignKey('user.id'), nullable=False)
            product_id = db.column(db.Integer, db.ForeignKey('product.id'), nullable=False)

## alterando classe User

        class User(db.Model, UserMixin):
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(80), nullable=False, unique=True)
            password = db.Column(db.String(80), nullable=True)
            cart = db.relationship('CartItem', backref='user', lazy=True)

## subindo as tabelas novamente

        db.drop_all()
        db.create_all()
        user = User(username="admin", password="123")
        db.session.add(user)
        db.session.commit()
        exit()

## importando current user

        from flask_login import current_user

    - essa biblioteca vai nos dar acesso ao usuário que está logado no momento

## criando a rota /api/cart/add

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


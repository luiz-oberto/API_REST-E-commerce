# Autenticação do usuário

## Rota para ver os detalhes do produto
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

## Rota para alterar/atualizar as informações do produto
    @app.route('/api/products/update/<int:product_id>', methods=["PUT"])
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

## criando classe usuário
- primeiro, faça a importação

        from flask_login import UserMixin
        # UserMixin já possui métodos de usuários definidos

- adicionando a classe User

        class User(db.Model, UserMixin):
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(80), nullable=False, unique=True)
            password = db.Column(db.String(80), nullable=True)

## Criando a tabela de usuários
- no terminal inicie 'flask shell'
-digite: 
        db.drop_all()  --> limpa todo o banco de dados (tabelas)
        db.create_all() --> cria tudo de novo
        db.session.commit() --> roda os comandos no banco de dados
        exit()
 
## criando usuário
- flask shell novamente no terminal
        
        user = User(username="admin", password="123")
        user
        <User (transient 2179625625904)>
        db.session.add(user) --> adicionar usuário
        db.session.commit() --> rodar no banco de dados
        exit()

## Criando rota do usuário

        @app.route('/login', methods=["POST"])
        def login():
        data = request.json

        user = User.query.filter_by(username=data.get("username")).first() 
        #-> usado quando voce quer filtrar um registro por uma coluna diferente do 'id'

        if user and data.get("password") == user.password:
                return jsonify({"message": "Logged in sucessufuly"})
        
        return jsonify({"message": "Unauthorized. Invalid credentials"}), 401

## importando login_user e LoginManager

        from flask_login import UserMixin, login_user, LoginManager

- essas duas bibliotecas vão nos ajudar a fazer definitivamente o login do usuário

## login_required
- mais uma importação que vai nos ajudar a obrigar o usuário a estar autenticado para que acesse determinadas rotas

## user_loader
- precisamos utilizar junto com login_required

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

- o login_required precisa recuperar qual é o usuário que está tentando acessar a rota, para isso ele utiliza o user_loader com uma função load_user que vai retornar o registro do usuário
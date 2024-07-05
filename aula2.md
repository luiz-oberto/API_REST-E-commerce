''' Criando o banco de dados '''

# falar onde está nosso banco de dados
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

# Iniciando a conexão com o banco
# db = SQLAlchemy(app)


# modelagem
# Produto(id, name, price, description)
# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), nullable=False)
#     price = db.Column(db.Float, nullable=False) # 4.20, 1.99
#     description = db.Column(db.Text, nullable=True)

# Agora vamos criar nosso bd
# vá em Terminal -> new Terminal -> no terminal digite: 'flask shell'
# ele vai abri um temrinal do flask, agora digite db.create_all() para criar o banco de dados
# se não deu retorno é porque não deu erro
# agora digite db.session.commit() que vai efetivar as mudanças no banco
# exit() para sair

# rota da api, modelo de produtos, operação add
# @app.route('/api/products/add', methods=["POST"])
# def add_product():
#     # quando o cliente vai mandar um payload (chave : valor)
#     data = request.json
#     return data

# Agora execute o arquivo no vscode
# seu site vai subir e vá para o postman
# No Postman, você vai na varra lateral em 'environments'
# clique em 'new', depois no '+' e digite o nome do ambiente, nesse caso: API  ecommerce LOCAL

# # rota da api, modelo de produtos, operação add
# @app.route('/api/products/add', methods=["POST"])
# def add_product():
#     # quando o cliente vai mandar um payload (chave : valor)
#     data = request.json
#     # verifica se existe nome e preço
#     if 'name' in data and 'price' in data:
#         # MODELO
#         # achar os valores de 'data'. O get ele vai tentar procurar o valor passado, caso não ache ele vai retornar o que voce colocou
#         product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
#         # adiciona o produto
#         db.session.add(product)
#         # commit
#         db.session.commit()
#         return jsonify({'message': "Product added sucessfully"})
#     return jsonify({'message': "Invalid product data"}), 400#-> dados do produto invalido

# @app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
# def delete_product(product_id):
#     # Recuperar o produto
#     # Verificar se o produto existe
#     # Se existe, apagar da base de dados
#     # Se não existe, retornar 404 not found
#     product = Product.query.get(product_id)
#     if product:
#         db.session.delete(product)
#         db.session.commit() 
#         return jsonify({'message': "Product deleted sucessfully"})
#     return jsonify({'message': "Product not found"}), 404 #-> não encontrado
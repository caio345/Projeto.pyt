from bson import ObjectId
from flask import Flask, jsonify, request
from config import bd, pedidos_collection, produtos_collection, clientes_collection

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World."

#Declarar classes
class Clientes():
    def __init__(self, id_cliente, nome, data_nascimento, email, cpf,):
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.data_nascimento = data_nascimento
    
    def serialize(self):
        return{
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "email": self.email,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento,
        }

class Produtos():
    def __init__(self,id_produto,nome,descricao,preco,categoria):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria

    def serialize(self):
        return{
            "id_produto": self.id_produto,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "categoria": self.categoria,
        }
    
class Pedidos():
    def __init__(self,id_produto,data_pedido,id_cliente,valor,pedido_id):
        self.id_produto = id_produto
        self.id_cliente = id_cliente
        self.data_pedido = data_pedido
        self.pedido_id = pedido_id
        self.valor = valor

    def serialize(self):
        return{
            "id_produto": self.id_produto,
            "id_cliente": self.id_cliente,
            "data_pedido": self.data_pedido,
            "pedido_id": self.pedido_id,
            "valor": self.valor,
        }

#Rotas para Clientes

@app.route("/clientes", methods=["GET"])
def lista_clientes():
    try:
        clientes = clientes_collection.find()

        clientes_serializado = []
        for cliente in clientes:
            cliente['_id'] = str(cliente['_id'])
            clientes_serializado.append(cliente)
        
        return jsonify(clientes_serializado), 200

    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao listar clientes", 500


@app.route("/insertCliente", methods=["POST"])
def set_cliente():
    dados = request.get_json()
    novo_cliente = Clientes(
        id_cliente = dados['id_cliente'],
        nome= dados['nome'],
        email= dados['email'],
        cpf= dados['cpf'],
        data_nascimento = dados['data_nascimento']
    )

    resultado = clientes_collection.insert_one(novo_cliente.serialize())

    if resultado.inserted_id:
        novo_cliente.id_cliente = str(resultado.inserted_id)
        return jsonify (novo_cliente.serialize()),201
    else:
        return "Erro ao inserir cliente.", 500

@app.route("/alterarCliente/<id_cliente>", methods=["PUT"])
def update_cliente(id_cliente):
    try:
        dados = request.get_json()

         
        id_cliente = int(id_cliente)

        
        resultado_busca = clientes_collection.find_one({"id_cliente": id_cliente})

        if resultado_busca:
            _id = resultado_busca["_id"]

            
            resultado_atualizacao = clientes_collection.update_one(
                {"_id": _id},
                {"$set": dados}
            )

            if resultado_atualizacao.modified_count == 1:
                return f"Cliente {id_cliente} atualizado com sucesso.", 200
            else:
                return f"Erro ao atualizar cliente.", 500
        else:
            return f"Cliente com id {id_cliente} não encontrado.", 404

    except Exception as e:
        return f"Erro ao atualizar cliente: {e}", 500

@app.route("/excluiCliente/<id_cliente>", methods=["DELETE"])
def delete_cliente(id_cliente):
    try:
        # Converter o id_cliente 
        id_cliente = int(id_cliente)

        # Buscar o documento 
        resultado_busca = clientes_collection.find_one({"id_cliente": id_cliente})

        if resultado_busca:
            _id = resultado_busca["_id"]

            resultado = clientes_collection.delete_one(
                {"_id": _id}
            )

            if resultado.deleted_count == 1:
                return f"Cliente {id_cliente} excluido com sucesso.", 200
            else:
                return f"Cliente com id {id_cliente} não encontrado.", 404
    except Exception as e:
        return f"Erro ao excluir cliente: {e}", 500


@app.route("/produtos", methods=["GET"])
def lista_produtos():
    try:
        produtos = produtos_collection.find()

        produtos_serializado = []
        for produto in produtos:
            produto['_id'] = str(produto['_id'])
            produtos_serializado.append(produto)
        
        return jsonify(produtos_serializado), 200

    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao listar produtos.", 500

@app.route("/inserirProduto", methods=['POST'])
def set_produto():
    dados = request.get_json()


    novo_produto = Produtos(
        id_produto=dados['id_produto'],
        nome=dados['nome'],
        categoria=dados['categoria'],
        preco=dados['preco'],
        descricao=dados["descricao"]
    )

    resultado = produtos_collection.insert_one(novo_produto.serialize())

    if  resultado.inserted_id:
        novo_produto.id_produto = str(resultado.inserted_id)
        return jsonify(novo_produto.serialize()), 201
    else:
        return "Erro ao inserir produto.", 500

@app.route("/alteraProduto/<id_produto>", methods=["PUT"])
def update_produto(id_produto):
    try:
        dados = request.get_json()

        
        id_produto = int(id_produto)

        
        resultado_busca = produtos_collection.find_one({"id_produto": id_produto})

        if resultado_busca:
            _id = resultado_busca["_id"]

           
            resultado_atualizacao = produtos_collection.update_one(
                {"_id": _id},
                {"$set": dados}
            )

            if resultado_atualizacao.modified_count == 1:
                return f"produto {id_produto} atualizado com sucesso.", 200
            else:
                return f"Erro ao atualizar produto.", 500
        else:
            return f"produto com id {id_produto} não encontrado.", 404

    except Exception as e:
        return f"Erro ao atualizar produto: {e}", 500

@app.route("/excluiproduto/<id_produto>", methods=["DELETE"])
def delete_produto(id_produto):
    try:

        
        id_produto = int(id_produto)

        
        resultado_busca = produtos_collection.find_one({"id_produto": id_produto})

        if resultado_busca:
            _id = resultado_busca["_id"]

            resultado = produtos_collection.delete_one(
                {"_id": _id}
            )
            print(resultado)
            if resultado.deleted_count == 1:
                return f"produto {id_produto} excluido com sucesso.", 200
            else:
                return f"produto com id {id_produto} não encontrado.", 404

    except Exception as e:
        return f"Erro ao excluir produto: {e}", 500

@app.route("/inserirPedidos", methods=['POST'])
def set_pedido():
    try:
        dados = request.get_json()

        id_cliente = dados.get('id_cliente')
        id_produto = dados.get('id_produto')
        data_pedido = dados.get('data_pedido')
        pedido_id = dados.get('pedido_id')
        valor = dados.get('valor')

        # Verificação do cliente
        cliente = clientes_collection.find_one({"id_cliente": id_cliente})
        if not cliente:
            return jsonify({"error": "Cliente não encontrado"}), 404

        # Verificação do produto
        produto = produtos_collection.find_one({"id_produto": id_produto})
        if not produto:
            return jsonify({"error": "Produto não encontrado"}), 404

        # Novo pedido
        novo_pedido = Pedidos(
                id_produto=id_produto,
                data_pedido=data_pedido,
                id_cliente=id_cliente,
                pedido_id=pedido_id,
                valor=valor
            )
        resultado = pedidos_collection.insert_one(novo_pedido.serialize())

        if resultado.inserted_id:
            return jsonify({"Pedido criado com sucesso": str(resultado.inserted_id)}), 201
        else:
            return jsonify({"Erro ao criar pedido"}), 500
    except Exception as e:
        print(f"Erro ao criar pedido: {e}")
        return jsonify({"error": f"Erro ao criar pedido {str(e)}"}), 500


@app.route("/atualizarPedidos/<pedido_id>", methods=['PUT'])
def update_pedido(pedido_id):
    try:
        dados = request.get_json()

        id_cliente = dados.get('id_cliente')
        id_produto = dados.get('id_produto')


        # Conversão do id 
        pedido_id = int(pedido_id)
        

        # Verificação do pedido
        pedido = pedidos_collection.find_one({"pedido_id": pedido_id})

        if pedido:
            _id = pedido["_id"]

            resultado = pedidos_collection.update_one(
            {"_id": _id}, 
            {"$set": dados}
        )

        if not pedido:
            return jsonify({"error": "Pedido não encontrado"}), 404

        # Verificação do cliente
        if id_cliente:
            cliente = clientes_collection.find_one({"id_cliente": id_cliente})
            if not cliente:
                return jsonify({"error": "Cliente não encontrado"}), 404

        # Verificação do produto
        if id_produto:
            produto = produtos_collection.find_one({"id_produto": id_produto})
            if not produto:
                return jsonify({"error": "Produto não encontrado"}), 404


        if resultado.modified_count > 0:
            return jsonify({"message": "Pedido atualizado com sucesso"}), 200
        else:
            return jsonify({"error": "Erro ao atualizar pedido"}), 500
        
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar pedido: {e}"}), 500

@app.route("/deletarPedidos/<pedido_id>", methods=['DELETE'])
def delete_pedido(pedido_id):
    try:

        
        pedido_id = int(pedido_id)

        
        pedido = pedidos_collection.find_one({"pedido_id": pedido_id})

        if not pedido:
            return jsonify({"error": "Pedido não encontrado"}), 404

        # excluir o pedido
        if pedido:
            _id = pedido["_id"]


            resultado = pedidos_collection.delete_one(
                {"_id": _id}
            )

            if resultado.deleted_count > 0:
                return jsonify({"message": "Pedido removido com sucesso"}), 200
            else:
                return jsonify({"error": "Erro ao remover pedido"}), 500
        
    except Exception as e:
        return f"Erro ao excluir pedido: {e}", 500
    
@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    try:
        pedidos = pedidos_collection.find()

        pedidos_serializado = []
        for pedido in pedidos:
            pedido['_id'] = str(pedido['_id'])
            pedidos_serializado.append(pedido)
        
        return jsonify(pedidos_serializado), 200


    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao listar pedidos.", 500

    
if __name__ == "__main__":
    app.run(debug=True)
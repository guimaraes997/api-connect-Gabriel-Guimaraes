from flask import Blueprint, request, jsonify
import json
# Importando as lógicas que foi criada no controller
from controllers.user_controller import carregar_usuarios, gerar_novo_id, FILE_PATH

# Criando um agrupador de rotas para organizar o código
user_routes = Blueprint('user_routes', __name__)

# 1. Rota GET - Listar todos os usuários
@user_routes.route('/users', methods=['GET'])
def listar_usuarios():
    usuarios = carregar_usuarios()
    return jsonify(usuarios), 200

# 2. Rota POST - Cadastrar novo usuário (Com Validação)
@user_routes.route('/users', methods=['POST'])
def criar_usuario():
    usuarios = carregar_usuarios()
    novo_usuario = request.get_json()
    
    # Validação: checa se os campos obrigatórios estão ausentes
    if 'nome' not in novo_usuario or 'email' not in novo_usuario:
        return jsonify({"error": "Nome e e-mail são obrigatórios"}), 400
    
    # Atribui o ID
    novo_usuario['id'] = gerar_novo_id(usuarios)
    
    # Adiciona na memória e salva no JSON
    usuarios.append(novo_usuario)
    with open(FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(usuarios, file, indent=4)
        
    # Retorno de sucesso envelopado na chave "data"
    return jsonify({"data": novo_usuario}), 201

# 3. Rota GET por ID - Buscar um usuário específico
@user_routes.route('/users/<int:id>', methods=['GET'])
def buscar_usuario(id):
    usuarios = carregar_usuarios()
    
    # Fazemos um loop (for) para olhar cada usuário dentro da nossa lista
    for usuario in usuarios:
        # Verifica se o ID do usuário atual é igual ao ID que veio na URL
        if usuario.get('id') == id:
            # Encontramos! Retorna os dados do usuário e o status 200 (OK)
            return jsonify(usuario), 200
        
    return jsonify({"erro": "Usuário não encontrado"}), 404
            

    # 4. Rota PUT - Atualizar um usuário existente
@user_routes.route('/users/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    usuarios = carregar_usuarios()
    novos_dados = request.get_json()
    
    # enumerate  dá a posição (i) e os dados (usuario)
    for i, usuario in enumerate(usuarios):
        if usuario.get('id') == id:
            # Atualiza os dados do usuário na posição 'i'
            usuarios[i].update(novos_dados)
            # Garantindo que o ID original não seja sobrescrito sem querer
            usuarios[i]['id'] = id
            
            # Salva no arquivo JSON
            with open(FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(usuarios, file, indent=4)
                
            return jsonify(usuarios[i]), 200
            
    return jsonify({"erro": "Usuário não encontrado"}), 404

# 5. Rota DELETE - Remover um usuário
@user_routes.route('/users/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuarios = carregar_usuarios()
    
    for i, usuario in enumerate(usuarios):
        if usuario.get('id') == id:
            # Remove o usuário da lista usando a posição 'i'
            usuarios.pop(i)
            
            # Salva a nova lista (sem o usuário) no arquivo JSON
            with open(FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(usuarios, file, indent=4)
                
            # Retornamos 200 com uma mensagem de sucesso
            return jsonify({"mensagem": "Usuário deletado com sucesso"}), 200
            
    return jsonify({"erro": "Usuário não encontrado"}), 404

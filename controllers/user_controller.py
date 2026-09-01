import json
import os

# Caminho para o nosso "banco de dados" provisório
FILE_PATH = 'data/users.json'

def carregar_usuarios():
    """Lê o arquivo JSON e retorna a lista de usuários. Se não existir, retorna lista vazia."""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def gerar_novo_id(usuarios):
    """Gera um ID sequencial analisando o maior ID atual na lista."""
    if len(usuarios) == 0:
        return 1 # Se a lista estiver vazia, o primeiro ID é 1
    
    # Percorre a lista, encontra o maior valor da chave 'id' e soma 1
    maior_id = max(usuario.get('id', 0) for usuario in usuarios)
    return maior_id + 1
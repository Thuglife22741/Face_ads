import re

def corrigir_json(arquivo_origem, arquivo_destino):
    with open(arquivo_origem, 'r', encoding='utf-8') as file:
        conteudo = file.read()
    
    # Substitui aspas simples por aspas duplas
    conteudo_corrigido = re.sub(r"'", r'"', conteudo)
    
    with open(arquivo_destino, 'w', encoding='utf-8') as file:
        file.write(conteudo_corrigido)

# Corrigir o arquivo JSON
corrigir_json('criacao/interesses/interests.txt', 'criacao/interesses/interests_corrigido.txt')

print("Arquivo JSON corrigido.")


# python criacao/interesses/formatar_interesses.py
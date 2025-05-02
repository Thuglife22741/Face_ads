import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

def search_facebook_pages(access_token, api_version, business_id):
    url = f"https://graph.facebook.com/v{api_version}/{business_id}/owned_pages"
    params = {
        'fields': 'id,name',
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching Facebook pages: {response.status_code} - {response.text}")

def search_instagram_accounts(access_token, api_version, business_id):
    url = f"https://graph.facebook.com/v{api_version}/{business_id}/instagram_accounts"
    params = {
        'fields': 'id,username',
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching Instagram accounts: {response.status_code} - {response.text}")

def save_to_file(data, filename):
    json_data = json.dumps(data, indent=4)  # Converte o dicionário em uma string JSON com aspas duplas
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json_data)

# Substitua pelos valores corretos
access_token = os.getenv("my_access_token")
api_version = '19.0'
business_id = os.getenv("business_id")  # Substitua pelo ID do seu Business Manager

# Buscando e salvando páginas do Facebook
facebook_pages = search_facebook_pages(access_token, api_version, business_id)
print("Facebook pages fetched:", facebook_pages)

# Buscando e salvando contas do Instagram
instagram_accounts = search_instagram_accounts(access_token, api_version, business_id)
print("Instagram accounts fetched:", instagram_accounts)

# Combinando as páginas do Facebook e contas do Instagram em um único dicionário
accounts_data = {
    'facebook_pages': facebook_pages,
    'instagram_accounts': instagram_accounts
}

# Salvando as informações no arquivo especificado
save_to_file(accounts_data, 'criacao/contas_facebook_e_instagram/contas_facebook_e_instagram.json')
print("Facebook pages and Instagram accounts saved to contas_facebook_e_instagram.json")

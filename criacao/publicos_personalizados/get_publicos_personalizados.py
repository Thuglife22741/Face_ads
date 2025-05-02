import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)


def search_custom_audiences(access_token, api_version, ad_account_id):  
    url = f"https://graph.facebook.com/v{api_version}/act_{ad_account_id}/customaudiences"  
    params = {  
        'fields': 'id,name',  # Inclui os campos 'id' e 'name'
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching custom audiences: {response.status_code} - {response.text}")

def search_lookalike_audiences(access_token, api_version, ad_account_id):
    url = f"https://graph.facebook.com/v{api_version}/act_{ad_account_id}/customaudiences"
    params = {
        'fields': 'id,name,lookalike_audience_ids',
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        lookalikes = [audience for audience in response.json()['data'] if 'lookalike_audience_ids' in audience]
        return lookalikes
    else:
        raise Exception(f"Error fetching lookalike audiences: {response.status_code} - {response.text}")

def save_to_file(data, filename):
    json_data = json.dumps(data, indent=4)  # Converte o dicionário em uma string JSON com aspas duplas
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json_data)

# Substitua pelos valores corretos
access_token = os.getenv("my_access_token")
api_version = '19.0'
ad_account_id = os.getenv("ad_account_id")  # Substitua pelo ID da sua conta de anúncios

# Buscando e salvando públicos personalizados
custom_audiences = search_custom_audiences(access_token, api_version, ad_account_id)
save_to_file(custom_audiences, 'criacao/publicos_personalizados/custom_audiences.json')
print("Custom audiences saved to custom_audiences.json")

# Buscando e salvando públicos semelhantes
lookalike_audiences = search_lookalike_audiences(access_token, api_version, ad_account_id)
save_to_file(lookalike_audiences, 'criacao/publicos_personalizados/lookalike_audiences.json')
print("Lookalike audiences saved to lookalike_audiences.json")

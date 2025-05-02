import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

def list_ad_accounts(access_token, business_id, api_version):
    url = f"https://graph.facebook.com/v{api_version}/{business_id}/owned_ad_accounts"
    params = {
        'access_token': access_token,
        'fields': 'id,name,account_status'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching ad accounts: {response.status_code} - {response.text}")

def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

access_token = os.getenv("my_access_token")
api_version = '19.0'
business_id = os.getenv("business_id") 

ad_accounts_data = list_ad_accounts(access_token, business_id, api_version)

# Filtrar apenas contas de anúncios ativas
active_ad_accounts = [{'id': account['id'], 'name': account['name']} 
                      for account in ad_accounts_data['data'] 
                      if account['account_status'] == 1]  # Status 1 indica que a conta está ativa

print(active_ad_accounts)

save_to_file(active_ad_accounts, 'criacao/ad_accounts/ad_accounts.txt')
print("Active ad accounts saved to ad_accounts.txt")

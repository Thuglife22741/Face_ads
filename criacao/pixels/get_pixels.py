import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)


def list_pixels(access_token, ad_account_id, api_version):
    url = f"https://graph.facebook.com/v{api_version}/act_{ad_account_id}/adspixels"
    params = {
        'access_token': access_token
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching pixels: {response.status_code} - {response.text}")

def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

access_token = os.getenv("my_access_token")
ad_account_id = os.getenv("ad_account_id") 
api_version = '19.0'

pixels_data = list_pixels(access_token, ad_account_id, api_version)

# Extrair IDs e nomes dos pixels
pixels = [{'id': pixel['id']} for pixel in pixels_data['data']]

print(pixels)

save_to_file(pixels, 'criacao/pixels/pixels.txt')
print("Pixels saved to pixels.txt")

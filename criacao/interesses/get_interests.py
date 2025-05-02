import requests
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

def search_interests(access_token, api_version):
    url = f"https://graph.facebook.com/v{api_version}/search"
    params = {
        'type': 'adTargetingCategory',
        'class': 'interests',
        'access_token': access_token
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching interests: {response.status_code} - {response.text}")

def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str(data))

access_token = os.getenv("my_access_token")
api_version = '19.0'

interests = search_interests(access_token, api_version)
save_to_file(interests, 'criacao/interesses/interests.json')
print("Interests saved to interests.txt")

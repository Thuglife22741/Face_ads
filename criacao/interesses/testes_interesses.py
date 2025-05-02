from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.targetingsearch import TargetingSearch

# Initialize the Facebook API with your credentials
access_token = 'EAAEZCawbJqnYBO7cCXk5p6OFh6ZBVJq9UlL9GetlHj0Az05OeElASQ7wi2bqZAxzqSgmgIKDcHKkt3CbQ8qd78vFgigkwhSrUqt2ZBvtMTldMwBuY9cCVudvvkcJXqQWHB6IwAYSFMysl1kc0dRZCk1LxonHsToiuDoTTIzdiFW1wqV9zkJFDIMjBqqnJPlrQ'
app_secret = 'af015b8e7a1e6ef81fb66dee103a6642'
app_id = '351203884640886'

FacebookAdsApi.init(app_id=app_id, app_secret=app_secret, access_token=access_token)

def search_interests(query):
    params = {
        'q': query,
        'type': 'adinterest',
    }
    resp = TargetingSearch.search(params=params)
    return resp

# Testar a função com diferentes palavras-chave
queries = ['inteligência artificial', 'programming python']
for query in queries:
    print(f"Interesses para a palavra-chave '{query}':")
    interests_response = search_interests(query)
    for interest in interests_response:
        print(f"ID: {interest['id']}, Nome: {interest['name']}")
    print("\n")

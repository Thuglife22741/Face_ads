from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import os
from dotenv import load_dotenv

def test_facebook_connection():
    try:
        # Load environment variables
        load_dotenv()
        
        access_token = os.getenv('my_access_token')
        app_id = os.getenv('my_app_id')
        app_secret = os.getenv('my_app_secret')
        ad_account_id = os.getenv('ad_account_id')

        # Initialize the API
        FacebookAdsApi.init(app_id, app_secret, access_token)

        # Try to get ad account info
        ad_account = AdAccount(f'act_{ad_account_id}')
        account_info = ad_account.api_get(fields=['name', 'account_status'])
        
        print("Connection successful!")
        print(f"Account Name: {account_info['name']}")
        print(f"Account Status: {account_info['account_status']}")
        
    except Exception as e:
        print("Connection failed!")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_facebook_connection()
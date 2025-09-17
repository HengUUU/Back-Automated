import requests
from typing import Dict
from fastapi import HTTPException
from app.models.data_schema import EntryResponseData

def fetch_api_data(api_base_url: str, bearer_token: str, api_key: str, cookies: str )-> Dict:
    headers = {}
    
    if bearer_token:
        headers = {
            "Accept": "application/json, text/html",
            "Accept-Language": "en-US,en;q=0.5",
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
    if api_key:
        headers["x-Api-Key"] = api_key

    cookies = {
    "platform": "Web",
    "checkout_address": 526767,
    "shipping_method": "",
    "language_id": "1"
}


    
    try:
        
        if cookies:
            response = requests.get(api_base_url, headers=headers, cookies=cookies)
        else:
            response = requests.get(api_base_url, headers=headers)

        if response.status_code == 200: 
            response.encoding = 'utf-8'
              # Ensure correct encoding
            try:
                data = response.json()  # try parsing JSON
            except ValueError:  # invalid JSON
                data = response.text
            return EntryResponseData(status=200, data=data)
        else:
            return EntryResponseData(status=response.status_code, data=None)
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
import requests
import dns.resolver
import json

def check_valid_token(token: str) -> dict:


    try:
        # Resolve wpms.moe.gov.kh using Google DNS
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ["8.8.8.8"] 

        answer = resolver.resolve("wpms.moe.gov.kh", "A")
        ip = answer[0].to_text()

        factorier_url = f"https://{ip}/api/v1/organizationHierarchy"


        headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        f"Authorization": f"Bearer {token}",
        "X-Api-Key": "1ccbc4c913bc4ce785a0a2de444aa0d6",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Host": "wpms.moe.gov.kh"  # Important!
        }

        response = requests.get(factorier_url, headers=headers, verify=False)  # verify=False skips SSL hostname mismatch


        if response.status_code == 200:
            return {"status": "success", "message": "Token is valid", "data": response.json()}
            
        
        elif response.status_code == 401:
            return {"status": "error", "message": "Invalid token"}
        else:
            return {"status": "error", "message": f"Unexpected response: {response.status_code}"}
        
    
        
    except dns.resolver.NXDOMAIN:
        return {"status": "error", "message": "Domain not found"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Request failed: {str(e)}"}
    
    
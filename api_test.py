import requests
import json

# API endpoint
BASE_URL = 'http://localhost:5000/api'

def test_login():
    login_url = f"{BASE_URL}/user/login"
    
    # Test credentials
    credentials = {
        "username": "testadmin",
        "password": "admin123"
    }
    
    # Make the login request
    print(f"Sending request to {login_url} with data: {json.dumps(credentials)}")
    response = requests.post(login_url, json=credentials)
    
    # Print the response
    print(f"Status code: {response.status_code}")
    if response.headers.get('Content-Type') == 'application/json':
        print(f"Response body: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Response body: {response.text[:500]}")  # Print first 500 chars of HTML response

if __name__ == "__main__":
    test_login() 
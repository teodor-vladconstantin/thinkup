import requests

url = "http://127.0.0.1:5000/projects/mky2cc61g3vd89ykkup"
params = {"project_token": "TOKEN_demo3efv"}

try:
    response = requests.get(url, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")

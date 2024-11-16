from typing import Optional

import requests
from locust import HttpUser, between, task

API_BASE_URL = "http://localhost:8000"


def login(username: str, password: str) -> Optional[str]:
    """This function calls the login endpoint of the API to authenticate the user and get a token.

    Args:
        username (str): email of the user
        password (str): password of the user

    Returns:
        Optional[str]: token if login is successful, None otherwise
    """
    # TODO SIMON: Implement the login function
    # 1 - make a request to the login endpoint
    # 2 - check if the response status code is 200
    # 3 - if it is, return the access_token
    # 4 - if it is not, return None
    url = f"{API_BASE_URL}/login"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }
    try: 
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        
        # Extraer el token de manera segura, ya que response.json().["access_token"]
        # asume que el token estará presente, lo cual puede producir un 'KeyError'
        # si por alguna razón el token no llega
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f'An error occurred while processing the request: {e}')
        return None


class APIUser(HttpUser):
    wait_time = between(1, 5)

    # Put your stress tests here.
    # See https://docs.locust.io/en/stable/writing-a-locustfile.html for help.
    # TODO SIMON
    # raise NotImplementedError

    # Debemos definir cuántas veces correran las pruebas
    
    @task(1) # Puse un peso relativo de 1 mientras definimos cuánto deben corre las pruebas
    def index(self):
        try:
            response = self.client.get("/index")
            response.raise_for_status()
            print('/index passed!')
        except requests.exceptions.RequestException as e:
            print(f'Error occurred during /index test: {e}')
    
    @task(2)
    def predict(self):
        try: 
            token = login("admin@example.com", "admin")
            files = [("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))]
            headers = {"Authorization": f"Bearer {token}"}
            #payload = {}
            response = self.client.post(
                "http://0.0.0.0:8000/model/predict",
                headers=headers,
                #data=payload, Esta línea está comentada porque no va payload adicional, todo va en 'files'
                files=files,
            )
            response.raise_for_status()
            print('/predict passed!')
        except requests.exceptions.RequestException as e:
            print(f'Error occurred during /predict test: {e}')
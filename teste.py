import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzgxMjAyODg3fQ.KcTMHib7woNz76CD6B39kkX5PJas6ZzD5e85lx2Ak0E"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh",headers=headers)

print(requisicao)
print(requisicao.json())
import requests
from lab6 import JsonOperations

class RestClient:
    def __init__(self, url):
        self.url=url
    def get(self, resource):
        endpoint=f"{self.url}/{resource}"
        res=requests.get(endpoint)
        if res.status_code==200:
            data=res.json()
            print('OK')
            return data
        else:
            print(f'error: {res.status_code}')
    def post(self, resource, data):
        endpoint=f"{self.url}/{resource}"
        res=requests.post(endpoint, json=data)
        if res.status_code==201:
            print("created post", res.json())
        else:
            print(f"{res.status_code}")
    def delete(self, resourse, number_post):
        endpoint=f"{self.url}/{resourse}/{number_post}"
        res=requests.delete(endpoint)
        if res.status_code==200 or res.status_code==204:
            print(f'post deleted')
        else:
            print(f"error: {res.status_code}")
    def put(self, resourse, number_post, new_data):
        endpoint=f"{self.url}/{resourse}/{number_post}"
        res=requests.put(endpoint, json=new_data)
        if res.status_code==200 or res.status_code==204:
            print(f'post updated')
        else:
            print(f"error: {res.status_code}")
url="https://jsonplaceholder.typicode.com"
client=RestClient(url)
info_posts=client.get('posts')

JsonOperations('posts.json').save_to_json(info_posts)

data = {
    "userId": 10,
    "id": 101,
    "title": "test",
    "body": "test body"
}
new_data={
    "userId": 10,
    "id": 101,
    "title": "new_test",
    "body": "new_test body"
}
client.post('posts', data)
client.delete('posts', 1)
client.put('posts', 1, new_data)
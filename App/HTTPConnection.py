import requests

if __name__ == '__main__':
    response = requests.get('http://localhost:8888/getpeerip', params={'username': 'alireza'})
    print(response.text)

import requests

TESTURL = "https://demo.noguera.dev/api/"

def get_test():
    response = requests.get(TESTURL)
    return response.json()
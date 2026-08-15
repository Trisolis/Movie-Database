import requests
from config import API_KEY

class API:
    def __init__(self):
        self.key = API_KEY
        self.base_url = ""
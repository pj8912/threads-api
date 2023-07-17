from instagrapi import Client
import json
import requests

from threads_api.src.http_sessions.abstract_session import HTTPSession
from threads_api.src.anotherlogger import log_debug

class InstagrapiSession(HTTPSession):
    def __init__(self):
        self._instagrapi_client = Client()
        self._instagrapi_headers = self._instagrapi_client.private.headers
        self._threads_headers = {
                'User-Agent': 'Barcelona 289.0.0.77.109 Android',
                'Sec-Fetch-Site': 'same-origin',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        # override with Threads headers
        self._instagrapi_client.private.headers=self._threads_headers

    def auth(self, **kwargs):
        # restore original headers for Instagram login
        self._instagrapi_client.private.headers = self._instagrapi_headers
        self._instagrapi_client.login(**kwargs)
        token = self._instagrapi_client.private.headers['Authorization'].split("Bearer IGT:2:")[1]

        # override with Threads headers
        self._instagrapi_client.private.headers = self._threads_headers
        
        return token
    
    async def start(self):
        pass

    async def close(self):
        pass

    async def post(self, **kwargs):
        log_debug(title='PRIVATE REQUEST', type='POST', requests_session_params=vars(self._instagrapi_client.private), **kwargs)
        response = self._instagrapi_client.private.post(**kwargs)
        try:
            resp = response.json()
            log_debug(title='PRIVATE RESPONSE', requests_session_params=vars(self._instagrapi_client.private), response=resp)

            if resp['status'] == 'fail':
                raise Exception(f"Request Failed: [{resp['message']}]")
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            raise Exception('Failed to decode response as JSON')
        
        return resp

    async def get(self, **kwargs):
        log_debug(title='PRIVATE REQUEST', type='GET', **kwargs)
        response = self._instagrapi_client.private.get(**kwargs)
        try:
            resp = response.json()
            log_debug(title='PRIVATE RESPONSE', response=resp)

            if resp['status'] == 'fail':
                raise Exception(f"Request Failed: [{resp['message']}]")
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            raise Exception('Failed to decode response as JSON')
        
        return resp
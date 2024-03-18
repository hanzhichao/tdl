import requests

from tdl.context import library


@library
class Http:
    def __init__(self, base_url=None, params: dict=None, headers: dict=None, auth: tuple=None):
        self.base_url = base_url
        self._session = requests.Session()
        if params is not None:
            self._session.params = params
        if headers is not None:
            self._session.headers = headers
        if auth is not None:
            self._session.auth = auth

    def request(self, method, url, **kwargs):
        if not url.startswith('http'):
            url = '%s%s' % (self.base_url, url)
        return self._session.request(method, url, **kwargs)

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

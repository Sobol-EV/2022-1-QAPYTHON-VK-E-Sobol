import json
from urllib.parse import urljoin

import allure
import requests


class InvalidLoginException(Exception):
    pass


class FailedToGetCSRF(Exception):
    pass


class RespondErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url, user, password):
        self.base_url = base_url
        self.base_login_url = 'https://auth-ac.my.com'
        self.user = user
        self.password = password
        self.csrftoken = None

        self.session = requests.Session()

    def _request(self, method, location, headers=None, data=None, expected_status=200, jsonify=True, params=None):
        headers = headers if headers or method == "GET" else \
            {
                'X-CSRFToken': self.csrftoken
            }
        url = urljoin(self.base_url, location)
        response = self.session.request(method=method, url=url, headers=headers, data=data, params=params)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"')

        if jsonify:
            json_response = response.json()
            if json_response.get('error', False):
                error = json_response['error']
                raise RespondErrorException(f'Request {url} returned error {error["message"]}!')

            return json_response

        return response

    def update_csrf(self):
        try:
            url_csrf = urljoin(self.base_url, '/csrf/')
            response = self.session.get(url=url_csrf)
            return response.cookies['csrftoken']
        except Exception as E:
            raise FailedToGetCSRF(E)

    def csrf_auth(self):
        try:
            url_auth = urljoin(self.base_login_url, '/auth')
            response = self.session.get(url=url_auth)
            return response.cookies['csrf_token']
        except Exception as E:
            raise FailedToGetCSRF(E)

    @allure.step("Authorization on the my.target.com portal")
    def authorize(self, set_session=True):
        self.csrf_auth()
        url_auth = urljoin(self.base_login_url, '/auth')
        headers = {
            'Referer': self.base_url
        }
        data = {
            'email': self.user,
            'password': self.password,
            'continue': 'https://account.my.com/login_continue/?continue=https://account.my.com',
            'failure': 'https://account.my.com/login/?continue=https://account.my.com'
        }

        response = self.session.post(url=url_auth, data=data, headers=headers)

        if not set_session:
            return response

        response = self.session.get(url='https://target.my.com/dashboard')

        if response.url == self.base_url + "/":
            raise InvalidLoginException('Failed authorization')
        self.csrftoken = self.update_csrf()

    def post_campaing_create(self, payload):
        """Creates a company from the given JSON object"""
        location = '/api/v2/campaigns.json'
        payload = json.dumps(payload)

        return self._request(method="POST", location=location, data=payload)

    def post_campaing_change_status(self, id_campaing, payload):
        """
        Changes campaign status by id
        :param id_campaing: int
        :param payload: json {"status": <status>}
        """
        location = f'/api/v2/campaigns/{id_campaing}.json'
        payload = json.dumps(payload)

        return self._request(method="POST", location=location, data=payload,
                             expected_status=204, jsonify=False)

    def post_create_segments(self, payload, fields="id"):
        """
        Creates a segment on the passed json object, and returns the data specified in fields
        """
        location = "/api/v2/remarketing/segments.json"
        params = {
            "fields": {fields}
        }
        payload = json.dumps(payload)

        return self._request(method="POST", location=location, data=payload, params=params)

    def delete_segments(self, id_segments):
        """Deleting a segment by id"""
        location = f"/api/v2/remarketing/segments/{id_segments}.json"

        return self._request(method="DELETE", location=location, expected_status=204, jsonify=False)

    def get_info_campaing_by_id(self, id_campaing, fields='id,status'):
        location = f"/api/v2/campaigns/{id_campaing}.json"
        params = {
            "fields": {fields}
        }

        return self._request(method="GET", location=location, params=params)

    def get_info_segment_by_id(self, id_segment, fields='id'):
        location = f"/api/v2/remarketing/segments/{id_segment}/relations.json"
        params = {
            "fields": {fields}
        }

        return self._request(method="GET", location=location, params=params)

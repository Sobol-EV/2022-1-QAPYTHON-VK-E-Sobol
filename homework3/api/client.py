import json
from urllib.parse import urljoin
import os
import allure
import requests

import api.error_classes as error_cls


class ApiClient:

    def __init__(self, base_url, user, password):
        self.base_url = base_url
        self.base_login_url = 'https://auth-ac.my.com'
        self.user = user
        self.password = password
        self.csrftoken = None

        self.session = requests.Session()

    def _request(self, method, location, headers=None, data=None,
                 expected_status=200, jsonify=True, params=None, files=None):

        url = urljoin(self.base_url, location)
        response = self.session.request(method=method, url=url, headers=headers,
                                        data=data, params=params, files=files)

        if response.status_code != expected_status:
            raise error_cls.ResponseStatusCodeException(
                f'Got {response.status_code} {response.reason} for URL "{url}"'
            )

        if jsonify:
            json_response = response.json()
            if json_response.get('error', False):
                error = json_response['error']
                raise error_cls.RespondErrorException(
                    f'Request {url} returned error {error["message"]}!'
                )

            return json_response

        return response

    def update_csrf(self):
        try:
            url_csrf = urljoin(self.base_url, '/csrf/')
            response = self.session.get(url=url_csrf)
            return response.cookies['csrftoken']
        except KeyError as E:
            raise error_cls.FailedToGetCSRF(E)

    def csrf_auth(self):
        try:
            url_auth = urljoin(self.base_login_url, '/auth')
            response = self.session.get(url=url_auth)
            return response.cookies['csrf_token']
        except KeyError as E:
            raise error_cls.FailedToGetCSRF(E)

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
            raise error_cls.InvalidLoginException('Failed authorization')
        self.csrftoken = self.update_csrf()

    def post_campaign_create(self, payload):
        """Creates a company from the given JSON object"""
        location = '/api/v2/campaigns.json'
        payload = json.dumps(payload)
        headers = {
                'X-CSRFToken': self.csrftoken
        }

        return self._request(method="POST", location=location, headers=headers, data=payload)

    def post_campaign_change_status(self, id_campaing, payload):
        """
        Changes campaign status by id
        :param id_campaing: int
        :param payload: json {"status": <status>}
        """
        location = f'/api/v2/campaigns/{id_campaing}.json'
        headers = {
            'X-CSRFToken': self.csrftoken
        }
        payload = json.dumps(payload)

        return self._request(method="POST", location=location, headers=headers, data=payload,
                             jsonify=False, expected_status=204)

    def post_create_segments(self, payload, fields="id"):
        """
        Creates a segment on the passed json object, and returns the data specified in fields
        """
        location = "/api/v2/remarketing/segments.json"
        headers = {
            'X-CSRFToken': self.csrftoken
        }
        params = {
            "fields": {fields}
        }
        payload = json.dumps(payload)

        return self._request(method="POST", location=location, headers=headers,
                             data=payload, params=params)

    def delete_segments(self, id_segments):
        """Deleting a segment by id"""
        location = f"/api/v2/remarketing/segments/{id_segments}.json"
        headers = {
            'X-CSRFToken': self.csrftoken
        }

        return self._request(method="DELETE", location=location, headers=headers,
                             jsonify=False, expected_status=204)

    def get_info_campaign_by_id(self, id_campaing, fields='id,status'):
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

    def post_upload_file(self, file_path, repo_root):
        location = "/api/v2/content/static.json"
        file_path = os.path.join(repo_root, file_path)
        file_open = open(file_path, 'rb')
        files = {
            'file': file_open
        }
        headers = {
            'X-CSRFToken': self.csrftoken
        }
        response = self._request(method="POST", location=location, headers=headers, files=files)
        file_open.close()
        return response

    def post_add_to_mediateka(self, payload):
        location = "/api/v2/mediateka.json"
        headers = {
            'X-CSRFToken': self.csrftoken
        }
        payload = json.dumps(payload)

        return self._request(method="POST", location=location, headers=headers,
                             data=payload, expected_status=201)

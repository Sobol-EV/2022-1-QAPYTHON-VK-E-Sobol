import settings
import socket


class Socket:

    def __init__(self):

        self.host = settings.MOCK_HOST
        self.port = int(settings.MOCK_PORT)

    def create_client(self, request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(0.1)
            client.connect((self.host, self.port))
            client.send(request.encode())
            total_data = []
            while True:
                data = client.recv(4096)
                if data:
                    total_data.append(data.decode())
                else:
                    break
            data = ''.join(total_data).splitlines()

        return data

    def get_request(self, name):
        request = f'GET /get_user/{name} HTTP/1.1\r\n' \
                  f'Host: {self.host}\r\n\r\n'

        return self.create_client(request)

    def post_request(self, name):
        data = '{' + f'"first_name": "{name}"' + '}'
        length = str(len(data))
        request = f'POST /add_user HTTP/1.1\r\n' \
                  f'host: {self.host}\r\n' \
                  f'Content-Length: {length}\r\n'\
                  f'content-type: application/json\r\n'\
                  f'\r\n{data}'

        return self.create_client(request)

    def put_request(self, name, new_last_name):
        data = '{' + f'"new_last_name": "{new_last_name}"' + '}'
        length = str(len(data.encode()))
        request = f'PUT /change_last_name_by_name/{name} HTTP/1.1\r\n' \
                  f'host: {self.host}\r\n' \
                  f'Content-Length: {length}\r\n'\
                  f'content-type: application/json\r\n'\
                  f'\r\n{data}'

        return self.create_client(request)

    def delete_request(self, name):
        request = f'DELETE /delete_user_by_name/{name} HTTP/1.1\r\n' \
                  f'Host: {self.host}\r\n\r\n'

        return self.create_client(request)


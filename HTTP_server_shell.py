# HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants
import os
import socket

# TO DO: set constants
IP = '127.0.0.1'
PORT = 80
DEFAULT_URL = 'index.html'
REDIRECTION_DICTIONARY = ['webroot\\redirection_file.html']
FORBIDDEN_DIRECTORIES = ['webroot\\classified\\']
SOCKET_TIMEOUT = 60000


# REQUEST_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']


def get_file_data(filename):
    """ Get data from file """
    print('Trying to open file ' + filename)
    file = open(filename, 'rb')

    with file as f:
        data = f.read()

    return data


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    if resource == '' or resource == '/':
        url = DEFAULT_URL
    else:
        url = resource

    optional_field = ''

    # TO DO: STATUS-CODE check if URL had been redirected, not available or other error code. For example:
    if url in REDIRECTION_DICTIONARY:
        status_code = '302 Found'
        optional_field = r'webroot\redirection_file.html\r\n'
    else:
        status_code = '200 OK'

    http_header = ('HTTP/1.1 %s\r\n' % status_code) + optional_field

    if not status_code == '200 OK':
        client_socket.send(http_header.encode())
    else:
        # TO DO: read the data from the file
        file_name = 'webroot\\' + url.replace('/', '\\')  # Example: C:\Cyber\webroot\index.html
        if os.path.isfile(file_name):
            filetype = file_name.split('.')[-1]
            data = get_file_data(file_name)

            http_header += 'Content-Length: %d\r\n' % len(data)

            if filetype == 'html':
                http_header += 'Content-Type: %s\r\n' % 'text/html; charset=utf-8'
            elif filetype == 'jpg':
                http_header += 'Content-Type: %s\r\n' % 'image/jpeg'
            elif filetype == 'js':
                http_header += 'Content-Type: %s\r\n' % 'text/javascript; charset=UTF-8'
            elif filetype == 'css':
                http_header += 'Content-Type: %s\r\n' % 'text/css'
            else:
                http_header += '\r\n'
            http_header += '\r\n'
            client_socket.send(http_header.encode())
            client_socket.send('\r\n'.encode())  # header and body should be separated by additional newline
            client_socket.send(data)
        else:
            print('Error 404 Not Found')
            http_header = 'HTTP/1.1 404 Not Found\r\n\r\n'
            client_socket.send(http_header.encode())


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    # TO DO: write function
    req = request.split()
    if len(req) == 0:
        return False, 'Invalid request'
    if not req[0] == 'GET':
        return False, '500 Internal Server Error'

    if not req[2] == 'HTTP/1.1':
        return False, '500 Internal Server Error'

    return True, req[1]


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        # TO DO: insert code that receives client request
        client_request = client_socket.recv(1024).decode()

        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print(resource)
            break
    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    print("Listening for connections on port %d" % PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()

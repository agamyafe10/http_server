import socket
import os


# HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules

# constants
IP = '127.0.0.1'
PORT = 8090
SOCKET_TIMEOUT = 5.0# the time the server waits before raising error if there is no Get


def get_file_data(file_root):
    """ Get data from file """
    # file_type = file_root.split('.')[-1]
    # if file_type in ['html', 'jpg']:
    file_data = open(file_root, 'rb')
    data = file_data.read()
    file_data.close()
    return data


def get_content_type(type):
    contents = {"html": "text/html; charset=utf-8",
                    "txt": "text/html; charset=utf-8",
                    "jpg": "image/jpeg",
                    "js": "text/javascript; charset=UTF-8",
                    "css": "text/css",
                    "ico": "image/x-icon",
                    "gif": "image/gif"}
    return contents[type]


def handle_client_request(file_name, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""

    directory = 'webroot\\'
    DEFAULT_URL = directory + "index.html"

    if file_name == '':# in case no specific file was requested
        url = DEFAULT_URL
    else:
        url = directory + file_name# generating the url
    http_header = "HTTP/1.1"
    data = ""
    if os.path.isfile(url):# if the requested file exists
        print(url)
        response_dict = {"index.html": "ok",
        "css\\doremon.css": "ok",
        "js\\box.js": "ok",
        "js\\jquery.min.js": "ok",
        "js\\submit.js": "ok",
        "imgs\\abstract.jpg": "ok",
        "imgs\\favicon.ico": "ok",
        "imgs\\loading.gif": "ok",
        "ido.html": "forbidden",
        "agam.html": "moved",
        "noam.html": "error"}
        if response_dict[file_name] == "ok":
            file_type = url.split(".")[-1]
            status = " 200 OK\r\nContent-Length: " + str(os.path.getsize(url)) + "\r\nContent-Type: " + get_content_type(file_type) + "\r\n\r\n"
            data = get_file_data(url)
            print(data)
        elif response_dict[file_name] == "forbidden": 
            status = " 403 Forbidden"
        elif response_dict[file_name] == "moved":
            status = " 302 Temprarily Moved\r\nLocation: index.html"
        elif response_dict[file_name] == "error":
            status = " 500 Internal Server Error"


        http_header += status
        print(http_header)

    # generating the response properly    
    if not isinstance(data, bytes):
        data = data.encode()
    http_header = http_header.encode()
    http_response = http_header + data
    print(http_response)
    client_socket.send(http_response)


def validate_http_request(request):

    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested file name """
    # TO DO: write function
    web_root = request.decode().split(r'\r\n')[0].split(' ')[1][1:]# take the requested file name
    if '/' in web_root:
        web_root = web_root.replace('/', '\\')
    decoded_request = str(request.decode())# it benn received binary

    if decoded_request[0:3] != 'GET':
        return False, web_root

    if decoded_request[3] != ' ':
        return False, web_root
    # if "http://" not in decoded_request:
    #     return False, file_data
    if "HTTP/1.1" not in decoded_request:
        return False, web_root
    # if decoded_request[len(decoded_request)-4:len(decoded_request)] != r'\r\n':
    #     return False, file_data
    return True, web_root


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """

    print('Client connected')

    #while True:
    client_request = client_socket.recv(2048)# receiving the data the client sent
    print(client_request)
    valid_http, file_name = validate_http_request(client_request)# valid the request
    if valid_http:# the request is valid indeed
        print('Got a valid HTTP request')
        handle_client_request(file_name, client_socket)
    else:
        print('Error: Not a valid HTTP request')
        #break
    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# defining the socket
    server_socket.bind((IP, PORT))# setting the current ip and port
    server_socket.listen()# the time it listen to client until closing the socket
    print("Listening for connections on port %d" % PORT)

    while True:
        client_socket, client_address = server_socket.accept()# accept the request
        print('New connection received')
        # client_socket.settimeout(SOCKET_TIMEOUT)# defining the time until the socket will be shut down
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
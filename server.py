# Written by Shlomi Ben-Shushan and Gal Yehezkel 
import socket, sys, os

# Get server port as argument.
TCP_PORT = int(sys.argv[1])

# Set global consts.
BUFFER_SIZE = 4096
END_OF_MESSAGE = "\r\n\r\n"

# Open a TCP socket and listen.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
s.listen(1)

# Set flag that marks connection status.
is_alive = False

# Funtion that gets file path from the request.
def get_path(request):
    path = "files"
    if request == "/":
        path = os.path.join(path, "index.html")
    elif request == "/redirect":
        path = os.path.join(path, "result.html")
    else:
        path = os.path.join(path, request[1:])
    return path

# Function that gets the connection status according to the client.
def get_conn_status(data_rows):
    for row in data_rows:
        words = row.split(" ")
        if words[0] == "Connection:":
            return words[1]
    return "close"

# Server operation loop.
while True:

    # If there is no connection, open a new one.
    if is_alive == False:
        conn, addr = s.accept()
        conn.settimeout(1)

    # Try to recieve not-empty-data for 1 second.
    try:
        data = conn.recv(BUFFER_SIZE).split(END_OF_MESSAGE)
        if len(data) == 0:
            conn.close()
            is_alive = False
            continue
    except:
        conn.close()
        is_alive = False
        continue

    # For each request in the recieved data.
    for request in data:

        # If request is empty, continue. Else, print it.
        if len(request) == 0:
            continue
        print request + END_OF_MESSAGE

        # Get file path according to the request.
        rows = request.split('\n')
        request_line = rows[0].split(" ")
        if request_line[0] == "GET" or request_line[0] == "POST":
            file_request = request_line[1]
            file_path = get_path(file_request)
        else:
            conn.close()
            is_alive = False
            continue

        # Try to read the file in file_path, and send the relevant message.
        file_request_splitted = file_request.split(".")
        file_extention = file_request_splitted[len(file_request_splitted) - 1]
        try:
            if file_extention == "jpg" or file_extention == "ico":
                file_obj = open(file_path, "rb")
                content = file_obj.read()
            else:
                file_obj = open(file_path, "r")
                content = file_obj.read()
            if file_request == "/redirect":
                conn_status = "close"
                http_msg = "HTTP/1.1 301 Moved Permanently\r\n"
                conn_msg = "Connection: " + conn_status + "\r\n"
                loca_msg = "Location: /result.html\r\n"
                msg = http_msg + conn_msg + loca_msg + "\r\n" + content
            else:
                conn_status = get_conn_status(rows)
                http_msg = "HTTP/1.1 200 OK\r\n"
                conn_msg = "Connection: " + conn_status + "\r\n"
                leng_msg = "Content-Length: " + str(len(content)) + "\r\n"
                msg = http_msg + conn_msg + leng_msg + "\r\n" + content
            conn.send(msg)
            file_obj.close()
        except:
            conn_status = "close"
            http_msg = "HTTP/1.1 404 Not Found\r\n"
            conn_msg = "Connection: " + conn_status + "\r\n"
            msg = http_msg + conn_msg + "\r\n"
            conn.send(msg)

        # Close the connection if needed.
        if conn_status == "close":
            conn.close()
            is_alive = False
        else:
            is_alive = True

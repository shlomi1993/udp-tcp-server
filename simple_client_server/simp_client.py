# Written by Shlomi Ben-Shushan
import socket
import sys

# Store the given arguments in variables.
args = sys.argv
serverIP = str(args[1])
serverPort = int(args[2])

# Creates a socket.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Operation Loop.
while True:

    # The client asks for user's input.
    url = input("Enter URL: ")

    # Afterwards, it sent the request to it's server and wait for an answer.
    s.sendto(url.encode(), (serverIP, serverPort))
    data, addr = s.recvfrom(1024)

    # Than, the client prints the IP address.
    dataSplit = str(data).split(",")
    print(dataSplit[1])

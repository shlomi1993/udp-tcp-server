# Written by Shlomi Ben-Shushan
import socket
import sys
import time

# Store the given arguments in variables.
args = sys.argv
myPort = int(args[1])
parentIP = str(args[2])
parentPort = int(args[3])
ipsFileName = str(args[4])

# Creates a socket and binds server permanent port.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(myPort)))

# This function returns the current time in seconds.
def currentIntTime():
	enterTime = time.asctime(time.localtime(time.time())).split()
	enterTimeSplitted = enterTime[3].split(":")
	hrs = int(enterTimeSplitted[0])
	mins = int(enterTimeSplitted[1])
	secs = int(enterTimeSplitted[2])
	return hrs * 3600 + mins * 60 + secs

# This function erases line that thier TTL passed.
def deleteRows(ipsRows):
	with open(ipsFileName, "w") as file:
		for line in ipsRows:
			splitted = line.split(",")
			if len(splitted) == 3: #original line.
				if ipsRows[len(ipsRows) - 1] == line:
					file.write(line)
				else:
					file.write(line + "\n")
			elif len(splitted) == 4:#line that was added from the parent server.
				if currentIntTime() - int(splitted[3]) < int(splitted[2]): #if TTL didn't pass.
					if ipsRows[len(ipsRows) - 1] == line:
						file.write(line)
					else:
						file.write(line + "\n")

# The operation Loop.
while True:

	# Get the request from the client, refresh data and read IPs file.
	ips = open(ipsFileName, "r")
	ipsRows = ips.read().split("\n")
	data, addr = s.recvfrom(1024)
	deleteRows(ipsRows)


	# Looking for the data according to the client's request in the IPs file.
	info = ""
	for row in ipsRows:
		splitted = row.split(",")
		if data.decode() == splitted[0]:
			info = row

	# Case 1 - the requested URL isn't in the server's IPs file.
	if info == "":
		# If there is a parent, the request will pass to it.
		if parentIP != "-1":
			s.sendto(data, (parentIP, parentPort))
			data, parentAdder = s.recvfrom(1024)
			with open(ipsFileName, "a") as file:
				file.write(data.decode() + "," + str(currentIntTime()) + "\n")
			s.sendto(data, addr)

	# Case 2 - the requested URL was found in the file so the server can respond.
	else:
		s.sendto(info.encode(), addr)

import socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = ('172.16.1.165', 6666)

while 1:
	data = input("Enter:\n")
	client.sendto(data.encode(), port)


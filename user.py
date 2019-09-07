import json 
import socket
import time

def main():
	
	SERVER = "192.168.12.168"
	PORT = 12345
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((SERVER, PORT))
	m ={"requestId": "1", "access": "accepted", "method": "PUT", "client" : "USER"}
	jsonObj = json.dumps(m)
	data = jsonObj
	client.sendall(jsonObj.encode('utf-8'))
	received = client.recv(1024)
	recievedData = received.decode('utf-8')
	receivedJson = json.loads(recievedData)
	print(receivedJson)
	
if __name__ == '__main__':
	main()
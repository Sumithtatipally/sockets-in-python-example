import json 
import socket
import time

def main():

	SERVER = "192.168.12.168"
	PORT = 12345
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((SERVER, PORT))
	m ={"patientId": "32457632132", "clinicId": "2", "method": "POST", "client" : "CLINIC"}
	jsonObj = json.dumps(m)
	data = jsonObj
	client.sendall(jsonObj.encode('utf-8'))
	received = client.recv(1024)
	recievedData = received.decode('utf-8')
	receivedJson = json.loads(recievedData)
	print(receivedJson)
	requestId = receivedJson['id']
	try:
		while True:
			m ={"requestId": requestId , "method": "GET", "client" : "CLINIC"}
			jsonObj = json.dumps(m)
			data = jsonObj
			client.sendall(jsonObj.encode('utf-8'))
			received = client.recv(1024)
			recievedData = received.decode('utf-8')
			receivedJson = json.loads(recievedData)
			print(receivedJson)
			if receivedJson['access'] != "pending":
				m ={"method": "CLOSE", "client" : "CLINIC"}
				jsonObj = json.dumps(m)
				data = jsonObj
				client.sendall(jsonObj.encode('utf-8'))
				break
			time.sleep(5)
	finally:
		client.close()
	
if __name__ == '__main__':
	main()
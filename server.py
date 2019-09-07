import socket
import threading
import json
from database import *

class ClientThread(threading.Thread):

    def __init__(self,clientAddress,clientsocket, databaseConnect):

        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.databaseConnect = databaseConnect

    def run(self):

        msg = ''
        while True:
            data = self.csocket.recv(2048)
            data = data.decode('utf-8')
            if not data:
                break
            receivedJson = json.loads(data)
            method = receivedJson['method']
            client = receivedJson['client']

            if client == "CLINIC":
                if method == "POST":
                    patientId = receivedJson['patientId']
                    patientQuery = "SELECT id FROM patient WHERE uid = '"+patientId+"'"
                    patientData = database.selectSingleData(self.databaseConnect, patientQuery)
                    patientId = patientData[0]
                    clinicId = receivedJson['clinicId']
                    query = "INSERT INTO `records_access` (`patient_id`, `clinic_id`) VALUES (%s, %s)"
                    val = (patientId, clinicId)
                    id = database.insertData(self.databaseConnect, query, val)
                    response = {"status" : 1, "access" : "pending", "id" : id}

                if method == "GET":
                    requestId = receivedJson['requestId']
                    query = "SELECT response FROM records_access WHERE id = '%s'" % (requestId)
                    getData = database.selectSingleData(self.databaseConnect, query)
                    response = {"status" : 1, "access" : getData[0]}


            elif client == "USER":

                if method == "PUT":
                    requestId = receivedJson['requestId']
                    access = receivedJson['access']
                    query = "UPDATE `records_access` SET response = %s WHERE id = %s"
                    val = (access, requestId)
                    database.updateData(self.databaseConnect, query, val)
                    response = {"status" : 1 }

            if method == "CLOSE":
                break;

            jsonObj = json.dumps(response)
            responseData = jsonObj.encode("utf-8")
            self.csocket.send(responseData)

LOCALHOST = "192.168.12.168"
PORT = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
dbConnect = database.databaseConnect()
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock, dbConnect)
    newthread.start()

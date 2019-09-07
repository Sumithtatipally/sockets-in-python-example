import mysql.connector

class database():

	def databaseConnect():
		config = {
		  	'user': 'root',
		 	'password': '',
		  	'host': 'localhost',
		  	'database': 'name_api',
		  	'raise_on_warnings': True
		}
		cnx = mysql.connector.connect(**config)
		return cnx

	def insertData(cnx, query, val):
		cursor = cnx.cursor()
		cursor.execute(query, val)
		cnx.commit()
		id = cursor.lastrowid
		return id


	def selectAllData(cnx, query):
		cursor = cnx.cursor()
		cursor.execute(query)
		data = cursor.fetchall()
		return data

	def selectSingleData(cnx, query):
		cursor = cnx.cursor()
		cursor.execute(query)
		data = cursor.fetchone()
		return data

	def databaseClose(cnx):
		cnx.close()

	def updateData(cnx, query, val):
		cursor = cnx.cursor()
		cursor.execute(query, val)
		cnx.commit()
		

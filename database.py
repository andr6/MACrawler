import psycopg2
import sys

"""
INSTALL POSTGRES:
1. In terminal: sudo apt-get install postgresql libpq-dev postgresql-client postgresql-client-common
2. After installation: sudo -i -u postgres
3. In #postgres: createuser group11 -P --interactive
4. We set password as 12345 for now. Choose no, yes, yes
5. createdb MACdb
6. ctrl-d to exit postgres
7. In terminal: sudo apt-get install python-psycopg2
8. To import into crawler.py: from database import db



"""

class scanResults(object):
	scanID = ""
	url = ""
	result = ""
	status = -1

	def __init__(self):
		self.fileName = ""
		self.scanID = ""
		self.permalink = ""
		self.status = -1

	def setURL(self, url):
		self.url = url

	def setScanID(self, scanID):
		self.scanID = scanID

	def setResult(self, result):
		self.result = result

	def setStatus(self, status):
		self.status = status

	def getURL(self):
		return self.url

	def getScanID(self):
		return self.scanID

	def getResult(self):
		return self.result

	def getStatus(self):
		return self.status

class db(object):
	# Initialization includes connection and creation of cursor
	def __init__(self):	
		try: 
			connect_str = "dbname='MACdb' user='group11' host='localhost' password='12345'"
			self.conn = psycopg2.connect(connect_str)
			self.cursor = self.conn.cursor()
		except Exception as e:
			print("Invalid dbname, user or password")

	def insertTableNames(self, tableName_1, tableName_2, tableName_3):
		self.visited = tableName_1
		self.scanResult = tableName_2
		self.urlQueue = tableName_3

	def closeDB(self):
		try:
			self.cursor.close()
			self.conn.close()
		except Exception as e:
			print("Database cannot close properly")

	def createVisitedTable(self, tableName):
		try:
			self.visited = tableName;
			self.cursor.execute("CREATE TABLE " + tableName + " ( url varchar(256) PRIMARY KEY , urlType numeric, domain varchar(128), isScanned boolean);")
			self.conn.commit()
		except Exception as e:
			print("Visited Table creation failed")		

	def createScanResultTable(self, tableName):
		try:
			self.scanResult = tableName;
			self.cursor.execute("CREATE TABLE " + tableName \
					+ " ( scanID varchar(64) PRIMARY KEY, url varchar(256) REFERENCES " + self.visited \
					+ "(url), result varchar(3000), status numeric );")
			self.conn.commit()
		except Exception as e:
			print("Scan Result Table creation failed")

	def createURLQueueTable(self, tableName):
		try:
			self.urlQueue = tableName
			self.cursor.execute("CREATE TABLE " + tableName + " ( id SERIAL, url varchar(256) UNIQUE);")
			self.conn.commit()
		except Exception as e:
			print("URL Queue Table creation failed")				

	# Creates all the necessary tables
	def createCrawlerTables(self, tableName_1, tableName_2, tableName_3):
		self.createVisitedTable(tableName_1)
		self.createScanResultTable(tableName_2)
		self.createURLQueueTable(tableName_3)

	def deleteVisitedTable(self):
		try: 
			self.cursor.execute("DROP TABLE " + self.scanResult + ";")
			self.conn.commit()
			self.cursor.execute("DROP TABLE " + self.urlQueue + ";")
			self.conn.commit()
			self.cursor.execute("DROP TABLE " + self.visited + ";")
			self.conn.commit()
		except Exception as e:
			print("Table cannot be dropped")
			self.conn.rollback()

	def deleteTable(self, tableName):
		try:
			self.cursor.execute("DROP TABLE " + tableName + ";")
			self.conn.commit()
		except Exception as e:
			print("Table " + tableName + " cannot be dropped")
			self.conn.rollback()

	# Deletes all the existing tables
	def deleteAllTables(self):
		""" DONT EVER RANDOMLY DROP TABLE. TABLE DROPPED CANNOT BE RECOVERED DONT PLAY PLAY """
		self.deleteTable(self.scanResult)
		self.deleteTable(self.urlQueue)
		self.deleteTable(self.visited)



	'''
	THIS PORTION IS FOR VISITED URL TABLE THAT IS USED BY THE CRAWLER
	'''
	def insertVisitedEntry(self, url, urlType, domain):
		try:
			self.cursor.execute("INSERT INTO " + self.visited + " VALUES (%s, %s, %s, %s);", (url, str(urlType), domain, str(False)))
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be inserted into table " + self.visited)
			self.conn.rollback()

	# Updates the isScanned column in the visited Table in accordance to the url provided
	# Input paramters (string, string, boolean) 
	def editVisitedScanEntry(self, url, isScanned):
		try:
			self.cursor.execute("UPDATE " + self.visited + " SET isScanned	= %s WHERE url = %s;", (str(isScanned), url))
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be updated")
			self.conn.rollback()

	def isVisited(self, url):
		try:		
			self.cursor.execute("SELECT url FROM " + self.visited + " WHERE url = '" + url + "';")
			rows = self.cursor.fetchall()
			if (len(rows) == 1):
				return True
			else:
				return False
		except Exception as e:
			print("Url: " + url + " cannot be selected from table " + self.visited)
			self.conn.rollback()

	def getVisitedEntriesByDomain(self, domain):
		try:		
			self.cursor.execute("SELECT url FROM " + self.visited + " WHERE domain = '" + domain + "';")
			rows = self.cursor.fetchall()
			if (len(rows) > 0):
				return True
			else:
				return False
		except Exception as e:
			print("Domain: " + domain + " cannot be selected from table " + self.visited)
			self.conn.rollback()



	'''
	THIS PORTION IS FOR SCAN RESULT TABLE THAT IS USED BY THE VIRUSTOTAL SENDER AND RECEIVER
	'''
	# Input parameters (string, string, string, string, int)
	def insertScanResultEntry(self, scanID, url, result, status):
		try:
			self.cursor.execute("INSERT INTO " + self.scanResult + " VALUES (%s, %s, %s, %s);", (scanID, url, result, str(status)))
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be inserted into table " + self.scanResult)
			self.conn.rollback()

	# Updates the status column (0, 1, -2 or 2) in the scan result table in accordance to scanID provided
	def updateScanResultStatus(self, scanID, status):
		try:
			self.cursor.execute("UPDATE " + self.scanResult + " SET status = %s WHERE scanID = %s;", (str(status), scanID))
			self.conn.commit()
		except Exception as e:
			print("Status cannot be updated in URL: " + url + " of table " + self.scanResult)
			self.conn.rollback()	

	def updateScanResults(self, scanID, result):
		try:
			self.cursor.execute("UPDATE " + self.scanResult + " SET result = %s WHERE scanID = %s;", (result, scanID))
			self.conn.commit()
		except Exception as e:
			print("Result cannot be updated in URL: " + url + " of table " + self.scanResult)
			self.conn.rollback()	

	# Returns a list of scanResults objects
	def getUnscannedResults(self):
		self.cursor.execute("SELECT * FROM " + self.scanResult + " WHERE status <> 2 LIMIT 4;")
		rows = self.cursor.fetchall()
		scanResultsList = self.readScanResults(rows)
		return scanResultsList

	def getAllScanResultsByDomain(self, domain):
		self.cursor.execute("SELECT srt.scanID, srt.url, srt.result, srt.status FROM " \
							+ self.scanResult + " srt, " + self.visited \
							+ " vt WHERE vt.url = srt.url AND vt.domain = '" + domain + "';")
		rows = self.cursor.fetchall()
		scanResultsList = self.readScanResults(rows)
		return scanResultsList

	def readScanResults(self, rows):
		scanResultsList = []
		for i in rows:
			tempScanResults = scanResults()
			tempScanResults.setScanID(i[0])
			tempScanResults.setURL(i[1])
			if i[2] is None :
				tempScanResults.setResult("")
			else:
				tempScanResults.setResult(i[2])
			tempScanResults.setStatus(int(i[3]))

			scanResultsList.append(tempScanResults)
		return scanResultsList		

	'''
	THIS PORTION IS FOR URL QUEUE TABLE THAT IS USED BY THE CRAWLER
	'''
	def push(self, url):
		try:
			self.cursor.execute("INSERT INTO " + self.urlQueue + " (url) VALUES ('" + url + "');")
			self.conn.commit()
		except Exception as e:
			print("Url: " + url + " cannot be inserted into table " + self.urlQueue)
			self.conn.rollback()

	def pop(self):
		try:
			self.cursor.execute("SELECT * FROM " + self.urlQueue + " ORDER BY id LIMIT 1;")
			row = self.cursor.fetchall()
			self.cursor.execute("DELETE FROM " + self.urlQueue + " WHERE id = '" + str(row[0][0]) + "';")
			self.conn.commit()
			return row[0][1]
		except Exception as e:
			print("Url: " + url + " cannot be popped from table " + self.urlQueue)
			self.conn.rollback()

	# Reset the serial sequence number
	# NOTE: restartValue MUST BE > 0
	def restartURLQueue(self, restartValue):
		try:
			self.cursor.execute("ALTER SEQUENCE " + self.urlQueue + "_id_seq RESTART WITH " + str(restartValue) + ";")
			self.conn.commit()
		except Exception as e:
			print("URL Queue Table serial ID cannot be restarted")
			self.conn.rollback()

	def exists(self, url):
		try:
			self.cursor.execute("SELECT * FROM " + self.urlQueue + " WHERE url = '" + url + "';")
			row = self.cursor.fetchall()		
			if (len(row) > 0):
				return True
			else:
				return False
		except Exception as e:
			print("Url: " + url + " cannot be popped from table " + self.urlQueue)
			self.conn.rollback()


'''
a = db()
a.insertTableNames("visitedTable", "scanResultTable", "urlQueueTable")

# a.deleteTable("urlQueueTable")
# a.createURLQueueTable("urlQueueTable")

a.deleteTable("scanResultTable")
a.deleteTable("visitedTable")
a.createVisitedTable("visitedTable")
a.createScanResultTable("scanResultTable")
a.insertVisitedEntry("www.google.com.sg", 0, "www.google.com")
a.insertVisitedEntry("www.google.com.hk", 0, "www.google.com")
a.insertVisitedEntry("www.yahoo.com.sg", 0, "www.yahoo.com")
a.insertVisitedEntry("www.yahoo.com.hk", 0, "www.yahoo.com")
a.insertVisitedEntry("www.dropit.com", 0, "www.dropit.com")
a.insertScanResultEntry("scanID_1", "www.dropit.com", "done", 2)
a.insertScanResultEntry("scanID_2", "www.google.com.sg", None, 0)
a.insertScanResultEntry("scanID_3", "www.google.com.hk", None, -2)
a.insertScanResultEntry("scanID_4", "www.yahoo.com.sg", None, -2)
a.insertScanResultEntry("scanID_5", "www.yahoo.com.hk", None, 1)

scanList = a.getUnscannedResults()
for i in scanList:
	print("Scan ID: " + i.getScanID())
	print("URL: " + i.getURL())
	print("Result: " + i.getResult())
	print("Status: " + str(i.getStatus()))

# a.createCrawlerTables("visitedTable", "scanResultTable", "urlQueueTable")
# a.insertVisitedEntry("visitedTable", "www.google.com.sg", 0, "www.google.com", False)
# a.editVisitedScanEntry("visitedTable", "www.google.com.sg", True)
# a.insertScanResultEntry("scanResultTable", "scanID_1", "www.google.com.sg", None, 0)
# a.editScanResultStatus("scanResultTable", "scanID_1", 2)
# a.insertURLQueueEntry("urlQueueTable", "www.google.com.sg")
# a.deleteURLQueueEntry("urlQueueTable", "www.google.com.sg")
# a.updateScanResults("scanResultTable", "scanID_1", None)
# a.restartURLQueue("urlQueueTable", 1)
# a.push("www.google.com.sg")
# a.push("www.google.com")

a.closeDB()
'''

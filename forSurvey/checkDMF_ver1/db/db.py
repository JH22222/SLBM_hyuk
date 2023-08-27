from pymongo import MongoClient
from config.constants import __dbloc__


class MongoDB: 
	def __init__(self):
		try:
			self._conn = MongoClient(__dbloc__) 
			self._db   = self._conn['users']
			print("MongoDB successfully connected!") 
		except:
			print("Could not connect to MongoDB")

	def get_collection(self, name=""):
		return self._db[name]

	def close_connection(self):
		self._conn.close()
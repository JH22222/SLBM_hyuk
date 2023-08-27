import tornado.web
import os, uuid
import json
from bson import json_util, ObjectId
from datetime import datetime, timedelta

from config.constants import (
	HTTP_INTERNAL_SERVER_ERROR,
	HTTP_OK
)

from db.db import MongoDB 


class QuantifiedSelf(tornado.web.RequestHandler):
	def post(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

		
		args = json.loads(self.request.body.decode('utf-8'))
		print(args)
		
		deviceID = args["deviceID"]
		status = args["status"]
		date = args["date"]

		print('deviceID: ', deviceID)
		print('status: ', status)
		print('date: ', date)

		db = MongoDB()

		try:
			if db._conn:

				users_collection = db.get_collection('users')

				deviceDetails = users_collection.find_one(
					{
						"deviceID": deviceID
					}
				)

				deviceDetails_str = json_util.dumps(deviceDetails)
				_deviceDetails = json.loads(deviceDetails_str)

				if _deviceDetails is not None:
					authCodeLast4 = _deviceDetails['authCodeLast4']
				else:
					authCodeLast4 = "UNKNOWN"

				quantified_self_collection = db.get_collection('quantified_self')

				print('checking....')
				qs = quantified_self_collection.find_one(
					{
						"deviceId": authCodeLast4,
						"status": status,
						"date": date,
					}
				)

				if qs is None:
					print('No analytics')
					print('-------')
					self.write("No analytics")
					self.set_status(200)
					self.finish()
				else:
					print(json_util.dumps(qs))

					self.write(json_util.dumps(qs))
					self.set_status(200)
					self.finish()

			
				db.close_connection()
				
			else:
				self.write('GetQuantifiedSelf Error')
				self.set_status(500)
				self.finish()
		except Exception as e:
			print('DB Error ', str(e))
			self.set_status(500)
			self.finish()


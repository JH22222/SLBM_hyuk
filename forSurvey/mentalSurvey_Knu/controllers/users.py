import tornado.web
import os, uuid
import json
from bson import json_util, ObjectId
from datetime import datetime, timedelta

from config.constants import (
	HTTP_INTERNAL_SERVER_ERROR,
	HTTP_OK,
	WATCH_ERROR,
	ONLINE_REGISTRATION_ERROR
)

from db.db import MongoDB 

AUTH_CODES_LIST = []

def date_request_received(ts):
  return datetime.fromtimestamp((float(ts)/1000.0)).strftime('%Y-%m-%d %H:%M:%S')


class OnlineRegistration(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

		overall_satisfaction = self.get_argument("overall_satisfaction")
		health = self.get_argument("health")
		asthma = self.get_argument("asthma")
		gender = self.get_argument("gender")
		marriage = self.get_argument("marriage")
		workstatus = self.get_argument("workstatus")
		morning_notification = self.get_argument("morning_notification")
		afternoon_notification = self.get_argument("afternoon_notification")
		evening_notification = self.get_argument("evening_notification")
		name = self.get_argument("name")

		db = MongoDB()

		try:
			if db._conn:
				users_collection = db.get_collection('users')

				user_auth_code = uuid.uuid4()
				user_auth_code_last4 = str(user_auth_code)[-4:]

				while True:
					if user_auth_code_last4 in AUTH_CODES_LIST:
						user_auth_code = uuid.uuid4()
						user_auth_code_last4 = str(user_auth_code)[-4:]
					else:
						AUTH_CODES_LIST.append(user_auth_code_last4)
						break

				new_user = {
					"overall_satisfaction": overall_satisfaction,
					"health": health,
					"asthma": asthma,
					"gender": gender,
					"marriage": marriage,
					"workstatus": workstatus,
					"authCodeLast4": user_auth_code_last4,
					"authCode": user_auth_code,
					"morning_notification": morning_notification,
					"afternoon_notification": afternoon_notification,
					"evening_notification": evening_notification,
					"name": name,
					"date": datetime.utcnow()
				}

				user_id = users_collection.insert_one(new_user).inserted_id

				print('New User recorded...')
				print(users_collection.find_one({'_id': user_id}))
				print('UserID:', user_id)
				print('Auth Code:', user_auth_code_last4)
				print('-------')
				print(users_collection)

				self.write(str(user_auth_code_last4))
				db.close_connection()
			else:
				self.write(ONLINE_REGISTRATION_ERROR)
		except Exception as e:
			print('DB Error ', str(e))


class RecoverUser(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

		name = self.get_argument("name")
		db = MongoDB()

		try:
			if db._conn:
				users_collection = db.get_collection('users')

				user_record = users_collection.find_one(
					{"$and": 
						[
							{"name": name}, 
							{"deviceID": {'$exists': True}}
						]
					}
				)

				if user_record is None:
					user_ret_obj = "User does not exist or device is not registered yet"
				else:
					
					user_ret_obj = {
						"deviceID": user_record['deviceID'],
						"authCode": user_record['authCodeLast4']
					}

				self.write(json.dumps(user_ret_obj))
				db.close_connection()
			else:
				self.write(ONLINE_REGISTRATION_ERROR)
		except Exception as e:
			print('DB Error ', str(e))


class VerifyWatchUser(tornado.web.RequestHandler):
	def post(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

		verification = json.loads(self.request.body.decode('utf-8'))

		duid = verification['duid']
		code = verification['code']
		regID = verification['regID']
		timestamp = verification['timestamp']

		print('Verification request received at:', date_request_received(timestamp))
		print('Payload: ', verification)

		db = MongoDB()

		try:
			if db._conn:
				users_collection = db.get_collection('users')

				# check the DB, if code (userID) exists update the entry with the deviceID and regID
				users_collection.update_one({'authCodeLast4': str(code)}, {'$set': {'deviceID':str(duid)}})
				users_collection.update_one({'authCodeLast4': str(code)}, {'$set': {'regID':str(regID)}})

				update_user_record = users_collection.find_one({"authCodeLast4":code})

				if update_user_record:
					print('Update User recorded... DevideID registered')
					print(users_collection.find_one({'authCodeLast4': str(code)}))
					print(users_collection)
					print('--------------')
					self.write(str(code))
				else:
					print('authCode error')
					self.write(WATCH_ERROR)
					self.set_status(400)
					self.finish()
			else:
				self.write(WATCH_ERROR)
				self.set_status(500)
				self.finish()
		except Exception as e:
			print('DB Error: ', str(e))
			self.set_status(500)
			self.finish()
			print('-------')

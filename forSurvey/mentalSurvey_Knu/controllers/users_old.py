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
				users_collection.update({'authCodeLast4': str(code)}, {'$set': {'deviceID':str(duid)}})
				users_collection.update({'authCodeLast4': str(code)}, {'$set': {'regID':str(regID)}})

				update_user_record = users_collection.find_one({"authCodeLast4":code})

				if update_user_record:
					print('Update User recorded... DevideID registered')
					print(users_collection.find_one({'authCodeLast4': str(code)}))
					print('-------')
					print(users_collection)
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
			print('DB Error ', str(e))
			self.set_status(500)
			self.finish()
			print('-------')

#######
# mongo
# use users
# db.users.find()
#db.users.find({deviceID:"z7HgloLuTnO65f5MuxOnylR6SUQ="})

## New Experiment from KNU => for WonKwang Univ (220713)
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'na','marriage':'na','workstatus':'na','authCodeLast4':'wku13','authCode':'wku13','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'knu_exp','date':'20220713'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'na','marriage':'na','workstatus':'na','authCodeLast4':'wku25','authCode':'wku25','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'knu_exp','date':'20220713'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'na','marriage':'na','workstatus':'na','authCodeLast4':'wku37','authCode':'wku37','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'knu_exp','date':'20220713'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'na','marriage':'na','workstatus':'na','authCodeLast4':'wku31','authCode':'wku31','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'knu_exp','date':'20220714'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'na','marriage':'na','workstatus':'na','authCodeLast4':'wku52','authCode':'wku52','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'knu_exp','date':'20220714'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'na','marriage':'na','workstatus':'na','authCodeLast4':'wku73','authCode':'wku73','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'knu_exp','date':'20220714'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'na','marriage':'na','workstatus':'na','authCodeLast4':'wku42','authCode':'wku42','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'knu_exp','date':'20220728'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'na','marriage':'na','workstatus':'na','authCodeLast4':'wku63','authCode':'wku63','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'knu_exp','date':'20220728'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'na','marriage':'na','workstatus':'na','authCodeLast4':'wku87','authCode':'wku87','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'knu_exp','date':'20220728'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'na','marriage':'na','workstatus':'na','authCodeLast4':'wku17','authCode':'wku17','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'knu_exp','date':'20220728'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'na','marriage':'na','workstatus':'na','authCodeLast4':'wku29','authCode':'wku29','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'knu_exp','date':'20220728'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'na','marriage':'na','workstatus':'na','authCodeLast4':'wku34','authCode':'wku34','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'knu_exp','date':'20220728'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'na','marriage':'na','workstatus':'na','authCodeLast4':'wku58','authCode':'wku58','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'knu_exp','date':'20220728'})

## 3rd Real Experiment: IBS + KAIST => Bug Fix (210721)
# { "_id" : ObjectId("60f0f579bf6d65e1ea056f65"), "authCode" : "ek97", "deviceID" : "z7HgloLuTnO65f5MuxOnylR6SUQ=", "regID" : "" } "=> oldUserId : md23" (=> Changed device one more time on 210812)
# { "_id" : ObjectId("60f0f57dbf6d65e1ea056f76"), "authCode" : "ux88", "deviceID" : "3z5c/AsxTM2UFZUPkWMrHVR6SUQ=", "regID" : "" } "=> oldUserId : ab60" (=> Changed device one more time on 210812)
# { "_id" : ObjectId("60f0f577bf6d65e1ea056f5d"), "authCode" : "ac13", "deviceID" : "HC65v9O4TQSd1ZpRg7ZWplR6SUQ=", "regID" : "" } "=> oldUserId : hk52"
# { "_id" : ObjectId("60f0f577bf6d65e1ea056f5e"), "authCode" : "ax22", "deviceID" : "JFg10GvLSD6CEeqIiySCoVR6SUQ=", "regID" : "" } "=> oldUserId : xw99"
# { "_id" : ObjectId("60f0f577bf6d65e1ea056f5f"), "authCode" : "be39", "deviceID" : "5R51ZXdaRd6JU/pSZXy6XlR6SUQ=", "regID" : "" } "=> oldUserId : ej27"
# { "_id" : ObjectId("60f0f577bf6d65e1ea056f60"), "authCode" : "bm45", "deviceID" : "019rW1TcTSGL5R/i2MAsbVR6SUQ=", "regID" : "" } "=> oldUserId : vc10"
# { "_id" : ObjectId("60f0f578bf6d65e1ea056f61"), "authCode" : "ch57", "deviceID" : "jK+M3KdxSVmRaOIsaPTR5VR6SUQ=", "regID" : "" } "=> oldUserId : ba30"
# { "_id" : ObjectId("60f0f578bf6d65e1ea056f62"), "authCode" : "cs63", "deviceID" : "/eL8MXIRQlimemhwb8ImRVR6SUQ=", "regID" : "" } "=> oldUserId : wc58"
# { "_id" : ObjectId("60f0f578bf6d65e1ea056f63"), "authCode" : "dw78", "deviceID" : "TPMxVSWJSlyhVmDTR98JVFR6SUQ=", "regID" : "" } "=> oldUserId : rw83"
# { "_id" : ObjectId("60f0f579bf6d65e1ea056f64"), "authCode" : "dp81", "deviceID" : "cADsalK1QRWG3olMEzc0z1R6SUQ=", "regID" : "" } "=> oldUserId : pg18"
# { "_id" : ObjectId("60f0f579bf6d65e1ea056f66"), "authCode" : "ea15", "deviceID" : "+UAYEavOTeCcHXpZJtrzl1R6SUQ=", "regID" : "" } "=> oldUserId : av54"
# { "_id" : ObjectId("60f0f579bf6d65e1ea056f67"), "authCode" : "gb23", "deviceID" : "rZWL7R79TMGq5w2PScvVVFR6SUQ=", "regID" : "" } "=> oldUserId : br74"
# { "_id" : ObjectId("60f0f57abf6d65e1ea056f68"), "authCode" : "gm34", "deviceID" : "qM5yMIhuSPKxwRyUP9Vkb1R6SUQ=", "regID" : "" } "=> oldUserId : xp20"
# { "_id" : ObjectId("60f0f57abf6d65e1ea056f69"), "authCode" : "ha49", "deviceID" : "mlKXFms4SM+M/EyECYpB0lR6SUQ=", "regID" : "" } "=> oldUserId : gw57"
# { "_id" : ObjectId("60f0f57abf6d65e1ea056f6a"), "authCode" : "hw52", "deviceID" : "8SRU7tnVTxquXKbtpV+iGVR6SUQ=", "regID" : "" } "=> oldUserId : us73"
# { "_id" : ObjectId("60f0f57abf6d65e1ea056f6b"), "authCode" : "km64", "deviceID" : "Tod+2TVNQ9uA7pX+11CFbFR6SUQ=", "regID" : "" } "=> oldUserId : ka67"
# { "_id" : ObjectId("60f0f57bbf6d65e1ea056f6c"), "authCode" : "kz73", "deviceID" : "ArNdBi7MSt2TsxYqy52UBlR6SUQ=", "regID" : "" } "=> oldUserId : sc27"
# { "_id" : ObjectId("60f0f57bbf6d65e1ea056f6d"), "authCode" : "ma85", "deviceID" : "HMZ+VQF1RgeC7EoXSnjCu1R6SUQ=", "regID" : "" } "=> oldUserId : gw39"
# { "_id" : ObjectId("60f0f57bbf6d65e1ea056f6e"), "authCode" : "mk94", "deviceID" : "cp4IjX2LS52At3a9OJngYVR6SUQ=", "regID" : "" } "=> oldUserId : ca37"
# { "_id" : ObjectId("60f0f57cbf6d65e1ea056f6f"), "authCode" : "pb17", "deviceID" : "tOQDlSMAQAa2W5ez29E3iFR6SUQ=", "regID" : "" } "=> oldUserId : dk68"
# { "_id" : ObjectId("60f0f57cbf6d65e1ea056f70"), "authCode" : "ph29", "deviceID" : "CWIO39qsRuyRwVLRh70wyVR6SUQ=", "regID" : "" } "=> oldUserId : pw85"
# { "_id" : ObjectId("60f0f57cbf6d65e1ea056f71"), "authCode" : "sb36", "deviceID" : "gfx74l7bTlWxngcqXMafdVR6SUQ=", "regID" : "" } "=> oldUserId : ev76"
# { "_id" : ObjectId("60f0f57cbf6d65e1ea056f72"), "authCode" : "sk43", "deviceID" : "f2Ma9TtnS76jGS2POUWCoVR6SUQ=", "regID" : "" } "=> oldUserId : te43"
# { "_id" : ObjectId("60f0f57dbf6d65e1ea056f73"), "authCode" : "tg53", "deviceID" : "Xssq2KiyRKKKbaE3YWifs1R6SUQ=", "regID" : "" } "=> oldUserId : it48"
# { "_id" : ObjectId("60f0f57dbf6d65e1ea056f74"), "authCode" : "tw68", "deviceID" : "/IxORz4fS9KryrFzD+kt8lR6SUQ=", "regID" : "" } "=> oldUserId : mg25"
# { "_id" : ObjectId("60f0f57dbf6d65e1ea056f75"), "authCode" : "ua77", "deviceID" : "kt/XkbYdS8WmO64bSQugJFR6SUQ=", "regID" : "" } "=> oldUserId : sm34"

## 3rd Real Experiment: IBS + KAIST (210716)
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'ac13','authCode':'ac13','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'ax22','authCode':'ax22','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'be39','authCode':'be39','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'bm45','authCode':'bm45','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'ch57','authCode':'ch57','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'cs63','authCode':'cs63','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'dw78','authCode':'dw78','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'dp81','authCode':'dp81','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'ek97','authCode':'ek97','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'ea15','authCode':'ea15','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'gb23','authCode':'gb23','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'gm34','authCode':'gm34','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'ha49','authCode':'ha49','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'hw52','authCode':'hw52','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'km64','authCode':'km64','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'kz73','authCode':'kz73','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'ma85','authCode':'ma85','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'mk94','authCode':'mk94','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'pb17','authCode':'pb17','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ph29','authCode':'ph29','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'sb36','authCode':'sb36','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'sk43','authCode':'sk43','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'tg53','authCode':'tg53','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'tw68','authCode':'tw68','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'female','marriage':'single','workstatus':'na','authCodeLast4':'ua77','authCode':'ua77','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ux88','authCode':'ux88','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'3rd_exp','date':'20210716'})

## 2nd Real Experiment: KAIST
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'md23','authCode':'md23','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ga64','authCode':'ga64','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'wc58','authCode':'wc58','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ab60','authCode':'ab60','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ub12','authCode':'ub12','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'kb24','authCode':'kb24','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'sm34','authCode':'sm34','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ba30','authCode':'ba30','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'rb86','authCode':'rb86','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ca37','authCode':'ca37','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'hp91','authCode':'hp91','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'we59','authCode':'we59','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'bp16','authCode':'bp16','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'pw85','authCode':'pw85','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ea80','authCode':'ea80','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'nd56','authCode':'nd56','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'gm49','authCode':'gm49','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'vh17','authCode':'vh17','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'mh40','authCode':'mh40','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'sh29','authCode':'sh29','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'vs14','authCode':'vs14','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ev76','authCode':'ev76','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'kn13','authCode':'kn13','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'xp20','authCode':'xp20','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ya71','authCode':'ya71','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'xw99','authCode':'xw99','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'cd53','authCode':'cd53','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ck44','authCode':'ck44','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'sp33','authCode':'sp33','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ka67','authCode':'ka67','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'zk41','authCode':'zk41','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'uz94','authCode':'uz94','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'rw83','authCode':'rw83','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'us73','authCode':'us73','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'gw39','authCode':'gw39','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})

## 2nd Real Experiment: IBS
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'sc27','authCode':'sc27','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'hk52','authCode':'hk52','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'es46','authCode':'es46','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'bc31','authCode':'bc31','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'sb88','authCode':'sb88','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'va70','authCode':'va70','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'av54','authCode':'av54','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'dk68','authCode':'dk68','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'gd81','authCode':'gd81','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'mg25','authCode':'mg25','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'pg18','authCode':'pg18','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ap21','authCode':'ap21','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'am77','authCode':'am77','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'pm96','authCode':'pm96','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'vc10','authCode':'vc10','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'2nd_exp','date':'20210303'})

## Before:
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'sp35','authCode':'sp35','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'shaun','date':'20210106'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'te43','authCode':'te43','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'james','date':'20210119'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'gw57','authCode':'gw57','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'tess','date':'20210119'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'br74','authCode':'br74','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'brian','date':'20210202'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ry23','authCode':'ry23','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'ryan','date':'20210202'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'wo16','authCode':'wo16','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'wook','date':'20210202'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ej27','authCode':'ej27','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'eunji','date':'20210202'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'it48','authCode':'it48','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'intern','date':'20210202'})

# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'ry89','authCode':'ry89','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20201207'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SA01','authCode':'SA01','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SB02','authCode':'SB02','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SC03','authCode':'SC03','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SD04','authCode':'SD04','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SE05','authCode':'SE05','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SF06','authCode':'SF06','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SG07','authCode':'SG07','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SH08','authCode':'SH08','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SI09','authCode':'SI09','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SJ10','authCode':'SJ10','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SA11','authCode':'SA11','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SB12','authCode':'SB12','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SC13','authCode':'SC13','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SD14','authCode':'SD14','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SE15','authCode':'SE15','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SF16','authCode':'SF16','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SG17','authCode':'SG17','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SH18','authCode':'SH18','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SI19','authCode':'SI19','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SJ20','authCode':'SJ20','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SA21','authCode':'SA21','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SB22','authCode':'SB22','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SC23','authCode':'SC23','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SD24','authCode':'SD24','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SE25','authCode':'SE25','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SF26','authCode':'SF26','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SG27','authCode':'SG27','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SH28','authCode':'SH28','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SI29','authCode':'SI29','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SJ30','authCode':'SJ30','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SA31','authCode':'SA31','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SB32','authCode':'SB32','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SC33','authCode':'SC33','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SD34','authCode':'SD34','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SE35','authCode':'SE35','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SF36','authCode':'SF36','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SG37','authCode':'SG37','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SH38','authCode':'SH38','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SI39','authCode':'SI39','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SJ40','authCode':'SJ40','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SA41','authCode':'SA41','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SB42','authCode':'SB42','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SC43','authCode':'SC43','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SD44','authCode':'SD44','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SE45','authCode':'SE45','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SF46','authCode':'SF46','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SG47','authCode':'SG47','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SH48','authCode':'SH48','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SI49','authCode':'SI49','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SJ50','authCode':'SJ50','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SA51','authCode':'SA51','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SB52','authCode':'SB52','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SC53','authCode':'SC53','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SD54','authCode':'SD54','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SE55','authCode':'SE55','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SF56','authCode':'SF56','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SG57','authCode':'SG57','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SH58','authCode':'SH58','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SI59','authCode':'SI59','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})
# db.users.insert({'overall_satisfaction':'na','health':'na','asthma':'na','gender':'male','marriage':'single','workstatus':'na','authCodeLast4':'SJ60','authCode':'SJ60','morning_notification':'na','afternoon_notification':'na','evening_notification':'na','name':'john','date':'20210104'})

## [End] > Add the user data.

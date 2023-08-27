import tornado.web
import os, uuid
from datetime import datetime, timedelta
import json
from bson import json_util, ObjectId
from bson.json_util import loads, dumps
import time
import pytz

from config.constants import (
	HTTP_INTERNAL_SERVER_ERROR,
	HTTP_OK,
	__UPLOADS__
)

from db.db import MongoDB 

class Upload(tornado.web.RequestHandler):
	def post(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

		datafile = self.request.files['file'][0]
		deviceID = self.get_argument("deviceID")
		battery = self.get_argument("battery")
		received_ts = self.get_argument("timestamp")
		filter_beginning = str(datafile['body']).replace("b'", "")
		filter_mid = filter_beginning.replace("\\r\\", "\n")
		filter_last = filter_mid.replace("'", "")

		fname = datafile["filename"]

		print('Data received at:', received_ts, ' from:', deviceID)
		print('File received:', fname)
		print('battery_percent:' , battery)
		print('--------------------------')
		print(deviceID)

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
					deviceID_folder_name = _deviceDetails['authCodeLast4']
				else:
					deviceID_folder_name = "UNKNOWN"

				db.close_connection()
			else:
				print('DB error')
		except Exception as e:
			print('DB Error ', str(e))

		# device_directory = "../../" + __UPLOADS__ + deviceID
		# date_now = datetime.now().date()
		# today = date_now.strftime('%d_%m_%Y')

		file_type = fname.split('_')[0]
		if file_type == 'mood' or file_type == "hrmapi":
			day = fname.split('_')[1]
			month = fname.split('_')[2]
			year = fname.split('_')[3].split('.')[0]

			file_created_date = day + '_' + month + '_' + year

			# device_directory = os.path.join(os.getcwd(), __UPLOADS__, deviceID, file_created_date)
			device_directory = os.path.join(os.getcwd(), __UPLOADS__, deviceID_folder_name, file_created_date)
			print(os.getcwd())

			new_fnanme = file_type + '_' + file_created_date + '_' + received_ts + '.csv'

		elif file_type == 'hrm' or file_type == 'ppg' or file_type == 'acc' or file_type == 'gyr' or file_type == 'grv' or file_type == 'ped' or file_type == 'slp' or file_type == 'tmp' or file_type == 'lit' or file_type == 'hum':
			file_created_ts = int(fname.split('_')[-1].split('.')[0])

			# gmt = pytz.timezone('Europe/London') 
			gmt = pytz.timezone('Asia/Seoul') 

			file_created_ts /= 1000
			print('-----------------')
			print('time on server UTC: ', datetime.utcfromtimestamp(file_created_ts))
			print('time on server -1: ', datetime.fromtimestamp(file_created_ts))

			print('-----------------')
			# file_created_date = datetime.utcfromtimestamp(file_created_ts).strftime('%d_%m_%Y')

			file_created_date = datetime.utcfromtimestamp(file_created_ts)
			local_created_date = file_created_date.astimezone(gmt)
			print('local time:',  local_created_date)

			file_created = local_created_date.strftime('%d_%m_%Y')
			print('file_created:',  file_created)
			print('-----------------')

			# device_directory = os.path.join(os.getcwd(), __UPLOADS__, deviceID, file_created)
			device_directory = os.path.join(os.getcwd(), __UPLOADS__, deviceID_folder_name, file_created)
			
			new_fnanme = fname

		print('file: ' + new_fnanme + ', will be stored in: ' + device_directory)
		print("device_directory dir: ", device_directory)

		if not deviceID_folder_name == "UNKNOWN":
			if not os.path.exists(device_directory):
				os.makedirs(device_directory)

			fh = open(device_directory + "/" + new_fnanme, 'w')
			fh.write(filter_last)

		db = MongoDB()

		try:
			if db._conn:
				devices_collection = db.get_collection('devices')

				received_ts = float(received_ts) / 1000
				gmt = pytz.timezone('Asia/Seoul')
				# gmt = pytz.timezone('Europe/London') 

				last_battery_percent_ts_utc = datetime.utcfromtimestamp(int(received_ts))
				last_battery_percent_ts_gmt = last_battery_percent_ts_utc.astimezone(gmt)

				last_battery_percent_date = last_battery_percent_ts_gmt.strftime('%d_%m_%Y')
				print('-------------------------')
				print('received_ts:', received_ts)
				print('last_battery_percent_ts_utc:', last_battery_percent_ts_utc)
				print('last_battery_percent_ts_gmt:', last_battery_percent_ts_gmt)
				print('last_battery_percent_date:', last_battery_percent_date)
				print('-------------------------')

				hasDeviceBatteryStatus = devices_collection.find_one(
					{
						"deviceID": deviceID,
						"battery": battery,
						"last_battery_percent_date": last_battery_percent_date,
					}
				)
				print('hasDeviceBatteryStatus:', hasDeviceBatteryStatus)
				if hasDeviceBatteryStatus is None:
					device_monitor = {
						"deviceID": deviceID,
						"battery": battery,
						"received_ts": received_ts,
						"last_battery_percent_date": last_battery_percent_date,
						"last_battery_percent_ts_utc": last_battery_percent_ts_utc,
						"last_battery_percent_ts_gmt": last_battery_percent_ts_gmt,
						"date": datetime.utcnow()
					}

					device_monitor_id = devices_collection.insert_one(device_monitor).inserted_id
				else:
					devices_collection.update({'deviceID': deviceID}, 
						{'$set': {
							"battery":battery,
							"received_ts": received_ts,
							"last_battery_percent_date": last_battery_percent_date,
							"last_battery_percent_ts_utc": last_battery_percent_ts_utc,
							"last_battery_percent_ts_gmt": last_battery_percent_ts_gmt,
							"date": datetime.utcnow()
							}
						}
					)

				self.write(str("OK"))
				db.close_connection()
			else:
				self.write("DB Error")
		except Exception as e:
			print('DB Error ', str(e))

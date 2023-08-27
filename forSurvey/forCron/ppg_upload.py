import pymongo
import os
import datetime
import glob

# 프로그램 작동 시간을 T 라고 했을 때
# T시 의 결과 => T-1시 부터 T까지의 ppg 갯수
# e.g., 14시 동작 >> 13시부터 14시의 갯수가 14시로 저장
#       15시 동작 >> 14시부터 15시의 갯수가 15시로 저장


UPLOADS = r'/home/wearables/gachon_test'
conn = pymongo.MongoClient("mongodb://admin1:slbm4321@localhost:27017/")
db = conn['users']
sensor_collection = db['sensor_data']

today = datetime.datetime.now()
# today = datetime.datetime(2023, 8, 2, 15, 10)
today = today.replace(minute=0, second=0, microsecond=0)
today_str = today.strftime("%d_%m_%Y")
today_utf = int(today.timestamp())
today_utf_end = int(today.timestamp())
today_utf_start = int ((today - datetime.timedelta(hours=1)).timestamp())


# def get_file_list():
#     userlist = os.listdir(UPLOADS)
    
#     for user in userlist:
#         path = os.path.join(UPLOADS, user)
#         date = os.listdir(path)
#         ppg_count = 0
#         if today_str in date:
#             today_path = os.path.join(path, today_str)
#             # filelist = glob.glob(today_path+'/ppg_*.csv')
#             filelist = glob.glob(today_path+'/PpgGreen_*.csv')
#             for file_ in filelist:
#                 ppg_count += get_ppg_count(file_)
#             print(user, ppg_count)
#         upload_DB(user, ppg_count, today)
    
# def get_ppg_count(csvfile):
#     # ppg_raw = []
#     count = 0
#     with open(csvfile, 'r') as f:
#         next(f)         ## 첫줄의 time, value 제거
#         for line in f:
#             line = line.strip()     ## 공백 및 개행문자 제거
#             time, value = line.replace('"', '').split(',')   ## 쌍따옴표 제거, time / value 분리
#             # if int(time)/1000 < today_utf and int(float(value)) > 10:
#             # if int(time)/1000 <= today_utf and int(float(value)) > 10:
#             #     count += 1
#             if int(time)/1000 <= today_utf_end and int(time)/1000 >= today_utf_start and int(float(value)) > 10:
#                 count += 1
#             # ppg_raw.append([int(time), int(float(value))])
    
#     # for x in ppg_raw:
#     #     if len(x) > 1 and int(x[0])/1000 > today_utf and int(x[1]) > 10:
#     #         print(x)
#     #         count += 1
#     return count


# def upload_DB(user, count, date):
#     sensor_collection = db['sensor_data']
    
#     insert_data = {"userid" : user,
#                    "ppg_count" : count,
#                   "date" : date,
#                    "update" : datetime.datetime.now()}
    
#     try:
#         result = sensor_collection.update_one({"userid" : user, "date" : date},
#                                               {"$set" : insert_data}, upsert = True)
        
#         print("UserID : ", user)
#         print(f"Updated id: {result.upserted_id if result.upserted_id else result.matched_count}\n")
    
        
#     except Exception as e:
#         print(e)


def get_file_list2():
    userlist = os.listdir(UPLOADS)
    
    for user in userlist:
        path = os.path.join(UPLOADS, user)
        date = os.listdir(path)
        if today_str in date:
            today_path = os.path.join(path, today_str)
            filelist = glob.glob(today_path+'/PpgGreen_*.csv')
            get_ppg_count2(user, filelist)
    
def get_ppg_count2(user, filelist):  
    start = today.replace(hour=0)
    for x in range(24):
        count = 0
        end = start + datetime.timedelta(hours=1)
        if end > datetime.datetime.now():
            break

        for file_ in filelist:
            with open(file_, 'r') as f:
                next(f)         ## 첫줄의 time, value 제거
                for line in f:
                    line = line.strip()     ## 공백 및 개행문자 제거
                    time, value = line.replace('"', '').split(',')   ## 쌍따옴표 제거, time / value 분리
                    if int(time)/1000 <= end.timestamp() and int(time)/1000 >= start.timestamp() and int(float(value)) > 10:
                        count += 1
        print(count)
        upload_DB2(user, count, end)
        start = start + datetime.timedelta(hours=1)

def upload_DB2(user, count, date):
    insert_data = {"userid" : user,
                   "ppg_count" : count,
                   "date" : date,
                   "hour" : date.hour,
                   "update" : datetime.datetime.now()}
    
    existing_document = sensor_collection.find_one({"userid": user, "date": date})

    if existing_document:
        if existing_document['ppg_count'] != count:
            result = sensor_collection.update_one({"userid" : user, "date" : date, "hour" : date.hour},
                                              {"$set" : insert_data}, upsert = True)
            print("UserID : ", user)
            print("count : ", count)
            print(f"{date} Yes Update")
        
        else:
            print("UserID : ", user)
            print(f"{date} No Update")

    else:
        result = sensor_collection.update_one({"userid" : user, "date" : date, "hour" : date.hour},
                                              {"$set" : insert_data}, upsert = True)
        print("UserID : ", user)
        print("count : ", count)
        print(f"{date} Yes Insert")

if __name__ == '__main__':
    get_file_list2()
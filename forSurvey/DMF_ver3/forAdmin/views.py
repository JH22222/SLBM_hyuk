from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import datetime
import pandas as pd
import pymongo
import os
import logging
from db.db import MongoDB
from config.constants import (
	UPLOAD_PATH,
    GACHON_UPLOAD_PATH,
)
from rest_framework.decorators import api_view #api
from rest_framework.response import Response #api
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi   


experimentCode= openapi.Parameter('experimentCode', openapi.IN_QUERY, description='실험 코드 (e.g., gc_test, knu_test)', required=True, type=openapi.TYPE_STRING)
logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method='get',
    operation_summary='Get Battery Data',
    operation_description='최신 남은 배터리 용량(%) 상태',
    tags=['For Admin'], 
    manual_parameters=[experimentCode], 
    responses={200: 'Success', 400:'요청 오류', 401:'해당 User의 DeviceID 찾을 수 없음', 402 : 'DB 접속 오류'})
@api_view(['get'])
def getBatteryData(request):
    if request.method == 'GET':
        data = request.GET
        experimentCode = data.get('experimentCode')
        
        print(experimentCode)
        
        db = MongoDB()
        try:
            if db._conn:
                devices_collection = db.get_collection('devices')
                users_collection = db.get_collection('users')
                query_toFindeDeviceID = {'name' : experimentCode}
                projection_toFindDeviceID = {"_id" : 0, "deviceID" : 1, "authCode" : 1}
            

                try:
                    cursor = users_collection.find(query_toFindeDeviceID, projection_toFindDeviceID)
                    userInfo = list(cursor)
                    # print(userInfo)
                except Exception as e:        ## deviceID가 없는 경우
                    return HttpResponse('No deviceId', status = 401)

                lastBattery = []
                
                for user in userInfo : 
                    query_toFindBatteryInfo = {"deviceID" : user.get('deviceID')}
                    projection_toFindDeviceID = {"_id" : 0, "battery" : 1, "last_battery_percent_ts_kst" : 1}
                    # print(user)
                    record = devices_collection.find(query_toFindBatteryInfo, projection_toFindDeviceID).sort('last_battery_percent_ts_kst', -1).limit(1)
                    # print(list(record))
                    result = {}
                    for doc in record:
                        result = {
                            'battery': doc.get('battery'),
                            'last_battery_percent_ts_kst': doc.get('last_battery_percent_ts_kst')
                        }
                    
                    # lastBattery = {'userID' : user.get('authCode'), 'data' : result}
                    lastBattery.append({'userID' : user.get('authCode'), 'data' : result})
                    
                    
                responseData = {'experimentCode' : experimentCode, 'lastBattery' : lastBattery}
            
            
    
        except Exception as e:
            print('DB Error', str(e))
            return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
        
        
        return JsonResponse(responseData,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)

    else:
        return HttpResponse('요청 오류', status = 400)        # 요청 오류    

@swagger_auto_schema(
    method='get',
    operation_summary='Get Survey Record',
    operation_description='해당 실험 참가자들의 수면일지 T day, T-1 day 여부',
    tags=['For Admin'], 
    manual_parameters=[experimentCode], 
    responses={200: 'Success', 400:'요청 오류', 401:'유효하지 않은 실험 코드', 402 : 'DB 접속 오류'})
@api_view(['get'])
def getSleepRecord(request):
    if request.method == 'GET':
        data = request.GET
        experimentCode = data.get('experimentCode')     ## 실험 코드
        
        print(experimentCode)
        
        db = MongoDB()
        try:
            if db._conn:
                users_collection = db.get_collection('users')
                query_toFindeDeviceID = {'name' : experimentCode}
                projection_toFindDeviceID = {"_id" : 0, "authCode" : 1, "date" : 1}
                
                try:
                    cursor = users_collection.find(query_toFindeDeviceID, projection_toFindDeviceID)
                    userInfo = list(cursor)
                    userList = [item['authCode'] for item in userInfo]
                    print(userInfo)
                except Exception as e:        ## 실험코드가 없는 경우
                    return HttpResponse('No experimentCode', status = 401)
                
        except Exception as e:
            print('DB Error', str(e))
            return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
        
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterDay = today - datetime.timedelta(days=1)
        print(today)
        print(yesterDay)
        
        try:
            if db._conn:
                result = []
                surveyCheckY = []
                polls_collection = db.get_collection('polls')
                
                checkDayStart = yesterDay
                checkDayEnd = yesterDay + datetime.timedelta(days=1)
                
                for user in userList:
                    cursor = polls_collection.find({'$and' : [ {'userid' : user}, {'date':{'$gte':checkDayStart}}, {'date': {'$lte' : checkDayEnd}}, {'tag': '수면 일지'}]})
                    if len(list(cursor)) == 5:
                        data = {"userID" : user, "response" : "O"}
                    else:
                        data = {"userID" : user, "response" : "X"}
                    surveyCheckY.append(data)
                
                surveyCheckT = []
                checkDayStart = today
                checkDayEnd = today + datetime.timedelta(days=1)
                    
                for user in userList:
                    cursor = polls_collection.find({'$and' : [ {'userid' : user}, {'date':{'$gte':checkDayStart}}, {'date': {'$lte' : checkDayEnd}}, {'tag': '수면 일지'}]})
                    if len(list(cursor)) == 5:
                        data = {"userID" : user, "response" : "O"}
                    else:
                        data = {"userID" : user, "response" : "X"}
                    surveyCheckT.append(data)
                
                yesterDayResult = {"date" : yesterDay, "result" : surveyCheckY}
                todayResult = {"date" : today, "result" : surveyCheckT}
                
                result.append(yesterDayResult)
                result.append(todayResult)
                
                return JsonResponse(result,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)
            else:
                return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
        except Exception as e:
            print('DB Error', str(e))
            return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류

        
    else:
        return HttpResponse('요청 오류', status = 400)        # 요청 오류  
    


@swagger_auto_schema(
    method='get',
    operation_summary='Get Survey Record',
    operation_description='해당 실험 참가자들의 설문 응답 여부',
    tags=['For Admin'], 
    manual_parameters=[experimentCode], 
    responses={200: 'Success', 400:'요청 오류', 401:'유효하지 않은 실험 코드', 402 : 'DB 접속 오류'})
@api_view(['get'])
def getSurveyRecord(request):
    if request.method == 'GET':
        data = request.GET
        experimentCode = data.get('experimentCode')     ## 실험 코드
        
        print(experimentCode)
        
        db = MongoDB()
        try:
            if db._conn:
                users_collection = db.get_collection('users')
                query_toFindeDeviceID = {'name' : experimentCode}
                projection_toFindDeviceID = {"_id" : 0, "authCode" : 1, "date" : 1}
                
                try:
                    cursor = users_collection.find(query_toFindeDeviceID, projection_toFindDeviceID)
                    userInfo = list(cursor)
                    userList = [item['authCode'] for item in userInfo]
                    print(userInfo)
                except Exception as e:        ## 실험코드가 없는 경우
                    return HttpResponse('No experimentCode', status = 401)
                
        except Exception as e:
            print('DB Error', str(e))
            return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
        
        today = datetime.datetime.now()
        startDay = datetime.datetime.strptime(userInfo[0].get('date'), "%Y%m%d")
        week = int((today - startDay).days / 7)

        result = []
        try:
            if db._conn:
                polls_collection = db.get_collection('polls')
                for week in range(week+1):
                    checkWeekStart = startDay
                    checkWeekEnd = startDay + datetime.timedelta(weeks=1)
                    surveyResult = []
                    for user in userList:
                        cursor = polls_collection.find({'$and' : [ {'userid' : user}, {'date':{'$gte':checkWeekStart}}, {'date': {'$lte' : checkWeekEnd}}, {'tag': {'$ne': '수면 일지'}}]})
                        if len(list(cursor)) > 0:
                            data = {"userID" : user, "response" : "O"}
                        else:
                            data = {"userID" : user, "response" : "X"}
                        surveyResult.append(data)
                    
                    result.append({"week" : week, "result" : surveyResult})
                
                return JsonResponse(result,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)

                
        except Exception as e:
            print('DB Error', str(e))
            return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류

        
    else:
        return HttpResponse('요청 오류', status = 400)        # 요청 오류    


@swagger_auto_schema(
    method='get',
    operation_summary='Get PPG Count',
    operation_description='해당 실험 참가자들의 수집된 PPG 신호의 개수',
    tags=['For Admin'], 
    manual_parameters=[experimentCode], 
    responses={200: 'Success', 400:'요청 오류', 401:'유효하지 않은 실험 코드', 402 : 'DB 접속 오류'})
@api_view(['get'])
def getCnt_PPG(request):
    if request.method == 'GET':
        data = request.GET
        experimentCode = data.get('experimentCode')     ## 실험 코드
        logger.info("ExperimentCode : %s", experimentCode)
        
        print(experimentCode)
        
        db = MongoDB()
        
        try:                        ## 실험코드에 대한 유저 리스트 가져오기
            if db._conn:
                users_collection = db.get_collection('users')
                query_toFindeDeviceID = {'name' : experimentCode}
                projection_toFindDeviceID = {"_id" : 0, "authCode" : 1}
                
                try:
                    cursor = users_collection.find(query_toFindeDeviceID, projection_toFindDeviceID)
                    userInfo = list(cursor)
                    userList = [item['authCode'] for item in userInfo]
                    # print(userInfo)
                except Exception as e:        ## 실험코드가 없는 경우
                    return HttpResponse('No experimentCode', status = 401)
                
        except Exception as e:
            print('DB Error', str(e))
            return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
        try:                        
            if db._conn:
                ppg_record = []
                start = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
                end = start + datetime.timedelta(days=1)
                print(start, end)
                sensor_collection = db.get_collection('sensor_data')
                for user in userList:
                    result = []
                    sensor_datas = sensor_collection.find({'userid' : user, 'date': {'$gte': start,'$lt': end}}).sort('date', pymongo.ASCENDING)
                    for sensor_data in sensor_datas:
                        # data = {"userid" : sensor_data['userid'], "ppg_count" : sensor_data['ppg_count'], "hour" : sensor_data['date'].hour}
                        # data = {"hour" : sensor_data['date'].hour, "ppg_count" : sensor_data['ppg_count']}
                        data = {"hour" : sensor_data['hour'], "ppg_count" : sensor_data['ppg_count']}
                        result.append(data)
                        print(data)
                    ppg_record.append({'userid' : user, 'data' : result})
                print(ppg_record)
        except Exception as e:
            print('DB Error', str(e))
            return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
        
        total_response = {'experimentCode' : experimentCode, 'ppg_date' : datetime.datetime.now().strftime("%Y-%m-%d"),
                          'ppg_record' : ppg_record} 
        
        
        return JsonResponse(total_response,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)
    else:
        return HttpResponse('요청 오류', status = 400)        # 요청 오류 
    

# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render
# import datetime
# import pandas as pd
# import pymongo
# import os
# from db.db import MongoDB
# from config.constants import (
# 	UPLOAD_PATH,
#     GACHON_UPLOAD_PATH,
# )
# from rest_framework.decorators import api_view #api
# from rest_framework.response import Response #api
# from drf_yasg.utils       import swagger_auto_schema
# from drf_yasg             import openapi   

# userID= openapi.Parameter('userID', openapi.IN_QUERY, description='사용자 ID (ex. AA00)', required=True, type=openapi.TYPE_STRING)
# timestamp= openapi.Parameter('timestamp', openapi.IN_QUERY, description='날짜 (ex. 2023-01-01)', required=True, type=openapi.TYPE_STRING)
# week= openapi.Parameter('week', openapi.IN_QUERY, description='요청 주차 (ex. 1)', required=True, type=openapi.TYPE_INTEGER)
# experimentCode= openapi.Parameter('experimentCode', openapi.IN_QUERY, description='실험 코드 (e.g., gc_test, knu_test)', required=True, type=openapi.TYPE_STRING)


# @swagger_auto_schema(
#     method='get',
#     operation_summary='Get Battery Data',
#     operation_description='업로드된 배터리 데이터 중 가장 최신 데이터 반환',
#     tags=['For Admin'], 
#     manual_parameters=[userID], 
#     responses={200: 'Success', 400:'요청 오류', 401:'해당 User의 DeviceID 찾을 수 없음', 402 : 'DB 접속 오류'})
# @api_view(['get'])
# def getBatteryData(request):
#     if request.method == 'GET':
#         data = request.GET
#         userID = data.get('userID')
        
#         print(userID)
        
#         db = MongoDB()
#         try:
#             if db._conn:
#                 devices_collection = db.get_collection('devices')
#                 users_collection = db.get_collection('users')
                
#                 try:
#                     cursor = users_collection.find_one({'authCode' : userID})
#                     deviceID = cursor['deviceID']
#                     print(deviceID)
#                 except Exception as e:        ## deviceID가 없는 경우
#                     return HttpResponse('No deviceId', status = 401)
                

#                 record = devices_collection.find({'deviceID' : deviceID}).sort('last_battery_percent_ts_gmt', -1).limit(1)
#                 for doc in record:
#                     result = {
#                         'battery': doc['battery'],
#                         'last_battery_percent_ts_gmt': doc['last_battery_percent_ts_gmt']
#                     }
                
#                 lastBattery = {'userID' : userID, 'data' : result}
#                 print(result)
                
    
#         except Exception as e:
#             print('DB Error', str(e))
#             return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
        
        
#         # userPath = os.path.join(UPLOAD_PATH, userID)
#         # userPath = os.path.join('/home/wearables/gachon_test/', userID)
#         # if not os.path.isdir(userPath):
#         #     return JsonResponse({'erro' : 'No User directory'}, status = 401)    ## 디렉토리 없음
        
#         # folders = [folder for folder in os.listdir(userPath) if os.path.isdir(os.path.join(userPath, folder)) and folder.count('_') == 2]
#         # latest_folder = max(folders, key=lambda folder: datetime.datetime.strptime(folder, '%d_%m_%Y'))
#         # print(latest_folder)

#         # userLastPath = os.path.join(userPath, latest_folder)
        
#         # json_files = [file for file in os.listdir(userLastPath) if file.endswith('.json')]
#         # latest_json_file = max(json_files, key=lambda file: os.path.getmtime(os.path.join(userLastPath, file)))
        
#         # jsonPath = os.path.join(userLastPath, latest_json_file)
        
#         # with open(jsonPath, 'r') as f:
#         #     lastBattery = json.load(f)
        
#         # print(lastBattery)
        
        
        
#         return JsonResponse(lastBattery,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)

        
#     else:
#         return JsonResponse({'error' : '요청 오류'}, status = 400)

# @swagger_auto_schema(
#     method='get',
#     operation_summary='Get Battery Data',
#     operation_description='최신 남은 배터리 용량(%) 상태',
#     tags=['For Admin'], 
#     manual_parameters=[experimentCode], 
#     responses={200: 'Success', 400:'요청 오류', 401:'해당 User의 DeviceID 찾을 수 없음', 402 : 'DB 접속 오류'})
# @api_view(['get'])
# def getBatteryData_tmp(request):
#     if request.method == 'GET':
#         data = request.GET
#         experimentCode = data.get('experimentCode')
        
#         print(experimentCode)
        
#         db = MongoDB()
#         try:
#             if db._conn:
#                 devices_collection = db.get_collection('devices')
#                 users_collection = db.get_collection('users')
#                 query_toFindeDeviceID = {'name' : experimentCode}
#                 projection_toFindDeviceID = {"_id" : 0, "deviceID" : 1, "authCode" : 1}
            

#                 try:
#                     cursor = users_collection.find(query_toFindeDeviceID, projection_toFindDeviceID)
#                     userInfo = list(cursor)
#                     # print(userInfo)
#                 except Exception as e:        ## deviceID가 없는 경우
#                     return HttpResponse('No deviceId', status = 401)

#                 lastBattery = []
                
#                 for user in userInfo : 
#                     query_toFindBatteryInfo = {"deviceID" : user.get('deviceID')}
#                     projection_toFindDeviceID = {"_id" : 0, "battery" : 1, "last_battery_percent_ts_gmt" : 1}
#                     # print(user)
#                     record = devices_collection.find(query_toFindBatteryInfo, projection_toFindDeviceID).sort('last_battery_percent_ts_gmt', -1).limit(1)
#                     # print(list(record))
#                     result = {}
#                     for doc in record:
#                         result = {
#                             'battery': doc.get('battery'),
#                             'last_battery_percent_ts_gmt': doc.get('last_battery_percent_ts_gmt')
#                         }
                    
#                     # lastBattery = {'userID' : user.get('authCode'), 'data' : result}
#                     lastBattery.append({'userID' : user.get('authCode'), 'data' : result})
                    
                    
#                 responseData = {'experimentCode' : experimentCode, 'lastBattery' : lastBattery}
            
            
    
#         except Exception as e:
#             print('DB Error', str(e))
#             return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
        
        
#         return JsonResponse(responseData,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)

#     else:
#         return HttpResponse('요청 오류', status = 400)        # 요청 오류    
        
#     else:
#         return HttpResponse('요청 오류', status = 400)

# @swagger_auto_schema(
#     method='get',
#     operation_summary='Get Data Exist',
#     operation_description='요청 날짜의 디렉토리 파일 리스트',
#     tags=['For Admin'], 
#     manual_parameters=[userID, timestamp], 
#     responses={200: 'Success', 400:'요청 오류', 401:'해당 User 디렉토리 없음', 402 : '해당 날짜 디렉토리 없음'})
# @api_view(['get'])
# def getDataExist(request):
#     if request.method == 'GET':
#         data = request.GET
#         userID = data.get('userID')     ## 우리가 아는 userid
#         timestamp = data.get('timestamp')      ## 요청 timestamp yyyy-mm-dd
        
#         userPath = os.path.join(UPLOAD_PATH, userID)
#         # print(userPath)
#         if not os.path.isdir(userPath):
#             return JsonResponse({'erro' : 'No User directory'}, status = 401)    ## 디렉토리 없음
        
#         try : 
#             target_dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
#         except Exception as e:
#             return JsonResponse({'error' : 'timestamp form Error'}, status = 402)

#     else:
#                 print('DB Error', str(e))
#                 return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
        
        
# @swagger_auto_schema(
#     method='get',
#     operation_summary='Get Sleep Record',
#     operation_description='요청 날짜의 수면 일지 기록',
#     tags=['For Admin'], 
#     manual_parameters=[userID, timestamp], 
#     responses={200: 'Success', 400:'요청 오류', 401:'UserID 입력 오류', 402 : 'timestamp 양식 오류', 403 : '해당 날짜의 수면 일지 없음', 405 : 'DB 접속 오류'})
# @api_view(['get'])
# # Create your views here.
# def getSleepRecord(request):
#     if request.method == 'GET':
#         data = request.GET
#         userID = data.get('userID')     ## 우리가 아는 userid
#         timestamp = data.get('timestamp')      ## 요청 timestamp yyyy-mm-dd
#         try : 
#             date_dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
#         except Exception as e:
#             return JsonResponse({'error' : 'timestamp form Error'}, status = 402)
#         date_dt = date_dt.timestamp()
#         date_dt_start = datetime.datetime.utcfromtimestamp(date_dt)
#         date_dt_end = date_dt_start + datetime.timedelta(days=1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        
#         print(date_dt_start)
#         print(date_dt_end)
        
        
#         db = MongoDB()
#         try:
#             if db._conn:
#                 polls_collection = db.get_collection('polls')
#                 users_collection = db.get_collection('users')
#                 isexist = users_collection.find_one({"authCodeLast4":userID})
#                 cursor = polls_collection.find({'$and' : [{'date':{'$gte':date_dt_start}}, {'date': {'$lte' : date_dt_end}}, {'userid' : userID}]})
#                 print(bool(isexist))
#                 if isexist:
#                     print('Print ' + userID + ' Record....')
#                 else:
#                     print('userID error')
#                     return JsonResponse({'error': 'userID Error'}, status = 401)
                
#                 try : 
#                     df = pd.DataFrame(list(cursor))
#                     df['kr_date'] = df['date'] + datetime.timedelta(hours = 8)
#                     df_handling = df
#                     df_handling = df_handling.drop_duplicates(['tag','poll_key'])
#                     df_handling = df_handling[df_handling.tag == '수면 일지']
#                     df_handling = df_handling.reset_index(drop = True)
#                     df_handling = df_handling[['tag', 'poll_key', 'poll', 'kr_date']]
                    
#                 except Exception as e:
#                     return JsonResponse({'error' : 'Empty DB'}, status = 403)
                
#                 sleepRecord = df_handling.to_json(orient='records', force_ascii=False)
#                 sleepRecord = {userID : sleepRecord}
                
#                 print(sleepRecord)
                
#                 return JsonResponse(sleepRecord,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)

#         except Exception as e:
#             print('DB Error', str(e))
#             return JsonResponse({'error' : 'DB 접속 오류'}, status = 405)        # Db 접속 오류
#     else:
#         return JsonResponse({'error' : '요청 오류'}, status = 400)
    
#     return HttpResponse(200)

# def getSleepRecord_tmp(request):
#     if request.method == 'GET':
#         data = request.GET
#         experimentCode = data.get('experimentCode')     ## 실험 코드
        
#         print(experimentCode)
        
#         db = MongoDB()
#         try:
#             if db._conn:
#                 users_collection = db.get_collection('users')
#                 query_toFindeDeviceID = {'name' : experimentCode}
#                 projection_toFindDeviceID = {"_id" : 0, "authCode" : 1, "date" : 1}
                
#                 try:
#                     cursor = users_collection.find(query_toFindeDeviceID, projection_toFindDeviceID)
#                     userInfo = list(cursor)
#                     userList = [item['authCode'] for item in userInfo]
#                     print(userInfo)
#                 except Exception as e:        ## 실험코드가 없는 경우
#                     return HttpResponse('No experimentCode', status = 401)
                
#         except Exception as e:
#             print('DB Error', str(e))
#             return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
        
#         today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
#         yesterDay = today - datetime.timedelta(days=1)
#         print(today)
#         print(yesterDay)
        
#         try:
#             if db._conn:
#                 result = []
#                 surveyCheckY = []
#                 polls_collection = db.get_collection('polls')
                
#                 checkDayStart = yesterDay
#                 checkDayEnd = yesterDay + datetime.timedelta(days=1)
                
#                 for user in userList:
#                     cursor = polls_collection.find({'$and' : [ {'userid' : user}, {'date':{'$gte':checkDayStart}}, {'date': {'$lte' : checkDayEnd}}, {'tag': '수면 일지'}]})
#                     if len(list(cursor)) == 5:
#                         data = {"userID" : user, "response" : "O"}
#                     else:
#                         data = {"userID" : user, "response" : "X"}
#                     surveyCheckY.append(data)
                
#                 surveyCheckT = []
#                 checkDayStart = today
#                 checkDayEnd = today + datetime.timedelta(days=1)
                    
#                 for user in userList:
#                     cursor = polls_collection.find({'$and' : [ {'userid' : user}, {'date':{'$gte':checkDayStart}}, {'date': {'$lte' : checkDayEnd}}, {'tag': '수면 일지'}]})
#                     if len(list(cursor)) == 5:
#                         data = {"userID" : user, "response" : "O"}
#                     else:
#                         data = {"userID" : user, "response" : "X"}
#                     surveyCheckT.append(data)
                
#                 yesterDayResult = {"date" : yesterDay, "result" : surveyCheckY}
#                 todayResult = {"date" : today, "result" : surveyCheckT}
                
#                 result.append(yesterDayResult)
#                 result.append(todayResult)
                
#                 return JsonResponse(result,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)

                
#         except Exception as e:
#             print('DB Error', str(e))
#             return JsonResponse({'error' : 'DB 접속 오류'}, status = 405)        # Db 접속 오류

        
#     else:
#         return JsonResponse({'error' : '요청 오류'}, status = 400)
    

# @swagger_auto_schema(
#     method='get',
#     operation_summary='Get Survey Record',
#     operation_description='요청 주차의 설문 기록',
#     tags=['For Admin'], 
#     manual_parameters=[userID, week], 
#     responses={200: 'Success', 400:'요청 오류', 401:'UserID 입력 오류', 402 : 'timestamp 양식 오류', 403 : '해당 날짜의 수면 일지 없음', 405 : 'DB 접속 오류'})
# @api_view(['get'])
# def getSurveyRecord(request):
#     if request.method == 'GET':
#         data = request.GET
#         userID = data.get('userID')     ## 우리가 아는 userid
#         week = int(data.get('week'))                 ## 요청 주차
#         db = MongoDB()
#         try:
#             if db._conn:
#                 users_collection = db.get_collection('users')
                
#                 user = users_collection.find_one({'authCode' : userID})
#                 if user:
#                     print('Print ' + userID + ' Record....')
#                 else:
#                     print('userID error')
#                     return JsonResponse({'error': 'userID Error'}, status = 401)
        
#         except Exception as e:
#             print('DB Error', str(e))
#             return JsonResponse({'error' : 'DB 접속 오류'}, status = 405)        # Db 접속 오류        

        
#         try : 
#             survey_dt = datetime.datetime.strptime(user['date'], '%Y%m%d')
#             survey_dt_start = survey_dt + datetime.timedelta(days=((week*7)))
#             survey_dt_end = survey_dt_start + datetime.timedelta(days=7)
#         except Exception as e:
#             return JsonResponse({'error' : 'timestamp form Error'}, status = 402)
        
        
#         starttime = survey_dt_start
#         survey_dt_start = survey_dt_start.timestamp()
#         survey_dt_end = survey_dt_end.timestamp()
        
#         survey_dt_start = datetime.datetime.utcfromtimestamp(survey_dt_start)
#         print('Start DATE : ',survey_dt_start)
#         survey_dt_end = datetime.datetime.utcfromtimestamp(survey_dt_end)
#         print('End DATE : ',survey_dt_end)
        
        
        
#         try:
#             if db._conn:
#                 polls_collection = db.get_collection('polls')
#                 users_collection = db.get_collection('users')
#                 cursor = polls_collection.find({'$and' : [ {'userid' : userID}, {'date':{'$gte':survey_dt_start}}, {'date': {'$lte' : survey_dt_end}}]})
                
                
#                 try : 
#                     df = pd.DataFrame(list(cursor))
#                     df['kr_date'] = df['date'] + datetime.timedelta(hours = 8)
#                     df_handling = df
#                     df_handling = df_handling.drop_duplicates(['tag','poll_key'])
#                     df_handling = df_handling[df_handling.tag != '수면 일지']
#                     df_handling = df_handling.reset_index(drop = True)
#                     df_handling = df_handling[['tag', 'poll_key', 'poll', 'kr_date']]
#                 except Exception as e:
#                     return JsonResponse({'error' : 'Empty DB'}, status = 403)
                
#                 surveyRecord = df_handling.to_json(orient='records', force_ascii=False)

#                 surveyRecord = {'userID' : userID, 'week' : week, 'data' : surveyRecord}
                
#                 print(surveyRecord)
                
#                 return JsonResponse(surveyRecord,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)

#         except Exception as e:
#             print('DB Error', str(e))
#             return JsonResponse({'error' : 'DB 접속 오류'}, status = 405)        # Db 접속 오류
#     else:
#         return JsonResponse({'error' : '요청 오류'}, status = 400)
    
#     return HttpResponse(200)

# @swagger_auto_schema(
#     method='get',
#     operation_summary='Get Survey Record',
#     operation_description='해당 실험 참가자들의 설문 응답 여부',
#     tags=['For Admin'], 
#     manual_parameters=[experimentCode], 
#     responses={200: 'Success', 400:'요청 오류', 401:'유효하지 않은 실험 코드', 402 : 'DB 접속 오류'})
# @api_view(['get'])
# def getSurveyRecord_tmp(request):
#     if request.method == 'GET':
#         data = request.GET
#         experimentCode = data.get('experimentCode')     ## 실험 코드
        
#         print(experimentCode)
        
#         db = MongoDB()
#         try:
#             if db._conn:
#                 users_collection = db.get_collection('users')
#                 query_toFindeDeviceID = {'name' : experimentCode}
#                 projection_toFindDeviceID = {"_id" : 0, "authCode" : 1, "date" : 1}
                
#                 try:
#                     cursor = users_collection.find(query_toFindeDeviceID, projection_toFindDeviceID)
#                     userInfo = list(cursor)
#                     userList = [item['authCode'] for item in userInfo]
#                     print(userInfo)
#                 except Exception as e:        ## 실험코드가 없는 경우
#                     return HttpResponse('No experimentCode', status = 401)
                
#         except Exception as e:
#             print('DB Error', str(e))
#             return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
        
#         today = datetime.datetime.now()
#         startDay = datetime.datetime.strptime(userInfo[0].get('date'), "%Y%m%d")
#         week = int((today - startDay).days / 7)

#         result = []
#         try:
#             if db._conn:
#                 polls_collection = db.get_collection('polls')
#                 for week in range(week+1):
#                     checkWeekStart = startDay
#                     checkWeekEnd = startDay + datetime.timedelta(weeks=1)
#                     surveyResult = []
#                     for user in userList:
#                         cursor = polls_collection.find({'$and' : [ {'userid' : user}, {'date':{'$gte':checkWeekStart}}, {'date': {'$lte' : checkWeekEnd}}, {'tag': {'$ne': '수면 일지'}}]})
#                         if len(list(cursor)) > 0:
#                             data = {"userID" : user, "response" : "O"}
#                         else:
#                             data = {"userID" : user, "response" : "X"}
#                         surveyResult.append(data)
                    
#                     result.append({"week" : week, "result" : surveyResult})
                
#                 return JsonResponse(result,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)

                
#         except Exception as e:
#             print('DB Error', str(e))
#             return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류

        
#     else:
#         return HttpResponse('요청 오류', status = 400)        # 요청 오류    


# @swagger_auto_schema(
#     method='get',
#     operation_summary='Get PPG Count',
#     operation_description='해당 실험 참가자들의 수집된 PPG 신호의 개수',
#     tags=['For Admin'], 
#     manual_parameters=[experimentCode], 
#     responses={200: 'Success', 400:'요청 오류', 401:'유효하지 않은 실험 코드', 402 : 'DB 접속 오류'})
# @api_view(['get'])
# def getCnt_PPG(request):
#     if request.method == 'GET':
#         data = request.GET
#         experimentCode = data.get('experimentCode')     ## 실험 코드
        
#         print(experimentCode)
        
#         db = MongoDB()
        
#         try:                        ## 실험코드에 대한 유저 리스트 가져오기
#             if db._conn:
#                 users_collection = db.get_collection('users')
#                 query_toFindeDeviceID = {'name' : experimentCode}
#                 projection_toFindDeviceID = {"_id" : 0, "authCode" : 1}
                
#                 try:
#                     cursor = users_collection.find(query_toFindeDeviceID, projection_toFindDeviceID)
#                     userInfo = list(cursor)
#                     userList = [item['authCode'] for item in userInfo]
#                     # print(userInfo)
#                 except Exception as e:        ## 실험코드가 없는 경우
#                     return HttpResponse('No experimentCode', status = 401)
                
#         except Exception as e:
#             print('DB Error', str(e))
#             return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
#         try:                        
#             if db._conn:
#                 ppg_record = []
#                 start = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
#                 end = start + datetime.timedelta(days=1)
#                 print(start, end)
#                 sensor_collection = db.get_collection('sensor_data')
#                 for user in userList:
#                     result = []
#                     sensor_datas = sensor_collection.find({'userid' : user, 'date': {'$gte': start,'$lt': end}}).sort('date', pymongo.ASCENDING)
#                     for sensor_data in sensor_datas:
#                         # data = {"userid" : sensor_data['userid'], "ppg_count" : sensor_data['ppg_count'], "hour" : sensor_data['date'].hour}
#                         data = {"hour" : sensor_data['date'].hour, "ppg_count" : sensor_data['ppg_count']}
#                         result.append(data)
#                         print(data)
#                     ppg_record.append({'userid' : user, 'data' : result})
#                 print(ppg_record)
#         except Exception as e:
#             print('DB Error', str(e))
#             return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
        
#         total_response = {'experimentCode' : experimentCode, 'ppg_date' : datetime.datetime.now().strftime("%Y-%m-%d"),
#                           'ppg_record' : ppg_record} 
        
#         return JsonResponse(total_response,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)
#     else:
#         return HttpResponse('요청 오류', status = 400)        # 요청 오류 
    
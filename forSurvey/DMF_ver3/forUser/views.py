from django.shortcuts import render
import csv
import json
import os
import pandas as pd
import pymongo
import time
import datetime

from django.views.decorators.csrf import csrf_exempt
from pandas.io.json import json_normalize
from django.http import FileResponse, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pytz
from config.constants import (
	__UPLOADS__,
  __dbloc__
)
from db.db import MongoDB 
# Create your views here.

from django.shortcuts import render
from rest_framework.decorators import api_view #api
from rest_framework.response import Response #api
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi   

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination

import csv
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




userID= openapi.Parameter('userID', openapi.IN_QUERY, description='사용자 ID (ex. AA00)', required=True, type=openapi.TYPE_STRING)
deviceID= openapi.Parameter('deviceID', openapi.IN_QUERY, description='device ID(ex. randomValue123456789)', required=True, type=openapi.TYPE_STRING)
regID= openapi.Parameter('regID', openapi.IN_QUERY, description='regID (ex. (ex. randomValue123456789))', required=True, type=openapi.TYPE_STRING)
battery= openapi.Parameter('battery', openapi.IN_QUERY, description='배터리 상태', required=True, type=openapi.TYPE_INTEGER)
timestamp= openapi.Parameter('timestamp', openapi.IN_QUERY, description='날짜 (ex. 2023-01-01)', required=True, type=openapi.TYPE_STRING)
csvfile= openapi.Parameter('csvfile', openapi.IN_BODY, description='전송될 워치 내의 데이터. csv 형식', required=True, type=openapi.TYPE_FILE)



@swagger_auto_schema(
    method='get',
    operation_summary='Regist User',
    operation_description='사용자 등록',
    tags=['For User'], 
    manual_parameters=[userID, deviceID, regID, timestamp], 
    responses={200: 'Success', 400:'요청 오류', 401:'미등록된 userID', 402:'DB 접속 오류'})
@api_view(['get'])
@csrf_exempt
def registUser(request):
    
    if request.method == 'GET':
        data = request.GET
        userID = data.get('userID')     ## 우리가 아는 userid
        duid = data.get('deviceID')             ## 난수값
        regID = data.get('regID')           ## 난수값
        timestamp = data.get('timestamp')
        
        db = MongoDB()

        try:
            if db._conn:
                users_collection = db.get_collection('users')
                users_collection.update_one({'authCodeLast4': str(userID)}, {'$set': {'deviceID':str(duid)}})
                users_collection.update_one({'authCodeLast4': str(userID)}, {'$set': {'regID':str(regID)}})
                update_user_record = users_collection.find_one({"authCodeLast4":userID})
                
                print(update_user_record)
                if update_user_record:
                    print('Update User record... UserID registered')
                    print(users_collection.find_one({'authCodeLast4':str(userID)}))
                    
                else :
                    print('authCode error')
                    return HttpResponse('미등록된 userID', status = 401)    # AuthCode 오류
            
            else:   
                return HttpResponse('DB 접속 오류', status = 402)        # db 접속 오류
                
        except Exception as e:
            print('DB Error', str(e))
            return HttpResponse('DB 접속 오류', status = 402)        # Db 접속 오류
    else:
        return HttpResponse('요청 오류', status = 400)        # 요청 오류
        
        
    
    return HttpResponse(userID + ' successfully regist', status = 200)



# @swagger_auto_schema(
#     method='post',
#     operation_summary='postCurrentData',
#     operation_description='웨어러블 기기에서 저장된 데이터들 서버로 업로드',
#     tags=['워치 데이터 전송'],
#     request_body=openapi.Schema(
#     type=openapi.TYPE_OBJECT,
#     properties={
#         'csvfile': csvfile,
#         'userID': openapi.Schema(title='userID', type='string',required='True', description='사용자 ID(ex. AA00)'),
#         'battery': openapi.Schema(title='Battery', type='integer',required='True', description='배터리 상태'),
#         'timestamp': openapi.Schema(description='데이터가 수집되기 시작한 시간 ; unixTime (ex. 1672498800)', title='userID', type='string',required='True'),
#     }, 
#     # responses={200: 'Success', 400: 'Fail', 401 : '이미 존재하는 파일', 402 : '전송된 데이터가 CSV가 아님'}
#      responses={
#         200: openapi.Response(
#             description='성공',
#             schema=openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     'message': openapi.Schema(
#                         type=openapi.TYPE_STRING,
#                         description='결과 메시지'
#                     ),
#                     'data': openapi.Schema(
#                         type=openapi.TYPE_OBJECT,
#                         properties={
#                             # 데이터에 대한 스키마 정의
#                         },
#                     ),
#                 },
#             ),
#         ),
#         400: openapi.Response(
#             description='실패',
#             schema=openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     'message': openapi.Schema(
#                         type=openapi.TYPE_STRING,
#                         description='실패 메시지'
#                     ),
#                 },
#             ),
#         ),
#         401: openapi.Response(
#             description='이미 존재하는 파일',
#         ),
#         402: openapi.Response(
#             description='전송된 데이터가 CSV가 아님',
#         ),
#     },
# )
# )
@swagger_auto_schema(
    method='post',
    operation_summary='postCurrentData',
    operation_description='웨어러블 기기에서 저장된 데이터들 서버로 업로드',
    tags=['For User'],
    manual_parameters=
    [openapi.Parameter(
            name='csvfile',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description='전송될 워치 내의 데이터. csv 형식'
        ),
     openapi.Parameter(
            name='userID',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            required=True,
            description='사용자 ID (ex. AA00)'
        ),
     openapi.Parameter(
            name='battery',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_INTEGER,
            required=True,
            description='배터리 상태'
        ),
     openapi.Parameter(
            name='timestamp',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            required=True,
            description='데이터 생성 시간 (ex. 1672498800)'
        )
    ],
    responses={200: 'Success', 400: 'Fail', 401 : '이미 존재하는 파일', 402 : '전송된 데이터가 CSV가 아님', 403 : '잘못된 Parameters', 405 : '해당 user의 device id가 없음', 406 : 'DB 접속 오류'},
)

@api_view(['POST'])
@parser_classes([MultiPartParser])
@csrf_exempt
def postCurrentData(request):
    if request.method == 'POST':
        file_ = request.FILES['csvfile']
        data = request.POST
        print(data)
        userID = data.get('userID')
        battery = data.get('battery')
        timestamp = data.get('timestamp')
        if (file_ is None) or (userID is None) or (battery is None) or (timestamp is None):
            return HttpResponse('Input Error', status = 403)

        print(userID)
        
        localtime = time.localtime(int(timestamp))
        folder_name = time.strftime("%d_%m_%Y", localtime)
        print(folder_name)
        
        fs = FileSystemStorage(location='/home/wearables/gachon_test/' + userID + '/' + folder_name , base_url='/home/wearables/gachon_test/' + userID + '/' + folder_name)
        # fs = FileSystemStorage(location='/home/wearables/gachon_uploads/' + userID + '/' + timestamp, base_url='/home/wearables/gachon_uploads' + userID + '/' + timestamp)
        # if fs.exists:
        #     return HttpResponse('File already exists', status = 401)
        # else:
        #     filename = fs.save(file_.name, file_)           ## 파일 저장
            
        file_path = '/home/wearables/gachon_test/' + userID + '/' + folder_name + '/' + file_.name
        file_exists = os.path.isfile(file_path)
        print(file_path)
        if not file_exists:
            fs = FileSystemStorage(location='/home/wearables/gachon_test/' + userID + '/' + folder_name, base_url='/home/wearables/gachon_test/' + userID + '/' + folder_name)
            filename = fs.save(file_.name, file_)           ## 파일 저장
        else:
            return HttpResponse('File already exists', status = 401)
            
        
        db = MongoDB()
        try:
            if db._conn:
                devices_collection = db.get_collection('devices')
                users_collection = db.get_collection('users')
                
                try:
                    cursor = users_collection.find_one({'authCode' : userID})
                    deviceID = cursor['deviceID']
                    print(deviceID)
                except Exception as e:        ## deviceID가 없는 경우
                    return HttpResponse('No deviceId', status = 405)
                    
                gmt = pytz.timezone('Asia/Seoul')
                
                # timeToDatetime = datetime.datetime.fromtimestamp(timestamp)
                # last_battery_percent_date = str(timeToDatetime.day) + '_' + str(timeToDatetime.month) + '_' + str(timeToDatetime.year)
                
                print(localtime)
                last_battery_percent_ts_kst = datetime.datetime.fromtimestamp(int(timestamp))
                last_battery_percent_ts_gmt = datetime.datetime.utcfromtimestamp(int(timestamp))
                last_battery_percent_date = last_battery_percent_ts_kst.strftime('%d_%m_%Y')
  
                query = {"deviceID" : deviceID, 'battery' : battery, 'received_ts' : timestamp, 
                         'last_battery_percent_date' : last_battery_percent_date,
                         'last_battery_percent_ts_kst' : last_battery_percent_ts_kst,
                         'last_battery_percent_ts_gmt' : last_battery_percent_ts_gmt,
                         "date": datetime.datetime.now()}
                
                device_monitor_id = devices_collection.insert_one(query).inserted_id
                    
                print(device_monitor_id)
                
            else:
                return HttpResponse('DB 접속 오류', status = 406)        # Db 접속 오류
        except Exception as e:
            print(e)
            return HttpResponse('DB 접속 오류', status = 406)        # Db 접속 오류
                
        
        
        
        # if fs.exists(filename):
        #     return HttpResponse('File already exist', status = 401)
        # else :
        #     filename = fs.save(filename, file_)           ## 파일 저장
        #     uploaded_file_url = fs.url(filename)
        #     print(uploaded_file_url)
        
        #     dic_ = {}
        #     dic_['userID'] = userID
        #     dic_['battery'] = battery
        #     dic_['timestamp'] = timestamp
            
        #     with open('/home/wearables/gachon_test/' + userID + '/' + folder_name + '/' + timestamp + '.json', 'w') as f:
        #     # with open('/home/wearables/gachon_uploads/' + deviceID + '/' + folder_name + '/' + timestamp + '.json', 'w') as f:
        #         json.dump(dic_, f, ensure_ascii=False)
            
        #     print(dic_)        
            
            
        return HttpResponse(filename + ' successfully post', status = 200)    
              
    else:
       return HttpResponse('요청 오류', status = 400)        # 요청 오류
   

def policy_response(request):
    return render(request, 'SLBM_PP.html')



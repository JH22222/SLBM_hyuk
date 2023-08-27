from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import datetime
import pandas as pd
import pymongo
import os
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

@swagger_auto_schema(
    method='get',
    operation_summary='Get Battery Data',
    operation_description='최신 남은 배터리 용량(%) 상태',
    tags=['For Admin'], 
    manual_parameters=[experimentCode], 
    responses={200: 'Success', 400:'요청 오류', 401:'해당 User의 DeviceID 찾을 수 없음', 402 : 'DB 접속 오류'})
@api_view(['get'])
def getBatteryData_tmp(request):
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
                    projection_toFindDeviceID = {"_id" : 0, "battery" : 1, "last_battery_percent_ts_gmt" : 1}
                    # print(user)
                    record = devices_collection.find(query_toFindBatteryInfo, projection_toFindDeviceID).sort('last_battery_percent_ts_gmt', -1).limit(1)
                    # print(list(record))
                    result = {}
                    for doc in record:
                        result = {
                            'battery': doc.get('battery'),
                            'last_battery_percent_ts_gmt': doc.get('last_battery_percent_ts_gmt')
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
def getSleepRecord_tmp(request):
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
def getSurveyRecord_tmp(request):
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
                        data = {"hour" : sensor_data['date'].hour, "ppg_count" : sensor_data['ppg_count']}
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
    
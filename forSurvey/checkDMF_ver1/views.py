from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import datetime
import pandas as pd
import json
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

userID= openapi.Parameter('userID', openapi.IN_QUERY, description='사용자 ID (ex. AA00)', required=True, type=openapi.TYPE_STRING)
timestamp= openapi.Parameter('timestamp', openapi.IN_QUERY, description='날짜 (ex. 2023-01-01)', required=True, type=openapi.TYPE_STRING)


@swagger_auto_schema(
    method='get',
    operation_summary='Get Battery Data',
    operation_description='업로드된 배터리 데이터 중 가장 최신 데이터 반환',
    tags=['For Admin'], 
    manual_parameters=[userID], 
    responses={200: 'Success', 400:'요청 오류', 401:'해당 User 디렉토리 없음'})
@api_view(['get'])
def getBatteryData(request):
    if request.method == 'GET':
        data = request.GET
        userID = data.get('userID')
        
        print(userID)
        # userPath = os.path.join(UPLOAD_PATH, userID)
        userPath = os.path.join('/home/wearables/gachon_test/', userID)
        if not os.path.isdir(userPath):
            return JsonResponse({'erro' : 'No User directory'}, status = 401)    ## 디렉토리 없음
        
        folders = [folder for folder in os.listdir(userPath) if os.path.isdir(os.path.join(userPath, folder)) and folder.count('_') == 2]
        latest_folder = max(folders, key=lambda folder: datetime.datetime.strptime(folder, '%d_%m_%Y'))

        userLastPath = os.path.join(userPath, latest_folder)
        
        json_files = [file for file in os.listdir(userLastPath) if file.endswith('.json')]
        latest_json_file = max(json_files, key=lambda file: os.path.getmtime(os.path.join(userLastPath, file)))
        
        jsonPath = os.path.join(userLastPath, latest_json_file)
        
        with open(jsonPath, 'r') as f:
            lastBattery = json.load(f)
        
        print(lastBattery)
        
        return JsonResponse(lastBattery,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)

        
    else:
        return JsonResponse({'error' : '요청 오류'}, status = 400)

@swagger_auto_schema(
    method='get',
    operation_summary='Get Data Exist',
    operation_description='요청 날짜의 디렉토리 파일 리스트',
    tags=['For Admin'], 
    manual_parameters=[userID, timestamp], 
    responses={200: 'Success', 400:'요청 오류', 401:'해당 User 디렉토리 없음', 402 : '해당 날짜 디렉토리 없음'})
@api_view(['get'])
def getDataExist(request):
    if request.method == 'GET':
        data = request.GET
        userID = data.get('userID')     ## 우리가 아는 userid
        timestamp = data.get('timestamp')      ## 요청 timestamp yyyy-mm-dd
        
        userPath = os.path.join(UPLOAD_PATH, userID)
        # print(userPath)
        if not os.path.isdir(userPath):
            return JsonResponse({'erro' : 'No User directory'}, status = 401)    ## 디렉토리 없음
        
        try : 
            target_dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
        except Exception as e:
            return JsonResponse({'error' : 'timestamp form Error'}, status = 402)
        
        targetPath = os.path.join(userPath, str(target_dt.day if target_dt.day > 9 else '0' + str(target_dt.day)) + '_' + str(target_dt.month if target_dt.month > 9 else '0' + str(target_dt.month)) + '_' + str(target_dt.year))
        
        if not os.path.isdir(targetPath):
            return JsonResponse({'error' : 'No directory'}, status = 402)  ## 해당날짜 디렉토리 없음
        
        else:
            files = []
            files = os.listdir(targetPath)
            currentData = {'userID' : userID, 'timestamp' : timestamp, 'data' : files}
            
            
            return JsonResponse(currentData,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)

        
        
        
        
    else:
        return JsonResponse({'error' : '요청 오류'}, status = 400)
        
        
@swagger_auto_schema(
    method='get',
    operation_summary='Get Sleep Record',
    operation_description='요청 날짜의 수면 일지 기록',
    tags=['For Admin'], 
    manual_parameters=[userID, timestamp], 
    responses={200: 'Success', 400:'요청 오류', 401:'UserID 입력 오류', 402 : 'timestamp 양식 오류', 403 : '해당 날짜의 수면 일지 없음', 405 : 'DB 접속 오류'})
@api_view(['get'])
# Create your views here.
def getSleepRecord(request):
    if request.method == 'GET':
        data = request.GET
        userID = data.get('userID')     ## 우리가 아는 userid
        timestamp = data.get('timestamp')      ## 요청 timestamp yyyy-mm-dd
        try : 
            date_dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
        except Exception as e:
            return JsonResponse({'error' : 'timestamp form Error'}, status = 402)
        date_dt = date_dt.timestamp()
        date_dt_start = datetime.datetime.utcfromtimestamp(date_dt)
        date_dt_end = date_dt_start + datetime.timedelta(days=1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        
        print(date_dt_start)
        print(date_dt_end)
        
        
        db = MongoDB()
        try:
            if db._conn:
                polls_collection = db.get_collection('polls')
                users_collection = db.get_collection('users')
                isexist = users_collection.find_one({"authCodeLast4":userID})
                cursor = polls_collection.find({'$and' : [{'date':{'$gte':date_dt_start}}, {'date': {'$lte' : date_dt_end}}, {'userid' : userID}]})
                print(bool(isexist))
                if isexist:
                    print('Print ' + userID + ' Record....')
                else:
                    print('userID error')
                    return JsonResponse({'error': 'userID Error'}, status = 401)
                
                try : 
                    df = pd.DataFrame(list(cursor))
                    df['kr_date'] = df['date'] + datetime.timedelta(hours = 8)
                    df_handling = df
                    df_handling = df_handling.drop_duplicates(['tag','poll_key'])
                    df_handling = df_handling[df_handling.tag == '수면 일지']
                    df_handling = df_handling.reset_index(drop = True)
                    df_handling = df_handling[['tag', 'poll_key', 'poll', 'kr_date']]
                    
                except Exception as e:
                    return JsonResponse({'error' : 'Empty DB'}, status = 403)
                
                sleepRecord = df_handling.to_json(orient='records', force_ascii=False)
                sleepRecord = {userID : sleepRecord}
                
                print(sleepRecord)
                
                return JsonResponse(sleepRecord,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)

        except Exception as e:
            print('DB Error', str(e))
            return JsonResponse({'error' : 'DB 접속 오류'}, status = 405)        # Db 접속 오류
    else:
        return JsonResponse({'error' : '요청 오류'}, status = 400)
    
    return HttpResponse(200)

@swagger_auto_schema(
    method='get',
    operation_summary='Get Survey Record',
    operation_description='요청 주차의 설문 기록',
    tags=['For Admin'], 
    manual_parameters=[userID, timestamp], 
    responses={200: 'Success', 400:'요청 오류', 401:'UserID 입력 오류', 402 : 'timestamp 양식 오류', 403 : '해당 날짜의 수면 일지 없음', 405 : 'DB 접속 오류'})
@api_view(['get'])
def getSurveyRecord(request):
    if request.method == 'GET':
        data = request.GET
        userID = data.get('userID')     ## 우리가 아는 userid
        week = int(data.get('week'))                 ## 요청 주차
        db = MongoDB()
        try:
            if db._conn:
                users_collection = db.get_collection('users')
                
                user = users_collection.find_one({'authCode' : userID})
                if user:
                    print('Print ' + userID + ' Record....')
                else:
                    print('userID error')
                    return JsonResponse({'error': 'userID Error'}, status = 401)
        
        except Exception as e:
            print('DB Error', str(e))
            return JsonResponse({'error' : 'DB 접속 오류'}, status = 405)        # Db 접속 오류        

        
        try : 
            survey_dt = datetime.datetime.strptime(user['date'], '%Y%m%d')
            survey_dt_start = survey_dt + datetime.timedelta(days=((week*7)))
            survey_dt_end = survey_dt_start + datetime.timedelta(days=7)
        except Exception as e:
            return JsonResponse({'error' : 'timestamp form Error'}, status = 402)
        
        
        starttime = survey_dt_start
        survey_dt_start = survey_dt_start.timestamp()
        survey_dt_end = survey_dt_end.timestamp()
        
        survey_dt_start = datetime.datetime.utcfromtimestamp(survey_dt_start)
        print('Start DATE : ',survey_dt_start)
        survey_dt_end = datetime.datetime.utcfromtimestamp(survey_dt_end)
        print('End DATE : ',survey_dt_end)
        
        
        
        try:
            if db._conn:
                polls_collection = db.get_collection('polls')
                users_collection = db.get_collection('users')
                cursor = polls_collection.find({'$and' : [ {'userid' : userID}, {'date':{'$gte':survey_dt_start}}, {'date': {'$lte' : survey_dt_end}}]})
                
                
                try : 
                    df = pd.DataFrame(list(cursor))
                    df['kr_date'] = df['date'] + datetime.timedelta(hours = 8)
                    df_handling = df
                    df_handling = df_handling.drop_duplicates(['tag','poll_key'])
                    df_handling = df_handling[df_handling.tag != '수면 일지']
                    df_handling = df_handling.reset_index(drop = True)
                    df_handling = df_handling[['tag', 'poll_key', 'poll', 'kr_date']]
                except Exception as e:
                    return JsonResponse({'error' : 'Empty DB'}, status = 403)
                
                surveyRecord = df_handling.to_json(orient='records', force_ascii=False)

                surveyRecord = {'userID' : userID, 'week' : week, 'data' : surveyRecord}
                
                print(surveyRecord)
                
                return JsonResponse(surveyRecord,json_dumps_params={'ensure_ascii' : False}, safe = False, status = 200)

        except Exception as e:
            print('DB Error', str(e))
            return JsonResponse({'error' : 'DB 접속 오류'}, status = 405)        # Db 접속 오류
    else:
        return JsonResponse({'error' : '요청 오류'}, status = 400)
    
    return HttpResponse(200)

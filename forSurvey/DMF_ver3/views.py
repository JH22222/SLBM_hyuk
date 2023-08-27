from django.shortcuts import render
import csv
import json
import os
import pandas as pd
import pymongo

from django.views.decorators.csrf import csrf_exempt
from pandas.io.json import json_normalize
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from config.constants import (
	__UPLOADS__,
  __dbloc__
)
from db.db import MongoDB 
# Create your views here.

from django.shortcuts import render
from rest_framework.decorators import api_view #api
from rest_framework.response import Response #api

# Create your views here.


@csrf_exempt
def registUser(request):
    
    if request.method == 'GET':
        data = request.GET

        userID = data.get('userID')     ## 우리가 아는 userid
        duid = data.get('duid')             ## 난수값
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
                    
                    return HttpResponse(401)    # AuthCode 오류
            
            else:   
                return HttpResponse(402)        # db 접속 오류
                
        except Exception as e:
            print('DB Error', str(e))
            return HttpResponse(402)        # Db 접속 오류
    else:
        return HttpResponse(400)        # 요청 오류
        
        
    
    return HttpResponse(200)

@csrf_exempt
def postCurrentData(request):
    if request.method == 'POST':
        file_ = request.FILES['csvfile']
        data = request.POST
        
        deviceID = data.get('deviceID')
        battery = data.get('battery')
        timestamp = data.get('timestamp')  
        
        fs = FileSystemStorage(location='/home/wearables/gachon_test/' + deviceID + '/' + timestamp, base_url='/home/wearables/gachon_test/' + deviceID + '/' + timestamp)
        # fs = FileSystemStorage(location='/home/wearables/uploads/' + deviceID + '/' + timestamp, base_url='/home/wearables/uploads' + deviceID + '/' + timestamp)
        # if fs.exists:
        #     return HttpResponse('File already exists')
        # else:
        #     filename = fs.save(file_.name, file_)           ## 파일 저장
        filename = fs.save(file_.name, file_)           ## 파일 저장
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        
        dic_ = {}
        dic_['deviceID'] = deviceID
        dic_['battery'] = battery
        dic_['timestamp'] = timestamp
        
        with open('/home/wearables/gachon_test/' + deviceID + '/' + timestamp + '/' + timestamp + '.json', 'w') as f:
            json.dump(dic_, f, ensure_ascii=False)
        
        print(dic_)        
        
        return HttpResponse(200)
              
    else:
       return HttpResponse(400)

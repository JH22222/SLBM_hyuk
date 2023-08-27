import time
#import schedule
import datetime
from datetime import datetime
from datetime import timedelta
import pymongo
from pytz import timezone
import requests
import csv, json
import itertools
import pandas as pd
#import numpy as np
import requests
import glob
import sys
import os
import datetime
import shutil

checkDay = datetime.datetime.now() - timedelta(days=1)

def do_analysis(name):
    userId = name
    
    date = checkDay
    
    today = int(date.day)
    todayMonth = int(date.month)
    today = str(today) if int(today) >= 10 else '0' + str(today)
    todayMonth = str(todayMonth) if int(todayMonth) >= 10 else '0' + str(todayMonth)
    
    date = date - timedelta(days=1)
    yesterday = int(date.day)
    yesterdayMonth = int(date.month)
    yesterday = str(yesterday) if int(yesterday) >= 10 else '0' + str(yesterday)
    yesterdayMonth = str(yesterdayMonth) if int(yesterdayMonth) >= 10 else '0' + str(yesterdayMonth)
    
    
    ######## 파일 경로 설정 ########
    # uploads_path = r'/home/wearables/uploads/' + userId
    input_file = r'/home/wearables/uploads/' + userId + '/' + today + '_' + todayMonth + '_2023'
    yesterday_path = r'/home/wearables/uploads/' + userId + '/' + yesterday + '_' + yesterdayMonth + '_2023'
    
    # output_hrm_file = r'/home/hyuk/wearable/uploads_merge/' + userId + '/hrm_'+ today + '_' + todayMonth + '_2023.csv'
    # output_hrm_perMin_file = r'/home/hyuk/wearable/uploads_merge/' + userId + '/hrm_perMin'+ today + '_' + todayMonth + '_2023.csv'
    
    # INOUTFILE = r'toReport/' + today + '_' + todayMonth + '_2023/' + userId + '_' + today + '_' + todayMonth + '_2023.csv'
    
    
    ######## HR 데이터 병합 ########
    allFiles = glob.glob(input_file + '/hrm_*')
    yesterdayFiles = glob.glob(yesterday_path + 'hrm_*')
    allFiles = allFiles + yesterdayFiles
    
    if len(allFiles) > 0:
        frame = pd.DataFrame()
        # global list_
        list_ = []

        for file_ in allFiles:
            with open(file_) as f:
                file_size = os.path.getsize(file_)
                if file_size == 0:
                    continue
                hrv_raw = [x.split(',') for x in f.read().split('\\n')]
                for record in hrv_raw:
                    if len(record[0]) > 0 and len(record[0]) < 14:
                        if len(record) >= 3:
                            print(record)
                            record = record[:2]
                            print(record)
                        s = (int(record[0])+3600000)/1000.
                        s, ms = divmod(int(record[0])+3600000, 1000)
                        fullTime = '%s.%03d' % (time.strftime("%d_%m_%Y_%H:%M:%S", time.localtime(int(s))), ms)
                        date = '%s' % (time.strftime('%d_%m_%Y', time.gmtime(s))); hour = (int(fullTime[11:13])-1); day = fullTime[:2]
                        min = fullTime[14:16]; record.append(fullTime); record.append(hour); record.append(min); record.append(day)
            
                df_raw = pd.DataFrame(hrv_raw)
                df_raw.columns = ['timestamp', 'hrm', 'date', 'hour', 'min', 'day']
                df_raw.dropna(inplace=True)
                list_.append(df_raw)
                
    elif len(allFiles) == 0:
        return returnErrorResult(userId)
        
        
    
    if len(list_) != 0:  
        frame = pd.concat(list_)
        sort_by_date = frame.sort_values('timestamp')
    
    elif len(list_) == 0:
        return returnErrorResult(userId)
        
        
    ######## HR 데이터 Handling ########
    df = sort_by_date
    df = df.astype({'hrm' : 'float', 'hour' : 'int', 'min' : 'int', 'day' : 'int'})
    df_today = df[(df['day'] == int(today))]        ## 당일 데이터만 뽑기 

    ######## 분 단위로 쪼개기 ########
    df_forHrm_perMin = pd.DataFrame()

    for i in range(24):
        tmp = df_today[df_today['hour'] == i]
        if not tmp.empty :
            for j in range(60) : 
                tmp2 = tmp[tmp['min'] == j].sort_values(by='hrm', axis=0)
                if not tmp.empty :
                    df_forHrm_perMin = pd.concat([df_forHrm_perMin, tmp2.tail(n=1)], ignore_index=0)
    
    if not(df_forHrm_perMin.empty):
        df_forHrm_perMin = df_forHrm_perMin.sort_values(by='date', axis=0)          
    else :
        return returnErrorResult(userId)  
    
    ######## 미착용 시간 분석 1안 ########
    check_Nwearing_byHrm_list = []
    check_wearing_byHrm_list = []

    for i in range(24) :
        if not (df_forHrm_perMin['hour'] == i).any():
            check_Nwearing_byHrm_list.append((i+100))
            continue
        tmp = df_forHrm_perMin[df_forHrm_perMin['hour'] == i]
        count = 0
        for j in tmp.hrm:
            if j < 0:
                count += 1
            else :
                count = 0
        
        if count >= 30:
            check_Nwearing_byHrm_list.append(i)
        elif len(tmp) <= 30:
            check_Nwearing_byHrm_list.append(i)
        else : check_wearing_byHrm_list.append(i)
        
    ######## 미착용 시간 중절 ########
    toSeperate = check_Nwearing_byHrm_list
    tmp = toSeperate[0]
    Nwearing_sequence_byHrm = []
    count = 0
    location = 0
    for i in range(len(toSeperate)):
        if i == len(toSeperate)-1 :
            Nwearing_sequence_byHrm.append(toSeperate[location:])
        elif toSeperate[i] == toSeperate[i+1]-1:
            count += 1
        elif (toSeperate[i]+100) == (toSeperate[i+1]-1):
            count += 1
        elif toSeperate[i] == (toSeperate[i+1]-100-1):
            count += 1
        elif (toSeperate[i]-100) == (toSeperate[i+1]-1):
            count += 1
        else :
            Nwearing_sequence_byHrm.append(toSeperate[location:count+1])
            count = i+1; location = i+1

    ######## 수면 추청 시간 추출 ########
    compare = []

    for i in range(len(Nwearing_sequence_byHrm)):
        compare.append(len(Nwearing_sequence_byHrm[i]))


    compare
    suspected_sleep_hrs = []
    suspected_sleep_hrs = Nwearing_sequence_byHrm[compare.index(max(compare))]
    Nwearing_byHrm = Nwearing_sequence_byHrm
    Nwearing_byHrm.remove(suspected_sleep_hrs)
    
    
    ######## 착용 미착용 시간 비율 추출 ########

    if len(suspected_sleep_hrs) == 24 : 
        Nwearing_ratio_byHrm = 99999
        wearing_ratio_byHrm = 99999
    else:
        wearing_ratio_byHrm = len(check_wearing_byHrm_list)/(24-len(suspected_sleep_hrs))*100
        Nwearing_ratio_byHrm = (len(check_Nwearing_byHrm_list)-len(suspected_sleep_hrs))/(24-len(suspected_sleep_hrs))*100
    
    NwrStr = str("%0.2f"%float(Nwearing_ratio_byHrm))
    wrStr = str("%0.2f"%float(wearing_ratio_byHrm))
    
    ######## 결과값 내보내기 ########
    result_list = []
    result_list.append('2023_' + todayMonth + '_' + today)
    result_list.append(userId)
    result_list.append(suspected_sleep_hrs)
    result_list.append(Nwearing_byHrm)
    result_list.append(len(Nwearing_byHrm))
    result_list.append(check_wearing_byHrm_list)
    result_list.append(NwrStr)
    result_list.append(wrStr)
    df_result = pd.DataFrame([result_list])

    return df_result
                
 
def returnErrorResult(userID):
    result_list = []
    result_list.append('2023_' + str(checkDay.month) + '_' + str(checkDay.day))
    result_list.append(userID)
    result_list.append([100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123])
    result_list.append([])
    result_list.append(0)
    result_list.append([])
    result_list.append('99999')
    result_list.append('99999')
    result_list.append('##Empty Data')
    df_result = pd.DataFrame([result_list])

    return df_result

def getID():
    conn = pymongo.MongoClient('mongodb://admin1:slbm4321@localhost:27017/')
    db = conn.users
    user = db.users
    list_ = user.find({'$or' : [{'name':'asan_0626'}, {'name':'asan_0629'}, {'name':'asan_0705'}]})


    list_ = list(list_)
    userList = []
    for x in list_:
        userList.append(x['authCode'])
        
    return userList

if __name__ == '__main__':   
    
    userID_list =  getID()
    except_list = ['TT12']
    
    result = pd.DataFrame()
    for userId in userID_list :
        if userId in except_list:
            continue
        print('Doing ' + userId)
        tmp = do_analysis(userId)
        print(tmp)
        result = pd.concat([result, tmp], axis=0)
        print('Done ' + userId)

    if(len(result.count()) == 9):
        result.columns = ['date','userId', 'suspected-sleep-hrs', 'not-wearing-hrs-by-HR', 'no-of-not-wearing-chunks', 'wearing-hrs-by-HR', 'not-wearing-ratio-by-HR', 'wearing-ratio-by-HR', '']
    else:
        result.columns = ['date','userId', 'suspected-sleep-hrs', 'not-wearing-hrs-by-HR', 'no-of-not-wearing-chunks', 'wearing-hrs-by-HR', 'not-wearing-ratio-by-HR', 'wearing-ratio-by-HR']
    print(result.dtypes)
    result = result.astype({'not-wearing-ratio-by-HR': 'float64'})
    result = result.sort_values('not-wearing-ratio-by-HR', ascending=False)
    print(result.dtypes)
    result = result.reset_index(drop = True)
    result = result.drop([result.columns[0]], axis=1)
    result = result.fillna('')
    
    today = datetime.datetime.now()
    todayS = str(today.day) + '_' + str(today.month) + '_' + str(today.year)
    if not os.path.isdir('/home/hyuk/forRun/toReport/' + todayS):
        os.mkdir('/home/hyuk/forRun/toReport/' + todayS)
    result.to_csv('/home/hyuk/forRun/toReport/' + todayS + '/' + str(checkDay.day) + '_' + str(checkDay.month) + '_2023_dailyReport.csv')
    
    print(result)
    
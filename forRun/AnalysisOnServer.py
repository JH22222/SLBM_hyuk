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

hasEmpty = False

def do_analytics(name):
    userID = name
    print(userID)
    ######## 현재 날짜 얻기 ########
    #daytime_today = datetime.datetime.now()
      
    #today = int(daytime_today.day)-2
    #today = int(daytime_today.day) - int(daytime_today.timedelta(days=2, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0))
    #today = today if int(today) >= 10 else '0' + str(today) 
    #yesterday = int(today)-1
    #yesterday = int(daytime_today.day) - int(daytime_today.timedelta(days=3, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0))
    #yesterday = str(yesterday) if int(yesterday) >= 10 else '0' + str(yesterday)
    #today = str(today)

    #todayMonth = int(daytime_today.month) - int(daytime_today.timedelta(days=2, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0))
    #yesterdayMonth = int(daytime_today.month) - int(daytime_today.timedelta(days=3, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0))
    #todayMonth = str(todayMonth) if int(todayMonth) >= 10 else '0' + str(todayMonth)
    #yesterdayMonth = str(yesterdayMonth) if int(yesterdayMonth) >= 10 else '0' + str(yesterdayMonth)

    date = datetime.datetime.now()
    
    # tmp_time = timedelta(days= 1)
    # date = date - tmp_time
    
    date_alpha = timedelta(days=1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
    date_beta = timedelta(days=1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

    date = date - date_alpha
    today = int(date.day)
    print(today, '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    todayMonth = int(date.month)
    today = str(today) if int(today) >= 10 else '0' + str(today)
    todayMonth = str(todayMonth) if int(todayMonth) >= 10 else '0' + str(todayMonth)

    date = date - date_beta
    yesterday = int(date.day)
    yesterdayMonth = int(date.month)
    yesterday = str(yesterday) if int(yesterday) >= 10 else '0' + str(yesterday)
    yesterdayMonth = str(yesterdayMonth) if int(yesterdayMonth) >= 10 else '0' + str(yesterdayMonth)

    ######## 파일 경로 설정 ########
    #uploads_path = r'/home/hyuk/wearable/uploads/' + userID
    uploads_path = r'/home/wearables/uploads/' + userID
    #input_file = r'/home/hyuk/wearable/uploads/' + userID + '/' + today + '_' + todayMonth + '_2023'
    input_file = r'/home/wearables/uploads/' + userID + '/' + today + '_' + todayMonth + '_2023'
    #yesterday_path = r'/home/hyuk/wearable/uploads/' + userID + '/' + yesterday + '_' + yesterdayMonth + '01_2023'
    yesterday_path = r'/home/wearables/uploads/' + userID + '/' + yesterday + '_' + yesterdayMonth + '_2023'
    
    #output_ped_file = r'C:\Wearable\uploads_merge\ac13\ped_06_01_2023.csv'
    output_hrm_file = r'/home/hyuk/wearable/uploads_merge/' + userID + '/hrm_'+ today + '_' + todayMonth + '_2023.csv'
    

    #output_ped_perMin_file =r'C:\Wearable\uploads_merge\ac13\ped_perMin_06_01_2023.csv'
    output_hrm_perMin_file = r'/home/hyuk/wearable/uploads_merge/' + userID + '/hrm_perMin'+ today + '_' + todayMonth + '_2023.csv'
    if userID == 'VD':
        #uploads_path = r'/home/hyuk/wearable/uploads/' + userID
        uploads_path = r'/home/wearables/uploads/' + userID
        #input_file = r'/home/hyuk/wearable/uploads/' + userID + '/m/' + today + '_' + todayMonth + '_2023'
        input_file = r'/home/wearables/uploads/' + userID + '/m/' + today + '_' + todayMonth + '_2023'
        #yesterday_path = r'/home/hyuk/wearable/uploads/' + userID + '/m/' + yesterday + '_' + yesterdayMonth + '_2023'
        yesterday_path = r'/home/wearables/uploads/' + userID + '/m/' + yesterday + '_' + yesterdayMonth + '_2023'
   

    INOUTFILE = r'/home/hyuk/wearable/result/' + today + '_' + todayMonth + '_2023/' + userID + '_' + today + '_' + todayMonth + '_2023.csv'
    
    
    ######## 어제의 파일들 복사해오기 ########
    #userID_list = os.listdir('C:/Wearable/uploads')
    # hrm_files = glob.glob(yesterday_path + '/hrm_*')
    # hrm_files

    # for files_ in hrm_files :
    #     if (os.path.isdir(input_file) & os.path.isdir(yesterday_path)):       ## 어제와 오늘의 데이터 디렉토리가 존재할 경우
    #         shutil.copy2(files_, input_file + '/' + os.path.basename(files_))
    #     elif (not (os.path.isdir(input_file)) & (os.path.isdir(yesterday_path))):                                             ## 어제의 데이터 디렉토리만 존재할 경우
    #         os.mkdir(uploads_path + '/' + today + '_' + todayMonth + '_2023')                            ## 디렉토리 새로 생성
    #         shutil.copy2(files_, input_file + '/' + os.path.basename(files_))
    #     elif (not (os.path.isdir(input_file))) & (not(os.path.isdir(yesterday_path))):
    #         os.mkdir(uploads_path + '/' + yesterday  + '_' + yesterdayMonth + '_2023')
    #         os.mkdir(uploads_path + '/' + today + '_' + todayMonth + '_2023')
    #                                                                                      ## 오늘의 데이터 디렉토리만 존재할 경우 복사할 필요가 없음
    print(input_file)
    print(yesterday_path)
    
    ######## HR 데이터 병합 ########
    allFiles = glob.glob(input_file + '/hrm_*')
    yesterdayFiles = glob.glob(yesterday_path + 'hrm_*')
    allFiles = allFiles + yesterdayFiles

    if len(allFiles) > 0:
        frame = pd.DataFrame()
        global list_
        list_ = []

        for file_ in allFiles:
            with open(file_) as f:
                file_size = os.path.getsize(file_)
			    #print(file_size)
			    #print(type(file_size))
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
                        # print(record)
                        # print(fullTime)

                       
                            
                df_raw = pd.DataFrame(hrv_raw)
                df_raw.columns = ['timestamp', 'hrm', 'date', 'hour', 'min', 'day']
                df_raw.dropna(inplace=True)
                list_.append(df_raw)
                
                
    elif len(allFiles) == 0:
        result_list = []
        result_list.append('2023_' + todayMonth + '_' + today)
        result_list.append(userID)
        result_list.append([100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123])
        result_list.append([])
        result_list.append(0)
        result_list.append([])
        result_list.append('99999')
        result_list.append('99999')
        result_list.append('##Empty Data')
        df_result = pd.DataFrame([result_list])
        if not (os.path.isdir('/home/hyuk/wearable/result/' + today + '_' + todayMonth + '_2023')) :
            os.mkdir('/home/hyuk/wearable/result/' + today + '_' + todayMonth + '_2023')
        df_result.to_csv(INOUTFILE)
        print(userID + " Data is empty   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        hasEmpty = True
        return
    
    if len(list_) != 0:  
        frame = pd.concat(list_)
        sort_by_date = frame.sort_values('timestamp')
        sort_by_date.to_csv(output_hrm_file)
        sort_by_date
        #print("Hrm has been made!")
    elif len(list_) == 0:
        result_list = []
        result_list.append('2023_' + todayMonth + '_' + today)
        result_list.append(userID)
        result_list.append([100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123])
        result_list.append([])
        result_list.append(0)
        result_list.append([])
        result_list.append('99999')
        result_list.append('99999')
        result_list.append('##Empty Data')
        df_result = pd.DataFrame([result_list])
        if not (os.path.isdir('/home/hyuk/wearable/result/' + today + '_' + todayMonth + '_2023')) :
            os.mkdir('/home/hyuk/wearable/result/' + today + '_' + todayMonth + '_2023')
        df_result.to_csv(INOUTFILE)
        print(userID + " Data is empty   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        hasEmpty = True
        return
    
    
    ######## HR 데이터 Handling ########
    df = pd.read_csv(output_hrm_file)
    df['hrm'] = df['hrm'].replace('-', '0').astype(float)               ## hrm float 형변환 > 문자열 '-'는 파악 못함

    print(df)


    # df = df.astype({'hrm' : 'float', 'hour' : 'int', 'min' : 'int', 'day' : 'int'})
    df = df.astype({'hrm' : 'float', 'hour' : 'int', 'min' : 'int', 'day' : 'int'})
    
    
    ######## 당일 데이터만 뽑기 ########
    df_today = df[(df['day'] == int(today))]
    df_today
    
    
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
        result_list = []
        result_list.append('2023_' + todayMonth + '_' + today)
        result_list.append(userID)
        result_list.append([100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123])
        result_list.append([])
        result_list.append(0)
        result_list.append([])
        result_list.append('99999')
        result_list.append('99999')
        result_list.append('##Empty Data')
        df_result = pd.DataFrame([result_list])
        if not (os.path.isdir('/home/hyuk/wearable/result/' + today + '_' + todayMonth + '_2023')) :
            os.mkdir('/home/hyuk/wearable/result/' + today + '_' + todayMonth + '_2023')
        df_result.to_csv(INOUTFILE)
        print(userID + " Data is empty   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        hasEmpty = True
        return
    
    df_forHrm_perMin.to_csv(output_hrm_perMin_file)
       
    
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

    #print(check_wearing_byHrm_list)
    #print(check_Nwearing_byHrm_list)
    
    
    ######## 미착용 시간 분석 2안 ########
    '''check_Nwearing_byHrm_list = []
    check_wearing_byHrm_list = []

    count = 0

    for index, row in df_forHrm_perMin.iterrows() :
        hrm = int(row.hrm)
        hour = int(row.hour)
        if hrm < 0:
            count +=0
        else :
            count = 0
        
        if count >= 30:
            check_Nwearing_byHrm_list.append(hour)
        else :
            check_wearing_byHrm_list.append(hour)

    check_wearing_byHrm_list = list(dict.fromkeys(check_wearing_byHrm_list))
    check_Nwearing_byHrm_list = list(dict.fromkeys(check_Nwearing_byHrm_list))

    for i in range(24) : 
        if not ((i in check_wearing_byHrm_list) | (i in check_Nwearing_byHrm_list)):
            check_Nwearing_byHrm_list.append((i+100))

    check_wearing_byHrm_list.sort()
    check_Nwearing_byHrm_list.sort()

    print(check_wearing_byHrm_list)
    print(check_Nwearing_byHrm_list) '''
    
    
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
    #print(Nwearing_sequence_byHrm)
    
    
    ######## 수면 추청 시간 추출 ########
    compare = []
    #print(Nwearing_sequence_byHrm)
    for i in range(len(Nwearing_sequence_byHrm)):
        compare.append(len(Nwearing_sequence_byHrm[i]))
        #print(Nwearing_sequence_byHrm[i])

    compare
    suspected_sleep_hrs = []
    suspected_sleep_hrs = Nwearing_sequence_byHrm[compare.index(max(compare))]
    Nwearing_byHrm = Nwearing_sequence_byHrm
    Nwearing_byHrm.remove(suspected_sleep_hrs)
    
    
    ######## 착용 미착용 시간 비율 추출 ########
    print(len(check_Nwearing_byHrm_list)-len(suspected_sleep_hrs)) 
    print(len(check_wearing_byHrm_list))
    print(len(suspected_sleep_hrs))
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
    result_list.append(userID)
    result_list.append(suspected_sleep_hrs)
    result_list.append(Nwearing_byHrm)
    result_list.append(len(Nwearing_byHrm))
    result_list.append(check_wearing_byHrm_list)
    result_list.append(NwrStr)
    result_list.append(wrStr)
    df_result = pd.DataFrame([result_list])
    if not (os.path.isdir('/home/hyuk/wearable/result/' + today + '_' + todayMonth + '_2023')) :
        os.mkdir('/home/hyuk/wearable/result/' + today + '_' + todayMonth + '_2023')
    df_result.to_csv(INOUTFILE)
    print(userID + " Data has been Done")

def getID():
    ## conn = pymongo.MongoClient('mongodb://admin1:slbm4321@220.149.46.249:27017/')
    conn = pymongo.MongoClient('mongodb://admin1:slbm4321@localhost:27017/')
    db = conn.users
    user = db.users
    list_ = user.find({'$or' : [{'name':'asan_0626'}, {'name':'asan_0629'}, {'name':'asan_0705'}]})

    list_ = list(list_)
    userList = []
    for x in list_:
        print(x['authCode'])
        userList.append(x['authCode'])
        
    return userList

if __name__ == '__main__':   
    
    #userID_list = os.listdir('/home/hyuk/wearable/uploads')
    #currentDay = datetime.datetime.now()
    #currentDay = int(currentDay.day) - 2
    #currentDay = int(currentDay.day) - int(currentDay.timedelta(days=2, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0))
    #currentDay = str(currentDay) if int(currentDay) >= 10 else '0' + str(currentDay)       
    currentDay = datetime.datetime.now()
    currentDay_alpha = timedelta(days=1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

    currentDay = currentDay - currentDay_alpha
    current = int(currentDay.day)
    currentMonth = int(currentDay.month)
    current = str(current) if int(current) >= 10 else '0' + str(current)
    currentMonth = str(currentMonth) if int(currentMonth) >= 10 else '0' + str(currentMonth)


    
    #except_list = ['2ZEx', 'cnEf', 'zP3R', 'qUq8', 'UNKNOWN', 'ga64', 'kb24', 'tw68', 'sk43', 'ha19', 'kn13', 'be39', 'pm96', 'ua77', 'ea80', 'ac13', 'bp16', 'ya71', 'we59', 'sh29', 'km64', 'dw78', 'vs14', 'ub12', 'bm15', 'vh17', 'cs63', 'mk94', 'ry23', 'ch17', 'pb17', 'sb36', 'gm49', 'hp91', 'rb86', 'ph29', 'zk41', 'gb23', 'kz73', 'am77', 'ea15', 'uz94', 'gd81', 'ux88', 'ek17', 'hw52', 'dp81', 'tg53', 'ax22', 'gm34', 'ma85']
    # except_list = ['UNKNOWN', 'ga64', 'kb24', 'tw68', 'sk43', 'ha19', 'kn13', 'be39', 'pm96', 'ua77', 'ea80', 'ac13', 'bp16', 'ya71', 'we59', 'sh29', 'km64', 'dw78', 'vs14', 'ub12', 'bm15', 'vh17', 'cs63', 'mk94', 'ry23', 'ch17', 'pb17', 'sb36', 'gm49', 'hp91', 'rb86', 'ph29', 'zk41', 'gb23', 'kz73', 'am77', 'ea15', 'uz94', 'gd81', 'ux88', 'ek17', 'hw52', 'dp81', 'tg53', 'ax22', 'gm34', 'ma85']
    # userID_list = ['AS89', 'AS71']'
    userID_list =  getID()
    except_list = ['TT12']

    c = 0
    for userId in userID_list :
        if userId in except_list:
            continue
        do_analytics(userId)
        c += 1
        print(c)

    print('Total count : ' + str(c))

    #currentDay = datetime.datetime.now()
    #currentDay = str(currentDay) if int(currentDay.day) > 10 else '0' + str(currentDay.day)
    #currentDay = int(currentDay) -1 

    result_files = r'/home/hyuk/wearable/result/' + current + '_' + currentMonth+ '_2023'
    report_file = r'/home/hyuk/wearable/result/'+ current + '_' + currentMonth + '_2023_dailyReport.csv'

    allFiles = glob.glob(result_files+'/*.csv')
    allData = []

    for file_ in allFiles:
        df = pd.read_csv(file_)
        allData.append(df)


    
    result = pd.concat(allData, axis=0, ignore_index=True)
    print(result)
    print(len(result.count()))
    if(len(result.count()) == 10):
        result.columns = ['','date','userId', 'suspected-sleep-hrs', 'not-wearing-hrs-by-HR', 'no-of-not-wearing-chunks', 'wearing-hrs-by-HR', 'not-wearing-ratio-by-HR', 'wearing-ratio-by-HR', '']
    else:
        result.columns = ['', 'date','userId', 'suspected-sleep-hrs', 'not-wearing-hrs-by-HR', 'no-of-not-wearing-chunks', 'wearing-hrs-by-HR', 'not-wearing-ratio-by-HR', 'wearing-ratio-by-HR']
        
    result = result.sort_values('not-wearing-ratio-by-HR', ascending=False)
    print(result.dtypes)
    result = result.reset_index(drop = True)
    result = result.drop([result.columns[0]], axis=1)
    
    print(result)
    
    today = datetime.datetime.now()
    
    # tmp_time = timedelta(days=0)
    # today = today - tmp_time
    print(today, '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    
    alpha_time = datetime.timedelta(days = 1)
    yesterday = today - alpha_time
    todayS = str(today.day) + '_' + str(today.month) + '_' + str(today.year)
    yesterdayS = str(yesterday.day) + '_' + str(yesterday.month) + '_' + str(yesterday.year)
    
    # result.to_csv(report_file)
    if not os.path.isdir('toReport/' + todayS):
        os.mkdir('toReport/' + todayS)
    report_file = r'toReport/' + todayS + '/' + current + '_' + currentMonth + '_2023_dailyReport.csv'
    result.to_csv(report_file)
    print(report_file)
    print('Reports has been made!')

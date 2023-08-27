import pymongo
import pandas as pd
import datetime
import time
from datetime import timedelta
import os

def doCheck(userId):
    ## conn = pymongo.MongoClient('mongodb://admin1:slbm4321@220.149.46.249:27017/')
    conn = pymongo.MongoClient('mongodb://admin1:slbm4321@localhost:27017/')
    db = conn.users
    polls = db.polls
    user = db.users

    user_dic = user.find_one({'authCode': userId})
    userDate = user_dic['date']

    
    cursor = polls.find({'userid': userId})
    df = pd.DataFrame(list(cursor))
    
    start_date = datetime.datetime.strptime(userDate, "%Y%m%d")
    # if datetime.datetime.now().weekday() == 1:
    #     start_date = datetime.datetime.strptime("20230509", "%Y%m%d")
    today = datetime.datetime.now()
    diff = today - start_date
    week = int(int(diff.days)/7)
    print(week, '주차')
    alpha = timedelta(days = (week*7))
    beta = timedelta(days = (week*7)+7)
    set_time1 = start_date + alpha
    set_time2 = start_date + beta
    print(set_time1)
    print(set_time2)
    df_handling = pd.DataFrame()
    df_handling = df
    df_handling = df[df['date'].between(set_time1, set_time2)]
    # df_handling = df[df['date_local'].between(set_time1, set_time2)]
    
    
    df_handling = df_handling.drop_duplicates(['tag','poll_key'])
    df_handling = df_handling[df_handling.tag != '수면 일지']
    df_handling = df_handling.reset_index(drop = True)
    alpha = timedelta(hours = 8)
    df_handling['date_local'] = df_handling['date'] + alpha
    print(df_handling)

    
    # set_time1 = datetime.datetime(2023, 3, 15)
    # set_time2 = datetime.datetime(2023, 3, 17)
    #df_handling = pd.DataFrame()
    # for idx, row in df.iterrows():
    #     if
    # df_handling = df[df['date'].between(set_time1, set_time2)]
    df_handling = df_handling[['userid', 'tag', 'poll_key', 'poll']]

    # df_handling.to_excel('/home/hyuk/wearable/checkSurvey/' + str(week) + 'week_Survey_' + userId + '.xlsx')
    today = datetime.datetime.now()
    alpha_time = datetime.timedelta(days = 1)
    yesterday = today - alpha_time
    todayS = str(today.day) + '_' + str(today.month) + '_' + str(today.year)
    yesterdayS = str(yesterday.day) + '_' + str(yesterday.month) + '_' + str(yesterday.year)
    
    if not os.path.isdir('/home/hyuk/forRun/toReport/' + todayS):
        os.mkdir('/home/hyuk/forRun/toReport/' + todayS)
        
    # df_handling.to_excel('toReport/' + todayS + '/' + str(week) + 'week_Survey_' + userId + '.xlsx')
    df_handling.to_excel('/home/hyuk/forRun/toReport/' + todayS + '/' + str(week) + 'week_Survey_' + userId + '.xlsx')
    
def getID():
    ## conn = pymongo.MongoClient('mongodb://admin1:slbm4321@220.149.46.249:27017/')
    conn = pymongo.MongoClient('mongodb://admin1:slbm4321@localhost:27017/')
    db = conn.users
    user = db.users
    if datetime.datetime.now().weekday() == 2:                  ## 수요일
        # list_ = user.find({'$or' : [{'name':'asan_0614'}, {'name':'asan_0705'}]})
        list_ = user.find({'name':'asan_0705'}) 
    # elif datetime.datetime.now().weekday() == 1:                ## 화요일
    #     list_ = user.find({'name':'asan_0509'})         
    elif datetime.datetime.now().weekday() == 3:                 ## 목요일
        # list_ = user.find({'$or' : [{'name':'asan_0615'}, {'name':'asan_0629'}]})
        list_ = user.find({'name':'asan_0629'})   
    elif datetime.datetime.now().weekday() == 0:
        # list_ = user.find({'$or' : [{'name':'asan_0626'}, {'name':'asan_0703'}]})   ## 월요일
        list_ = user.find({'name':'asan_0626'})   ## 월요일
    list_ = list(list_)
    userList = []
    print(list_)
    for x in list_:
        print(x['authCode'])
        userList.append(x['authCode'])
    return userList

if __name__ == '__main__':
    userID = getID()
    print(userID)
    for x in userID:
        if x == 'test_J' or x == 'AS33' or x == 'TT12':
            continue
        print(x, ' check')
        doCheck(x)
        print(x, ' checked')
    
    print('@@@@@@@@@@ Clear @@@@@@@@@@')
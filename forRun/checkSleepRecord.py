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
    
    cursor = polls.find({'userid': userId})
    df = pd.DataFrame(list(cursor))
    
    today = datetime.datetime.now()
        
    alpha_time = timedelta(hours = 8)
    beta_time = timedelta(days = 1)
    
    df['kr_date'] = df['date'] + alpha_time

    today = datetime.datetime(today.year, today.month, today.day)
    tom = today + beta_time
    df_handling = pd.DataFrame()
    df_handling = df[df['kr_date'].between(today, tom)]
    df_handling = df_handling.drop_duplicates(['tag','poll_key'])
    df_handling = df_handling[df_handling.tag == '수면 일지']
    df_handling = df_handling.reset_index(drop = True)
    df_handling = df_handling[['userid', 'tag', 'poll_key', 'poll', 'kr_date']]
    print(df_handling)

    s = str(today.day) + '_' + str(today.month) + '_' + str(today.year) + '_' + userId + '_sleepRecord'
    
    today = datetime.datetime.now()
    alpha_time = datetime.timedelta(days = 1)
    yesterday = today - alpha_time
    todayS = str(today.day) + '_' + str(today.month) + '_' + str(today.year)
    yesterdayS = str(yesterday.day) + '_' + str(yesterday.month) + '_' + str(yesterday.year)

    # if not os.path.isdir('toReport/' + todayS):
    #     os.mkdir('toReport/' + todayS)
    if not os.path.isdir('/home/hyuk/forRun/toReport/' + todayS):
        os.mkdir('/home/hyuk/forRun/toReport/' + todayS)
    
    df_handling.to_excel('/home/hyuk/forRun/toReport/' + todayS + '/' + s + '.xlsx')
    # df_handling.to_excel('toReport/' + todayS + '/' + s + '.xlsx')


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
    userID = getID()
    for x in userID:
        if x == 'test_J' or x == 'AS33' or x == 'TT12':
            continue
        print(x, ' check')
        doCheck(x)
        print(x, ' checked')
    
    print('@@@@@@@@@@ Clear @@@@@@@@@@')

import pandas as pd
import os
import datetime
import glob
import pymongo

def doCheck(userID):
    userId = userID
    targetpath = r'/home/wearables/uploads/'+ userId + '/'
    checkT = False
    checkY = False
    
    today = datetime.datetime.now()
    
    alpha_time = datetime.timedelta(days = 1)
    yesterday = today - alpha_time
    print(today)
    print(yesterday)
    
    dic_list = os.listdir(targetpath)
    print(dic_list)
    
    todayS = str(today.day) + '_' + str(today.month) + '_' + str(today.year)
    yesterdayS = str(yesterday.day) + '_' + str(yesterday.month) + '_' + str(yesterday.year)
    print(todayS)
    
    for x in dic_list:
        if str(today.day) in x[:2] and str(today.month) in x[3:5] and str(today.year) in x[6:]:
            checkT = True
        if str(yesterday.day) in x[:2] and str(yesterday.month) in x[3:5] and str(yesterday.year) in x[6:]:
            checkY = True

    print(checkT, checkY)
    list_ = []
    list_.append(userId)
    list_.append('X' if not checkT else 'O')
    list_.append('X' if not checkY else 'O')
    print(list_)
    
    df = pd.DataFrame(data = [list_])
    return df

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
    allData = []
    
    today = datetime.datetime.now()
    
    
    alpha_time = datetime.timedelta(days = 1)
    yesterday = today - alpha_time
    todayS = str(today.day) + '_' + str(today.month) + '_' + str(today.year)
    yesterdayS = str(yesterday.day) + '_' + str(yesterday.month) + '_' + str(yesterday.year)
    
    for x in userID:
        if x == 'test_J' or x == 'AS33' or x == 'TT12':
            continue
        print(x, ' check')
        try:
            allData.append(doCheck(x))
        except:
            print('Error')
        print(x, ' checked')
    
    result = pd.concat(allData, axis = 0, ignore_index=True)
    result.columns = ['UserID', todayS, yesterdayS]
    result = result.reset_index(drop = True)
    print(result)
    
    if not os.path.isdir('/home/hyuk/forRun/toReport/' + todayS):
        os.mkdir('/home/hyuk/forRun/toReport/' + todayS)
    
    # result.to_excel('toReport/' + todayS + '/' + todayS +  '_todayDirectory.xlsx')
    result.to_excel('/home/hyuk/forRun/toReport/' + todayS + '/' + todayS +  '_todayDirectory.xlsx')
    print('@@@@@@@@@@ Clear @@@@@@@@@@')
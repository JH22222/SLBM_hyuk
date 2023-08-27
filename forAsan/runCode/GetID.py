import pymongo


def getID(date):
    conn = pymongo.MongoClient('mongodb://admin1:slbm4321@localhost/')
    db = conn.users
    user = db.users
    list_ = user.find({'date':date})
    list_ = list(list_)
    userList = []
    for x in list_:
        print(x['authCode'])
        userList.append(x['authCode'])
    return userList
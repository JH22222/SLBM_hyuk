from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import StreamingHttpResponse
import pandas as pd
import os
from django.conf import settings
from sqlalchemy import create_engine
from django.views.decorators.csrf import csrf_exempt
import sqlite3
from db.db import MongoDB
import datetime
import pprint, math, pymongo

db = MongoDB()
import json
## Test. isit Run?
"""
@csrf_exempt
def post_routes(request):
    # get the response from the URL
    params = json.loads(request.body)
    time = params['datetime'].split('T')[1].split(':')

    url = 'http://hci.unist.ac.kr/naver-api/route_search' \
          '?start={}' \
          '&end={}' \
          '&eventid={}' \
          '&datetime={} {}' \
          '&num_traj={}' \
          '&start_latlng={}' \
          '&end_latlng={}' \
        .format(float(params['start']),
                float(params['end']),
                int(params['eventId']),
                params['datetime'].split('T')[0],
                ':'.join(time[:-1]),
                int(params['num_traj']),
                params['start_latlng'],
                params['end_latlng'])
    print(params)
    response = requests.get(url)
    con = sqlite3.connect("./db.sqlite3")

    cur = con.cursor()
    sql = 'INSERT INTO snapshot values(?,?,?,?)'
    cur.execute(sql, [json.dumps(params), json.dumps(response.json()), params['session'],None])
    con.commit()

    # Be sure to close the connection
    con.close()
    return JsonResponse(response.json())

"""

@csrf_exempt
def post_polls(request):
    con = sqlite3.connect("./db.sqlite3")

    cur = con.cursor()
    sql = 'SELECT * from polls'
    query = cur.execute(sql)
    cols = [col[0] for col in query.description]
    df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    # Be sure to close the connection
    con.close()
    response = HttpResponse(content_type='text/csv')
    df.to_csv(path_or_buf=response, index=False)
    return response


@csrf_exempt
def load_user(request):
    data = json.loads(request.body.decode("utf-8"))

    if db._conn:
        print(data)
        polls = db.get_collection('polls')
        users = db.get_collection('users')
        polltypes = db.get_collection('polltypes')
        user = users.find_one({'authCode': data['authCode']})
        name = user['name']

        if user:
            week = datetime.datetime.strptime(user['date'], '%Y%m%d').date()
            # now = datetime.datetime.utcnow().date()
            now = datetime.datetime.now().date()
            # now = datetime.datetime.strptime('20230107', '%Y%m%d').date() 1
            delta = math.floor((now - week).days / 7)
            lastseen = polls.find_one({'userid': data['authCode']}, sort=[('date', pymongo.DESCENDING)])
            print('lastseen', lastseen)
            if lastseen != None:
                lastseen_week = lastseen['date'].date()
                lastseen_delta = math.floor((lastseen_week - week).days / 7)
                print(lastseen_delta, delta)
                
                if lastseen_delta == delta:
                    dataset = {'dataset': [{'type': 'form0', 'tag': '수면 일지'}], 'week': delta, 'name': 'knu_test'}
                else:
                    dataset = polltypes.find_one({'name': name, 'week': delta})
                    del dataset['_id']
            else:
                dataset = polltypes.find_one({'name': name, 'week': delta})
                print(dataset)
                del dataset['_id']

            for idx, item in enumerate(dataset['dataset']):
                path = os.path.join(settings.BASE_DIR, 'static/data/' + item['tag'] + '.txt')
                with open(path, 'r', encoding='utf8') as f:
                    item['data'] = [line.rstrip() for line in f.readlines()]

            # print({'data': {'week': delta, 'dataset': dataset, 'name': name}})
            return JsonResponse({'data': dataset})

        else:
            return JsonResponse({'data': None})


@csrf_exempt
def load_polls(request):
    # replace this later to csv file

    dataset = [{'type': 'form0', 'tag': '수면 일지'}]

    for idx, item in enumerate(dataset):
        path = os.path.join(settings.BASE_DIR, 'static/data/' + item['tag'] + '.txt')
        print(idx, item, path)
        with open(path, 'r', encoding='utf8') as f:
            item['data'] = [line.rstrip() for line in f.readlines()]
    # 1주 간격 FU: PHQ-9, GAD-7
    # 2주 간격 FU: ISI, 국민건강영양조사 스트레스척도

    return JsonResponse({'data': dataset})


@csrf_exempt
def submit_polls(request):
    # replace this later to csv file
    data = json.loads(request.body.decode("utf-8"))

    def update_date(item):
        # item['date'] = datetime.datetime.utcnow()
        item['date'] = datetime.datetime.now()
        return item

    dataset = [*map(update_date, data['polls'])]
    print('submit_polls', dataset)

    if db._conn:
        polls = db.get_collection('polls')
        polls.insert_many(dataset)
    else:
        print('error monggo', db)
        HttpResponse(500)

    return HttpResponse(200)

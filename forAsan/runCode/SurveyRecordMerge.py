import pymongo
import pandas as pd
import datetime
import os

def doSurveyRecord(userId, str_startDate):
    savePath = r'/home/hyuk/forAsan/'
    print(userId)
    startDate = datetime.datetime.strptime(str_startDate, "%Y%m%d")
    endDate = startDate + datetime.timedelta(weeks=8)
    alpha_time = datetime.timedelta(hours = 8)      ## gmt 변환용
    oneWeek = datetime.timedelta(weeks=1)
    date_diff = endDate - startDate
    print(date_diff)
    now = startDate
    print(now)
    
    conn = pymongo.MongoClient('mongodb://admin1:slbm4321@localhost:27017/')
    db = conn.users
    polls = db.polls
    users = db.users
    
    cursor = polls.find({'userid' : userId})
    df = pd.DataFrame(list(cursor))
    df = df.drop(df[df.tag == '수면 일지'].index)
    df = df.drop(['_id'], axis =1)
    df['date'] = df['date'] + alpha_time
    # print(df)
    
    df_list = []
    for x in range(int(date_diff.days/7)+1):
        tmp = df[df['date'].between(now, now + oneWeek)]
        tmp = tmp.drop_duplicates(['tag', 'poll_key'])
        df_list.append(tmp)
        now = now + oneWeek

    print(df_list)
    surveyPath = os.path.join(savePath, str_startDate + '_FinalRecord')
    tmp_day = startDate
    with pd.ExcelWriter(surveyPath + '/' + userId +'_SurveyRecord.xlsx') as writer:
        for i, x in enumerate(df_list):
            # if x.empty:
            #     tmp_day = tmp_day + datetime.timedelta(weeks=1)
            #     record_day = str(tmp_day.day) + '_' + str(tmp_day.month) + '_' + str(tmp_day.year)
            #     empty_df = pd.DataFrame() 
            #     empty_df.to_excel(writer, sheet_name=str(record_day))  
            # else:
            #     tmp_day = x.iloc[0]['date']
            #     record_day = str(tmp_day.day) + '_' + str(tmp_day.month) + '_' + str(tmp_day.year)
            #     x.to_excel(writer, sheet_name=str(record_day))
            try:
                tmp_day = x.iloc[0]['date']
                record_day = str(tmp_day.day) + '_' + str(tmp_day.month) + '_' + str(tmp_day.year)
                x.to_excel(writer, sheet_name=str(record_day))
            except Exception:
                tmp_day = tmp_day + datetime.timedelta(weeks=1)
                record_day = str(tmp_day.day) + '_' + str(tmp_day.month) + '_' + str(tmp_day.year)
                empty_df = pd.DataFrame() 
                empty_df.to_excel(writer, sheet_name=str(record_day))  
                
    tmp_day = startDate
    if len(df_list) < int(date_diff.days/7)+1:
    # with pd.ExcelWriter(surveyPath + '/' + userid + '_SleepRecord.xlsx') as writer:
        with pd.ExcelWriter(surveyPath + '/' + userId +'_SurveyRecord_empty.xlsx') as writer:
            for x in df_list:
                try :
                    tmp_day = x.iloc[0]['date']
                    record_day = str(tmp_day.day) + '_' + str(tmp_day.month) + '_' + str(tmp_day.year)
                    #x.to_excel(writer, sheet_name = str(record_day))
                except Exception:
                    tmp_day = tmp_day + datetime.timedelta(weeks=1)
                    record_day = str(tmp_day.day) + '_' + str(tmp_day.month) + '_' + str(tmp_day.year)
                    x = pd.DataFrame()
                    x.to_excel(writer, sheet_name = str(record_day))
    # empty_sheet_path = os.path.join(surveyPath, userId + '_SurveyRecord_empty.xlsx')
    # with pd.ExcelWriter(empty_sheet_path) as empty_writer:
    #     for i, x in enumerate(df_list):
    #         # if x.empty:
    #         #     record_day = str(tmp_day.day) + '_' + str(tmp_day.month) + '_' + str(tmp_day.year)
    #         #     empty_df = pd.DataFrame()  # 빈 데이터프레임 생성
    #         #     empty_df.to_excel(empty_writer, sheet_name=str(record_day))  # 빈 데이터프레임을 시트로 추가
    #         #     tmp_day = tmp_day + datetime.timedelta(weeks=1)
    #         try:
    #             tmp_day = x.iloc[0]['date']
    #             record_day = str(tmp_day.day) + '_' + str(tmp_day.month) + '_' + str(tmp_day.year)
    #             empty_df = pd.DataFrame()  # 빈 데이터프레임 생성
    #             empty_df.to_excel(empty_writer, sheet_name=str(record_day))  # 빈 데이터프레임을 시트로 추가
    #         except Exception:
    #             pass 

    # if not os.path.exists(surveyPath):
    #     os.makedirs(surveyPath)
    # # with pd.ExcelWriter(surveyPath + '/' + userid + '_SleepRecord.xlsx') as writer:
    # tmp_day = startDate
    # with pd.ExcelWriter(surveyPath + '/' + userId +'_SurveyRecord.xlsx') as writer:
    #     for x in df_list:     
    #         try :
    #             tmp_day = x.iloc[0]['date']
    #             record_day = str(tmp_day.day) + '_' + str(tmp_day.month) + '_' + str(tmp_day.year)
    #             x.to_excel(writer, sheet_name = str(record_day))
    #         except Exception :
    #             tmp_day = tmp_day + datetime.timedelta(weeks=1)
    #             record_day = str(tmp_day.day) + '_' + str(tmp_day.month) + '_' + str(tmp_day.year)
    #             x.to_excel(writer, sheet_name = str(record_day))

    # # with pd.ExcelWriter(surveyPath + '/' + userid + '_SleepRecord.xlsx') as writer:
    # tmp_day = startDate
    # with pd.ExcelWriter(surveyPath + '/' + userId +'_SurveyRecord_empty.xlsx') as writer:
    #     for x in df_list:
    #         try :
    #             tmp_day = x.iloc[0]['date']
    #             record_day = str(tmp_day.day) + '_' + str(tmp_day.month) + '_' + str(tmp_day.year)
    #             # x.to_excel(writer, sheet_name = str(record_day))
    #         except Exception:
    #             tmp_day = tmp_day + datetime.timedelta(weeks=1)
    #             record_day = str(tmp_day.day) + '_' + str(tmp_day.month) + '_' + str(tmp_day.year)
    #             x.to_excel(writer, sheet_name = str(record_day))
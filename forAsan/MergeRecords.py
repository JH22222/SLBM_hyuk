import os
import glob
import datetime
from runCode.GetID import getID
from runCode.SleepRecordMerge import doSleepRecord
from runCode.SurveyRecordMerge import doSurveyRecord

if __name__ == '__main__':
    
    str_startDate = '20230615'  ## startDate 변수 설정으로 해당 날짜 시작 피험자들 병합
    week = 8                ## 실험 진행한 주
    
    
    for user in getID(str_startDate):
        if user == 'qm82':
            continue
        print('@@@@@@@ do Sleep Record Merge @@@@@@@')
        doSleepRecord(user, str_startDate)
        print('@@@@@@@ do Survey Record Merge @@@@@@@')
        doSurveyRecord(user, str_startDate)

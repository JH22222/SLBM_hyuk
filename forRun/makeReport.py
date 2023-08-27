import os
import glob
import datetime

if __name__ == '__main__':
    # allFiles = glob.glob('*.py')
    # exec(open('AnalysisOnServer.py').read())
    # exec(open('checkSleepRecord.py').read())
    # exec(open('checkTodayDirectory.py').read())
    
    # if datetime.datetime.now().weekday() == 2:      ## 수요일
    #     exec(open('checkSurvey.py').read())
    # elif datetime.datetime.now().weekday() == 1:        ## 화요일
    #     exec(open('checkSurvey.py').read())
    # elif datetime.datetime.now().weekday() == 3:        ## 목요일
    #     exec(open('checkSurvey.py').read())
    # elif datetime.datetime.now().weekday() == 0:        ## 월요일
    #     exec(open('checkSurvey.py').read())
        
    current_dir = os.path.dirname(os.path.abspath(__file__))
    analysis_file = os.path.join(current_dir, 'AnalysisOnServer_New.py')
    exec(open(analysis_file).read())
    sleep_record_file = os.path.join(current_dir, 'checkSleepRecord.py')
    exec(open(sleep_record_file).read())
    today_directory_file = os.path.join(current_dir, 'checkTodayDirectory.py')
    exec(open(today_directory_file).read())
    survey_file = os.path.join(current_dir, 'checkSurvey.py')
    if datetime.datetime.now().weekday() == 2:      ## 수요일
        exec(open(survey_file).read())
    elif datetime.datetime.now().weekday() == 1:        ## 화요일
        exec(open(survey_file).read())
    elif datetime.datetime.now().weekday() == 3:        ## 목요일
        exec(open(survey_file).read())
    elif datetime.datetime.now().weekday() == 0:        ## 월요일
        exec(open(survey_file).read())
            
    
    
    print('@@@@@@@@@@ DONE @@@@@@@@@@')
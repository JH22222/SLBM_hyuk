# DMF_ver3

가천대 통신 서버

API 서버 환경 


Django(https://www.djangoproject.com/)

MongoDB(https://www.mongodb.com/ko-kr)


### standard start

```sh
python3 manage.py runserver 0.0.0.0:7778
```
** 웹서버 포트 변경시, 해당 명령어 뒤의 '7778' 부분을 변경하여 서버 시작하면 됨

### 주요 파일 설명
<details>
  <summary>DMF_ver3/DMF_ver3/</summary>


#### DMF_ver3/settings.py : 서버 주요 설정

``` python
    DEBUG = True                    ## 디버그 모드 설정

    ALLOW_HOSTS = ['*']             ## 외부 접속 허용 목록. '*'은 모든 외부접속 가능하도록 한다.

    INSTALLED_APPS = [              ## 의존성 주입. (사용되는 라이브러리)
        'django.contrib.admin',
            
            ...

        'forUser',              
        'forAdmin',
        'django_crontab',
    ]                           


    DATABASES = {                     ## DB 등록. MongoDB와의 연결은 pymongo를 사용하기 때문에, 설정하지 않았음.
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }                               

    TIME_ZONE = 'Asia/Seoul'           ## 서버 시간대 설정
    USE_I18N = True
    USE_L10N = True
    USE_TZ = False 

    CORS_ALLOW_METHODS = [              ## CORS 허용 설정
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS'
    ]
    CORS_ALLOW_HEADERS = [
        'Accept',
        'Accept-Encoding',
        'Authorization',
        'Content-Type',
        'Origin',
        'User-Agent'
    ]

    LOGGING = {                            ## 로그 기록. ./logs에 기록됨
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            
            ...

        },
        'handlers': {
            
            ...

        },
        'loggers': {
            
            ...

        }
    }
```

#### DMF_ver3/urls.py : 서버 End-Point 관리
``` python
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),         ## Swagger 선언
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),

    path('forUser/', include('forUser.urls')),          ## 사용자용App End-point
    path('forAdmin/', include('forAdmin.urls')),        ## 관리자용App End-point
``` 

#### DMF_ver3/asgi.py : 비동기 요청 처리 기능

#### DMF_ver3/wsgi.py : 동기 요청 처리 기능

</details>

<details>
  <summary>DMF_ver3/forAdmin/</summary>

#### forAdmin/admin.py : 사용되는 모델 등록

#### forAdmin/apps.py : 사용되는 내장 App 설정

#### forAdmin/models.py : 사용되는 모델 정의

#### forAdmin/runApp.py : 

#### forAdmin/test.py : 테스트 코드 작성

#### forAdmin/urls.py : URL 라우팅 정의, End-point 설정. 해당 주소의 요청이 들어왔을 시에 경로 설정

``` python
    path("getBatteryData/", views.getBatteryData),                  ## views.py에서 정의된 함수로 매핑됨
    path("getSurveyRecord/", views.getSurveyRecord),
    path("getSleepRecord/", views.getSleepRecord),
    path("getCnt_PPG/",views.getCnt_PPG)
``` 

#### forAdmin/views.py : 웹 요청의 동작 정의

``` python
    experimentCode= openapi.Parameter('experimentCode', openapi.IN_QUERY, description='실험 코드 (e.g., gc_test, knu_test)', required=True, type=openapi.TYPE_STRING)            ## swagger에서의 요청 파라미터 정의
    logger = logging.getLogger(__name__)                            ## 로그 기능 정의

    @swagger_auto_schema(                                           ## Swagger 문서 생성을 위한 데코레이터.
        ...
    )
    @api_view(['get'])                                              ## 해당 함수가 처리할 수 있는 HTTP 메서드 명시

    def getBatteryData(request):
        if GET 요청
            쿼리에서 실험코드를 받아옴

            users 콜렉션에서 해당 실험코드를 가진 유저의 deviceID 리스트를 가져옴

            deviceID 리스트를 가지고, device 콜렉션에서 deviceID로 등록된 배터리 값 중 가장 최신의 것들을 가져와 dictionary 형태로 패키징

            패키징된 데이터를 json 형태로 반환. Ascii 문자가 아닌 것들을 그대로 전송

    def getSleepRecord(request):
        if GET 쿼리 요청
            쿼리에서 실험코드를 받아옴

            users 콜렉션에서 해당 실험코드를 가진 유저의 userid 리스트를 가져옴

            polls 콜렉션에서 전날, 오늘 작성된 수면일지 존재를 확인해 O,X 형태로 dictionary로 패키징

            패키징된 데이터를 json 형태로 반환
    def getSurveyRecord(request):
        if GET 쿼리 요청
            쿼리에서 실험코드를 받아옴

            users 콜렉션에서 해당 실험코드를 가진 유저의 userid 리스트를 가져옴

            polls 콜렉션에서 각 주차별 작성된 수면일지 존재를 확인해 O,X 형태로 dictionary로 패키징

            패키징된 데이터를 json 형태로 반환

    def getCnt_PPG(request):
        if GET 쿼리 요청
            쿼리에서 실험코드를 받아옴

            users 콜렉션에서 해당 실험코드를 가진 유저의 userid 리스트를 가져옴

            sensor_data 콜렉션에서 금일 저장된 PPG의 신호 갯수를 시간대별로 패키징

            패키징된 데이터를 json 형태로 반환
```
</details>


<details>
  <summary>DMF_ver3/forUser/</summary>

#### forUser/views.py


``` python
    userID= openapi.Parameter('userID', openapi.IN_QUERY, description='사용자 ID (ex. AA00)', required=True, type=openapi.TYPE_STRING)
    deviceID= openapi.Parameter('deviceID', openapi.IN_QUERY, description='device ID(ex. randomValue123456789)', required=True, type=openapi.TYPE_STRING)
    regID= openapi.Parameter('regID', openapi.IN_QUERY, description='regID (ex. (ex. randomValue123456789))', required=True, type=openapi.TYPE_STRING)
    battery= openapi.Parameter('battery', openapi.IN_QUERY, description='배터리 상태', required=True, type=openapi.TYPE_INTEGER)
    timestamp= openapi.Parameter('timestamp', openapi.IN_QUERY, description='날짜 (ex. 2023-01-01)', required=True, type=openapi.TYPE_STRING)
    csvfile= openapi.Parameter('csvfile', openapi.IN_BODY, description='전송될 워치 내의 데이터. csv 형식', required=True, type=openapi.TYPE_FILE)

    def registUser(request):
        if GET 쿼리 요청
            쿼리에서 userid, deviceid, registID, timstamp 를 받아옴

            등록된 userid에서 deviceID와 registID를 쿼리로 받아온 값으로 업데이트함


    @swagger_auto_schema(
            ...
        manual_parameters=                          ## 요정 파라미터 정의
        [
            ...
        ],
            ...
    )

    @api_view(['POST'])
    @parser_classes([MultiPartParser])              ## 'multipart/form-data'로 요청해야함. body에 csv파일을 담아 보내야하기 때문
    @csrf_exempt                                    ##  Django의 CSRF 보호 메커니즘을 해당 뷰에 대해 비활성화
    def postCurrentData(request):
        if POST 쿼리 요청                            
            요청에서 csvfile, userid, battery, timestamp를 분리

            전송된 csvfile은 timestamp를 활용하여 gachon_test 디렉토리에 유저, 날짜별로 분리하여 저장

            전송된 배터리 정보를 device콜렉션에 deviceID를 활용하여 저장

    def policy_response(request):                    ## 개인정보처리방침 정적 페이지 반환
        return render(request, 'SLBM_PP.html')

```


</details>

#### DMF_ver3/logs/ : 서버 내에서의 로그 파일 저장
#### DMF_ver3/manage.py : 서버 실행 파일


# metnalapi_aio,  mentalSurvey_Knu
### Mental Survey 앱
--- 
API 서버 환경 
Django(https://www.djangoproject.com/)

아산병원 기본 포트: 8010 
/mentalapi

 프론트 환경
Vite(https://vitejs.dev/)

기본 포트: 8011
프록시: /mentalapi => localhost:8010

---

강원대 기본 포트: 5011 
/mentalapi

프론트 환경
Vite(https://vitejs.dev/)

기본 포트: 5010
프록시: /mentalapi => localhost:5011

---

<details>
  <summary> Unist Tutorial</summary>

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
pip install -r requirements.txt
npm install
```

### Compile and Hot-Reload for Development

```sh
python manage.py runserver 127.0.0.1:8000
vite
```

### Compile and Minify for Production

```sh
npm run build
```

</details>



<details>
  <summary> KNU Tutorial</summary>

## Project Setup

```sh
pip install -r requirements.txt
npm install
```

## Project Server Setting CheckList

```
mental/settings.py
    - ALLOWED_HOSTS : ['*']

package.json
    - scripts": {
            "dev": "vite --host 0.0.0.0 --port 8011",
        }

vite.config.js.json
    - server: {
            port: 8011,
            proxy: {'/mentalapi':'http://localhost:8010'}
        }
```
## Start Server
```sh
python manage.py runserver 0.0.0.0:8010
```
```sh
npm run dev
```

</details>

### 주요 파일 설명

#### mentalapi_aio/db/ : DB 접속 및 관련 함수 정의

<details>
    <summary> mentalapi_aio/mental/ : 설문 시스템 Back-End 설정 </summary>

- metnalapi_aio/mental/urls.py 

    ``` python
        urlpatterns = [                                             ## End-point 정의
        path("admin/", admin.site.urls),
        path("mentalapi/post_polls/", views.post_polls),
        path("mentalapi/load_polls/", views.load_polls),
        path("mentalapi/submit_polls/", views.submit_polls),
        path("mentalapi/load_user/", views.load_user)
        ]
    ```
 - mentalapi_aio/mental/views.py :
    ```python
        def post_polls(request):
            설문 등록
        
        def load_uesr(request):
            유저의 실험 코드에 따라 유저별 설문 일정 반환
        
        def load_polls(requset):
            유저의 설문 일정에 따라 해당 설문 data 반환
        
        def submit_polls(request):
            설문 등록
    ```
</details>


<details>
    <summary> mentalapi_aio/mental/ : 설문 시스템 Front-End 설정 </summary>

    - mentalapi_aio/src/componets/ : 설문 data들을 parsing 하는 컴포넌트들
        - PollItem0.vue : form0 형식 렌더링에 사용
        - PollItem1.vue : form1, form3 형식 렌더링에 사용
        - PollItem2.vue : form2 형식 렌더링에 사용
        - PollItem2_1.vue : form2 형식 렌더링에 사용
        - PollItem5.vue : form5 형식(추가설문) 렌더링에 사용


    - mentalapi_aio/src/Apps.vue : 설문 페이지 렌더링
        - form0 형식 : parser0 메소드 사용
        - form1 형식 : parser1 메소드 사용
        - form2 형식 : parser1 메소드 사용
        - form3 형식 : parser3 메소드 사용
        - form5 형식(추가설문) : parser5 메소드 사용

</details>

#### static\data : 설문 양식 저장
#### package.json : Front 서버 빌드 버전 정의
#### requirements.txt : 해당 서버 실행시 필요 라이브러리 정의
#### vite.config.js : 빌드도구 vite 설정 정의



# forCron
### 크론탭을 활용한 스크립트 자동 실행 파일들

<details>
    <summary>forCron/ppg_upload.py</summary>

```python
    def get_file_list2():
        유저별로 저장된 리스트에서 금일 날짜의 ppg 신호 파일들 목록 탐색
    
    def get_ppg_count2(user, filelist):
        오늘 0시 부터 매 1시간마다 ppg 신호 갯수를 체크하여 upload_DB2 메소드 실행
    
    def upload_DB2(user,count, date):
        get_ppg_count2에서 받은 정보들을 활용하여 정보들을 upsert함(존재하지 않으면 insert, 존재하면 update)
```

- crontab 환경은 아래와 같이 설정한다. (파일 이동시 경로설정 수정 요망. 절대 경로로 설정해야함)
```sh
    10 * * * * /usr/bin/python3 /home/hyuk/forSurvey/forCron/ppg_upload.py >> /home/hyuk/forSurvey/forCron/logs_ppg_upload/$(date +\%Y_\%m_\%d_\%H).log 2>&1
```

</details>

<details>
    <summary>forCron/reportAsan</summary>

### 전송자 변경시 smtp 연결 및 로그인 정보, 전송자 변경 필히 요망!!

```python
    def daily_report_send():
        수면일지 응답, 디렉토리 생성 여부, 데일리 리포트를 forRun/toReport 디렉토리에 해당 유저별로 존재하는 금일 리포트들을 모두 전송
    
    def survey_report_send():
        설문 응답 결과를 전송

```
- crontab 환경은 아래와 같이 설정한다. (파일 이동시 경로설정 수정 요망. 절대 경로로 설정해야함)
```sh
    59 11 * * * /usr/bin/python3 /home/hyuk/forSurvey/forCron/reportAsan.py >> /home/hyuk/forSurvey/forCron/logs_reportAsan/$(date +\%Y_\%m_\%d).log 2>&1
```


</details>

#### logs_ppg_uploads : ppg_upload 실행 로그 파일 목록
#### logs_reportAsan : reportAsan 실행 로그 파일 목록

# checkDMF_ver1
아산병원 임시 모니터링 시스템(Swagger 환경 )

API 서버 환경 


Django(https://www.djangoproject.com/)

MongoDB(https://www.mongodb.com/ko-kr)


### standard start

```sh
python3 manage.py runserver 0.0.0.0:8012
```
** 웹서버 포트 변경시, 해당 명령어 뒤의 '8012' 부분을 변경하여 서버 시작하면 됨

### 주요 파일 설명
<details>
    <summary>check/views.py : 웹 요청 처리</summary>

```python
        def getDataExist(request):
            if GET 쿼리 요청
                userid, timestamp, key 값 추출
                
                키값 확인 후 인증되면

                요청 날짜의 파일 리스트 반환
        
        def getSleepRecord(request):
            if GET 쿼리 요청
                userid, timestamp, key 값 추출

                키값 확인 후 인증되면

                요청 날짜의 수면일지 검색 후 json형태로 반환(변환 과정은 'forRun' 설명 참고)

        def getSurveyRecord(request):
            if GET 쿼리 요청
                userid, week, key 값 추출

                키값 확인 후 인증되면

                요청 주차의 설문 응답 기록 검색 후 json형태로 반환(변환 과정은 'forRun' 설명 참고) 

```
</details>

# forRun
데일리 리포트 추출 스크립트

### crontab 설정은 아래와 같이 한다.
```sh
    45 11 * * * /usr/bin/python3 /home/hyuk/forRun/makeReport.py >> /home/hyuk/forRun/logs/$(date +\%Y_\%m_\%d).log 2>&1
```

<details>
<summary>makeReport.py : 전체 실행 파일</summary>

```python
    current_dir = os.path.dirname(os.path.abspath(__file__))
    analysis_file = os.path.join(current_dir, 'AnalysisOnServer_New.py')
    exec(open(analysis_file).read())                ## 데일리 리포트 추출
    sleep_record_file = os.path.join(current_dir, 'checkSleepRecord.py')
    exec(open(sleep_record_file).read())            ## 수면일지 응답 결과 추출
    today_directory_file = os.path.join(current_dir, 'checkTodayDirectory.py')
    exec(open(today_directory_file).read())         ## 어제, 오늘 디렉토리 생성 여부 확인
    survey_file = os.path.join(current_dir, 'checkSurvey.py')
    if datetime.datetime.now().weekday() == 2:      ## 수요일
        exec(open(survey_file).read())              ## 설문 응답 결과 추출
    elif datetime.datetime.now().weekday() == 1:        ## 화요일
        exec(open(survey_file).read())
    elif datetime.datetime.now().weekday() == 3:        ## 목요일
        exec(open(survey_file).read())
    elif datetime.datetime.now().weekday() == 0:        ## 월요일
        exec(open(survey_file).read())
```
** 절대경로로 설정해야만 cron을 돌릴 수 있음

</details>

<details>
<summary>AnalysisOnServer_New.py : 데일리 리포트 추출</summary>

```python

    checkDay = datetime.datetime.now() - timedelta(days=1)              ## 검색 날짜 설정. 현재 코드는 1일 전 데이터로 추출

    def do_analysis(name):
        파라미터 name을 통해 userid를 받아옴.
        
        추출 기준 날짜를 checkDay(어제 날짜)로 설정.

        기준일에 맞춰 HR 데이터 병합, 당일 데이터 추출, 분단위로 분절, 미착용 시간 중절, 수면 추정 시간 추출, 미착용 시간 비율 추출 진행해 dataframe으로 반환

    def returnErrorResult(userID):
        데이터가 존재하지 않을 경우 처리

    
```
** 절대경로로 설정해야만 cron을 돌릴 수 있음

</details>

<details>
<summary>checkTodayDirectory.py : 데이터 업로드 확인용</summary>

```python
    
    def doCheck(userID):
        유저 아이디를 받아와 오늘(T day)와 어제(T-1 day) 데이터 디렉토리가 존재하는지(데이터가 업로드 되었는지)를 임시적으로 확인. 

```
** 절대경로로 설정해야만 cron을 돌릴 수 있음

</details>

<details>
<summary>checkSurvey.py : 설문 응답 추출</summary>

```python
    
    def doCheck(userId):
        유저 아이디를 받아와 이번주 설문 응답 기록 추출


```
** 절대경로로 설정해야만 cron을 돌릴 수 있음

</details>

<details>
<summary>checkSleepRecord.py : 수면일지 응답 추출</summary>

```python

    def doCheck(userId):
        유저 아이디를 받아와 금일 수면일지 응답 추출

    
```
** 절대경로로 설정해야만 cron을 돌릴 수 있음

</details>


# forAsan
실험 종료 후 설문, 수면일지 응답 기록 및 미응답 날짜 확인

#### MergeRecords.py : 실행 파일. 내부의 'str_startDate'를 원하는 실험 시작일로 설정하면 됨
#### MergeRecords/GetID.py : 해당 실험의 userid 가져오기
#### MergeRecords/SleepRecordMerge.py : 해당 실험의 수면일지 병합
#### MergeRecords/SurveyRecordMerge.py : 해당 실험의 설문 응답 병합
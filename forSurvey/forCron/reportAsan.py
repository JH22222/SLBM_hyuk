import smtplib
import os
import glob
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

today = datetime.datetime.now()
formatted_today = f"{today.day}_{today.month}_{today.year}"
directory_path = f"/home/hyuk/forRun/toReport/{formatted_today}"

def daily_report_send():
    # Gmail SMTP 서버 설정
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # 계정 정보 설정
    username = "jh.knu.slbm@gmail.com"
    password = "glgpmqyccqnuebwg"

    # 메일 작성
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "[디정플_아산] 피험자 데일리 리포트입니다."
    msg['From'] = username
    recipients = ["qkrgusrb0120@naver.com", "plzgiveme45@gmail.com"]
    msg['To'] = ", ".join(recipients)
    today = datetime.datetime.now().strftime("%m/%d")
    text = f"{today} 데일리 리포트 및 리포트 입니다.\n\n-이재혁 드림"

    # 메일 내용을 MIME 형식으로 변환
    part = MIMEText(text, 'plain')
    msg.attach(part)


    for file_path in glob.glob(os.path.join(directory_path, "*sleepRecord.xlsx")):
        print(file_path)
        part = MIMEBase('application', "octet-stream")
        with open(file_path, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))  # or use file_path if you want the full path
        msg.attach(part)
    print('sleepRecord clear')
    for file_path in glob.glob(os.path.join(directory_path, "*todayDirectory.xlsx")):
        print(file_path)
        part = MIMEBase('application', "octet-stream")
        with open(file_path, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))  # or use file_path if you want the full path
        msg.attach(part)
    print('todayDirectory clear')
    for file_path in glob.glob(os.path.join(directory_path, "*dailyReport.csv")):
        print(file_path)
        part = MIMEBase('application', "octet-stream")
        with open(file_path, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))  # or use file_path if you want the full path
        msg.attach(part)
    print('dailyReport clear')
    # SMTP 서버 연결 및 로그인
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(username, password)

    # 이메일 전송
    server.sendmail(username, recipients, msg.as_string())
    server.quit()

def survey_report_send():
    # Gmail SMTP 서버 설정
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # 계정 정보 설정
    username = "jh.knu.slbm@gmail.com"
    password = "glgpmqyccqnuebwg"

    # 메일 작성
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "[디정플_아산] 피험자 설문 응답 결과입니다."
    msg['From'] = username
    recipients = ["qkrgusrb0120@naver.com", "plzgiveme45@gmail.com"]
    msg['To'] = ", ".join(recipients)
    if datetime.datetime.now().weekday() == 0 :       ## 월요일
        text = "월요일 설문 응답 결과 입니다.\n\n-이재혁 드림"
    elif datetime.datetime.now().weekday() == 1 :     ## 화요일
        text = "화요일 설문 응답 결과 입니다.\n\n-이재혁 드림"
    elif datetime.datetime.now().weekday() == 2 :     ## 수요일
        text = "수요일 설문 응답 결과 입니다.\n\n-이재혁 드림"
    elif datetime.datetime.now().weekday() == 3 :     ## 목요일
        text = "목요일 설문 응답 결과 입니다.\n\n-이재혁 드림"
    elif datetime.datetime.now().weekday() == 4 :     ## 금요일
        text = "금요일 설문 응답 결과 입니다.\n\n-이재혁 드림"
    elif datetime.datetime.now().weekday() == 5 :     ## 토요일
        text = "토요일 설문 응답 결과 입니다.\n\n-이재혁 드림"
    elif datetime.datetime.now().weekday() == 6 :     ## 일요일
        text = "일요일 설문 응답 결과 입니다.\n\n-이재혁 드림"
    

    # 메일 내용을 MIME 형식으로 변환
    part = MIMEText(text, 'plain')
    msg.attach(part)
    
    for file_path in glob.glob(os.path.join(directory_path, "*_Survey_*.xlsx")):
        print(file_path)
        part = MIMEBase('application', "octet-stream")
        with open(file_path, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))  # or use file_path if you want the full path
        msg.attach(part)
    print('surveyReport clear')

    # SMTP 서버 연결 및 로그인
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(username, password)

    # 이메일 전송
    server.sendmail(username, recipients, msg.as_string())
    server.quit()

if __name__ == '__main__':
    daily_report_send()
    if glob.glob(os.path.join(directory_path, "*_Survey_*.xlsx")):
        survey_report_send()
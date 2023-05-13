FROM python:3

ADD ["OAuth.py", "config.py", "./"]

RUN pip install requests requests_oauthlib sqlalchemy pymysql

CMD ["python", "./OAuth.py"]
from flask import Flask
import requests
from bs4 import BeautifulSoup
from flask_apscheduler import APScheduler
import random
import re
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}
class Config(object):
    JOBS = [
        {  # 第二个任务，每隔5S执行一次
            'id': 'job',
            'func': '__main__:job',  # 方法名
            'args': None,  # 入参
            'trigger': 'interval',  # interval表示循环任务
            'seconds': 10,
        }
    ]

app = Flask(__name__)
app.config.from_object(Config())
ips = []

def job():
    global ips
    url = 'http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&groupid=0&qty=15&time=100&pro=&city=&port=1&format=txt&ss=3&css=&dt=1&specialTxt=3&specialJson=&usertype=15'
    res = requests.get(url).text
    ips = res.split('\n')




@app.route('/')
def hello_world():
    ip = random.choice(ips)
    return ip
if __name__ == '__main__':
    job()
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.debug = False
    app.run(port='8000')
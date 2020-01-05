import requests
import re
import json
import threading, time
import queue
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
            #'Cookie': 'acw_tc=2f61f26315750900938826012e49b45f9ce47364fc9bf77862e04ff71c407c; modeZoneSport1=0; _uab_collina=157537448769495687062867; Hm_lvt_63b82ac6d9948bad5e14b1398610939a=1575374493,1575374812,1575375492,1575376360; acw_sc__=5de6561907ffcca00e73e5d051a291c153da7029; SERVERID=1396f98518aedae1bcc35be51919a12c|1575376469|1575376409; Hm_lpvt_63b82ac6d9948bad5e14b1398610939a=1575376426'
        }
statue = []
q = queue.Queue()
def get_ip():
    url = 'http://127.0.0.1:8000'
    res = requests.get(url)
    print(res.text)
    return res.text

class SpiderThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.now_time = int(time.time())
    def run(self) -> None:
        global statue, q
        ip = get_ip()
        while not q.empty():
            id = q.get()
            url = 'https://live.leisu.com/detail-' + str(id)
            try:
                proxies = {'http': 'http://' + ip, 'https': 'https://' + ip}
                res = requests.get(url, headers=headers, proxies=proxies, timeout=2)
                res.encoding = 'utf-8'
                top_title = re.findall('<div class="top-title"><i class="radius"></i>(.*?)开赛', res.text)[0]
                y = top_title.split(' ')[3].split(':')
                x = top_title.split(' ')[1]
                old_h = int(y[0])
                old_m = int(y[1])
                score_1 = re.findall('<div class="score home">(.*?)</div>', res.text)[0]
                score_2 = re.findall('<div class="score away">(.*?)</div>', res.text)[0]
                score = str(score_1) + ':' + str(score_2)
                #半场进球比
                try:
                    half = re.findall('>HT：<span class="half-score">(.*?)</span', res.text)[0]
                except:
                    half = '0-0'
                rate_all = re.findall('<span class="all" data-num=".*?">(.*?)</span>', res.text)
                rate_one = re.findall('\(<span class="tnum">(.*?)</span>\)', res.text)
                rate = list(zip(rate_all, rate_one))
                teams = re.findall('<span class="display-i-b line-h-25">(.*?)</span>', res.text)
                team = teams[0] + 'VS' + teams[1]
                if url not in str(statue):
                    statue.append([url, team, score, rate, 0, x, old_h, old_m, half])
                else:
                    for i in statue:
                        index = statue.index(i)
                        if i[0] == url:
                            print(i[0])
                            old_score = statue[index][2].split(':')[0]
                            statue[index][3] = rate
                            statue[index][8] = half
                            statue[index][2] = score
                            print(statue[i])
                            #如果进球数大于1
                            t = int(score.split(':')[0]) - int(old_score)
                            if t >= 1:
                                #如果时间没超过10分钟
                                now = int(time.time())
                                if now - self.now_time >= 600:
                                    # 如果射门比大于2
                                    rate_one = list(rate_one)
                                    if int(rate_one[0]) == 0:
                                        rate_one[0] = 1
                                    if int(rate_one[1]) == 0:
                                        rate_one[1] = 1
                                    if int(rate_one[0])/int(rate_one[1]) >= 2:
                                        statue[statue.index(i)][4] += 1
                                        #更新时间
                                        self.now_time = now
                                        break
            except Exception as e:
                pass

def get_lives():
    url = 'https://live.leisu.com/'
    try:
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        THATDATA = re.findall('THATDATA=(.*?);', res.text)[1]
        js = json.loads(THATDATA)
        matchesTrans = js.get('matchesTrans')
        lives = matchesTrans.get('live')
        game_ids = []
        for i in lives:
            game_ids.append(i[0])
        return game_ids
    except Exception as e:
        print(e)


def get_statue():
    global q
    ids = get_lives()
    for i in ids:
        q.put(i)
    threads = []
    for i in range(8):
        th = SpiderThread()
        threads.append(th)
        th.start()
    for i in threads:
        i.join()
    return statue

if __name__ == '__main__':
    print(1)
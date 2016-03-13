import requests, threading, time, random, re, queue, os
from bs4 import BeautifulSoup

thread = input('Введите номер треда:\n')
import get_proxies
threads_num = 500
post_num = 25
lock = threading.Lock()
q = queue.Queue(); qg = queue.Queue()

r = requests.get('https://2ch.hk/b/index.json')
thread_list = [i['thread_num'] for i in r.json()['threads'] if int(i['posts_count']) > 100 and i['thread_num'] != thread]

def get_captcha(s):
  r = s.get('https://2ch.hk/makaba/captcha.fcgi', params={'type':'2chaptcha','board':'b'}, timeout=20)
  captcha_id = r.content[6:].decode('utf-8')
  r = s.get('https://2ch.hk/makaba/captcha.fcgi', params={'type':'2chaptcha','action':'image','id':'%s' %(captcha_id)}, timeout=20)
  with open('captcha.png', 'wb') as f: f.write(r.content)
  os.system('start captcha.png')
  captcha = input("Введите капчу:\n")
  os.system('taskkill /im dllhost.exe')
  return captcha,captcha_id

def req(q, thread):
  while not q.empty():
    try:
      s = requests.Session()
      s.proxies = q.get()
      posts_thread = random.choice(thread_list)
      """
      r = s.get('https://2ch.hk/makaba/captcha.fcgi', params={'type':'2chaptcha','action':'thread'}, timeout=20)
      if r.text.find('CHECK') != -1:
        with lock: captcha,captcha_id = get_captcha(s)
        payload = {
          'task': ('', 'post'),
          'board': ('', 'b'),
          'thread': ('', thread),
          'email': ('', 'sage'),
          'captcha_type': ('', '2chaptcha'),
          'comment': ('', 'bump'),
          'sage': ('', 'on'),
          '2chaptcha_id': ('', captcha_id),
          '2chaptcha_value': ('', captcha)
          }
        r = s.post('https://2ch.hk/makaba/posting.fcgi',
                        files=payload, params={'json':'1'},
                        proxies=proxy,
                        timeout=20)
        if r.json()['Error'] == None: print('Сообщение успешно отправлено с прокси: ' + str(proxy))
        else: print(r.json()); continue
        time.sleep(random.randint(17,19))
        """
      for i in range(post_num):
        try:
          r = s.get('https://2ch.hk/b/res/%s.json' %(thread), timeout=20)
          if int(r.json()['posts_count']) >= 500 and threading.active_count() > 25: print('Постов больше 500'); os._exit(1)
          r = s.get('https://2ch.hk/b/res/%s.json' %(posts_thread), timeout=20)
        except Exception: continue
        posts = [i['comment'].replace('<br>', '\n').replace('</br>', '\n').replace(' (OP)', '') for i in r.json()['threads'][0]['posts']]
        posts = [BeautifulSoup(i, "html.parser").text for i in posts]
        posts = list(filter(None, posts)); posts = list(filter(lambda x: not re.findall(r'^>>\d+\n$',x),posts))
        posts = list(set(posts[1:]))
        payload = {
          'task': ('', 'post'),
          'board': ('', 'b'),
          'thread': ('', thread),
          'email': ('',  random.choice(['','sage'])),
          'comment': ('', random.choice(posts[1:])),
          'sage': ('', 'on'),
          'captcha_type': ('', '2chaptcha')
          }
        try: r = s.post('https://2ch.hk/makaba/posting.fcgi',
                          files=payload, params={'json':'1'},
                          timeout=20)
        except Exception: continue
        if r.json()['Error'] == None: qg.put(proxy)
        elif r.json()['Error'] == -3 or r.status_code == 404: print('Тред удален'); os._exit(1)
        else: print('%s: %s' %(r.json(), proxy)); break
        print('Сообщение успешно отправлено с прокси: ' + str(proxy))
        time.sleep(random.randint(17,19))
    except Exception: continue
    finally:
      q.task_done()
      print('Кол-во прокси в очереди: %s; Кол-во потоков: %s' %(q.qsize(), threading.active_count()))
      
for proxy in get_proxies.proxy_lst:
  q.put({'https': 'http://' + proxy})
  
for thr in range(threads_num):
  thr = threading.Thread(target=req, args=(q,thread))
  thr.start()

q.join()

good_proxies = list(set(map(str,qg.queue)))
good_proxies = [re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', i)[0] for i in good_proxies]
with open('good_proxies.txt', 'w') as f: f.write('\n'.join(good_proxies))

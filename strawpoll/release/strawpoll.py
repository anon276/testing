import requests, get_proxies, threading, queue

q = queue.Queue()
threads_num = 100
payload = {"pollId":6970091,"votes":[17]}

def poll(q):
  while not q.empty():
    proxy = q.get()
    try:
      r = requests.post('https://strawpoll.me/api/v2/votes', json=payload, timeout=20, proxies=proxy)
      print(r.json())
    except Exception: continue
    finally:
      q.task_done()
      print('Кол-во прокси в очереди: %s; Кол-во потоков: %s' %(q.qsize(), threading.active_count()))

for proxy in get_proxies.proxy_lst:
  q.put({'https': 'http://' + proxy})
  
for thr in range(threads_num):
  thr = threading.Thread(target=poll, args=(q,))
  thr.start()

q.join()

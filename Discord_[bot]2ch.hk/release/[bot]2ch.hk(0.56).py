import discord, requests, re, time, threading, random, logging, logging.handlers, sys, os
from bs4 import BeautifulSoup
from datetime import timezone, datetime, timedelta

logger=logging.getLogger()
logger.setLevel(logging.INFO)
fh = logging.handlers.RotatingFileHandler('[bot]2ch.hk.log', 'a', 100000, 1, encoding='utf-8')
fh.setFormatter(logging.Formatter('%(asctime)s %(message)s', '[%d.%m.%Y %X]'))
logger.addHandler(fh)

client = discord.Client()
client.login('<username>', '<password>')
ACL=('Jürgen','Бесогон', 'testing', 'Lance Vance')

anek_total = requests.get('https://api.vk.com/method/wall.get?owner_id=-45491419&count=1&filter=owner')
img_total = requests.get('https://api.vk.com/method/wall.get?owner_id=-22751485&count=1&filter=owner')
logger.info('Анекдотов всего: {}'.format(anek_total.json()["response"][0]-1))
logger.info('Картинок всего: {}'.format(img_total.json()["response"][0]-1))

hashes_acl = ('linux', 'игра бесконечное лето', 'что? где? когда?', 'hubble space images')

def get_anon_fm():
  r = requests.get('http://anon.fm:8000/')
  r2 = requests.get('http://anon.fm/shed.js')

  shed_lst = [i.split(',') for i in r2.text.strip('[]').replace('"','').split('],[')]
  shed_lst_frmtd = [[str(datetime.fromtimestamp(int(j)).strftime('%Y.%m.%d %H:%M:%S')) \
                     if i.index(j)<=1 else j for j in i if i.index(j) != 2] for i in shed_lst if \
                    datetime.now() <= datetime.fromtimestamp(int(i[1])) <= datetime.now() + timedelta(days=10)]

  result = '**Сейчас в эфире**: %s\nСлушателей: %s\n\n**Анонс:**\n' %(re.findall(r'<td class="streamdata">(.+)</td>',r.text)[7].encode('iso-8859-1').decode(), re.findall(r'<td class="streamdata">(.+)</td>',r.text)[5]) + ''.join(['Название программы: %s\nВремя начала: %s\nВремя окончания: %s\n\n' %(i[2],i[0],i[1]) for i in shed_lst_frmtd]) + '**Ссылка на трансляцию**: http://anon.fm/'
  return result

def get_img_hash(req_str):
  imgs_lst = []
  for i in range(0,1000,100):
    r = requests.get('https://api.datamarket.azure.com/Bing/Search/v1/Image', params={'Query':"'%s'" %(req_str), 'Adult':"'Strict'", 'Options':"'DisableLocationDetection'", '$skip':i}, auth=requests.auth.HTTPBasicAuth('iy9YcyZ5zek6sJBI1/zn+bzUVTBlP1hT5KO/P+fq62g', 'iy9YcyZ5zek6sJBI1/zn+bzUVTBlP1hT5KO/P+fq62g'))
    soup = BeautifulSoup(r.content, "html.parser")
    imgs_lst += [i.text for i in soup.findAll('d:mediaurl')]
  return imgs_lst

def get_img():
  with requests.Session() as s:  
    while True:
      try: r = s.get('https://api.vk.com/method/wall.get?owner_id=-22751485&offset=%s&count=1&filter=owner' %(random.randint(0,img_total.json()["response"][0]-2)), timeout=5)
      except: continue
      for i in ['src_xxbig','src_xbig','src_big']:
        try:
          img_url=r.json()['response'][1]['attachment']['photo'][i]
          if '.jpg' in img_url:
            img = s.get(img_url).content
            return img
        except: pass
      
def get_anek():
  while True:
    try:
      with requests.Session() as s:
        r = s.get('https://api.vk.com/method/wall.get?owner_id=-45491419&offset=%s&count=1&filter=owner' %(random.randint(1,anek_total.json()["response"][0]-1)), timeout=1)
    except Exception: continue
    anek = r.json()["response"][1]['text'].replace('<br>','\n').strip()
    if len(anek) == 0: continue
    return anek
  
def cli_progress(val, end_val, thread, msg_chan, bar_length=20):
  percent = val / end_val
  hashes = '■' * int(round(percent * bar_length))
  spaces = '□' * (bar_length - len(hashes))
  client.send_message(msg_chan, "**Авто-бамп** - процент выполнения: [{0}] {1}%\nТред в работе: https://2ch.hk/b/res/{2}.html".format(hashes + spaces, int(round(percent * 100)), thread))

def get_last_bump(num):
  msg = "%s" % ("—"*31)
  with requests.Session() as s:
    r = s.get('https://2ch.hk/b/catalog.json')
    for i in range(int(num)):
      msg += '\n%s\n\nСсылка на треад: https://2ch.hk/b/res/%s.html\n%s' % (BeautifulSoup(re.sub(r'<br>', r'\n', r.json()['threads'][i]['comment']), "html.parser").text[:436]+'...', r.json()['threads'][i]['num'], ("—"*31))
    return msg

def get_top(num):
  msg = "%s" % ("—"*31)
  with requests.Session() as s:
    r = s.get('https://2ch.hk/b/threads.json')
    sorted_list = sorted(r.json()['threads'], key=lambda k: k['score'])
    for i in range(-1, -(int(num)+1), -1):
      msg += '\n%s\n\nСсылка на треад: https://2ch.hk/b/res/%s.html\nБаллы треада: %s\n%s' % (BeautifulSoup(sorted_list[i]['subject'], "html.parser").text, sorted_list[i]['num'], round(sorted_list[i]['score']), "—"*31)
    return msg

def auto_bump(thread, msg_chan, num, text, stop):
  with requests.Session() as s:
    if text in hashes_acl:
      imgs_lst = get_img_hash(text)
    for i in range(int(num)):
      if i % 10 == 0 and i != 0: cli_progress(i, num, thread, msg_chan)
      if stop.is_set(): client.send_message(msg_chan, '**Авто-бамп** завершил работу по команде \'stop\''); return
      if text == '1': r = s.post('https://2ch.hk/makaba/posting.fcgi', files=payload_template('b',str(thread),'бамп'))
      elif text in hashes_acl:
        while True:
          img_url = random.choice(imgs_lst)
          try: img = s.get(img_url).content
          except Exception: continue
          print(img_url, len(img))
          if 10*1000 <= len(img) <= 2*1000*1000 and str(img)[:4] == r"b'\x": break
        r = s.post('https://2ch.hk/makaba/posting.fcgi', files=payload_template('b',str(thread),image=(img)))
      else: r = s.post('https://2ch.hk/makaba/posting.fcgi', files=payload_template('b',str(thread),image=(get_img())))
      try:
        if r.json()['Status'] == 'OK':
          pass
      except:
        client.send_message(msg_chan, '**Авто-бамп** завершил работу c **Ошибкой!**: ' + str(r.json()['Reason']))
        return
      time.sleep(random.randint(19,25))
    client.send_message(msg_chan, "**Авто-бамп** завершил работу для треда: https://2ch.hk/b/res/%s.html. Можете запускать новый цикл." % (thread))

def payload_template(board,thread,comment='',captcha_type='',chaptcha_id='',chaptcha_value='',**kwargs):
  try:
    if kwargs['image']: image = kwargs['image']
  except Exception: image = ('','')
  payload = {
    'json':('','1'),
    'task':('','post'),
    'board':('',board),
    'thread':('',thread),
    'captcha_type':('',captcha_type),
    'email':('',''),
    'name':('',''),
    'subject':('',''),
    'comment':('',comment),
    '2chaptcha_id':('',chaptcha_id),
    '2chaptcha_value':('',chaptcha_value),        
    'image':image
    }
  return payload

def get_news(news_num):
  projects = []
  msg = "%s" % ("—"*31)
  r = requests.get('https://2ch.hk/news/')
  soup = BeautifulSoup(r.content, "html.parser")
  opposts = soup.find_all('div', {"class": "post oppost"})
  
  for oppost in opposts[:news_num]:
    try:
      post_title = re.sub(r"\n","",str(oppost.find('span', {"class": "post-title"}).get_text()))
    except:
      pass
    post_message = re.sub(r"\n","",str(oppost.find('blockquote', {"class": "post-message"}).get_text(' '))[:436])
    reflink = str(oppost.find('span', {"class": "reflink"}).a.get("href"))
    msg += "\n%s\n\n%s...\n\nСсылка на новость: https://2ch.hk%s\n%s" % (post_title, post_message, reflink,"—"*31)
  return msg
  
@client.event
def on_message(message):
  global te,t
  if message.author == client.user or not message.content.startswith('!'):
    return
  else:
    logger.info(message.author.name + ': ' + message.content)
  if message.content.startswith('!news'):
    try:
      news_num=int(str(message.content).split()[1])
      if 1 <= news_num <= 3:
        client.send_message(message.channel, get_news(news_num))
      else:
        raise ValueError
    except:
      client.send_message(message.channel, "**Ошибка!** Правильный формат: !news <num>. <num> может быть от 1 до 3")

  elif message.content.startswith('!bump'):
    try:
      if message.content == '!bump stop':
        if str(message.author) in ACL:
          te.set(); return
        else: client.send_message(message.channel, "**Ошибка!** У вас нет прав на эту команду."); return
    except: pass

    try:
      auto_bump_args=message.content.split(maxsplit=1)[1]
      auto_bump_args_list=auto_bump_args.split(',')
    except:
      client.send_message(message.channel, "**Ошибка!** Правильный формат: !bump <thread num>,<bumps num>")
      return
    try:
      if t.isAlive():
        client.send_message(message.channel, "**Ошибка!** Авто-бамп уже запущен. Ждите своей очереди.")
        return
      else: raise Exception
    except Exception:
      try:
        text = auto_bump_args_list[2].lower()
      except Exception: text = 0
      try:
        if 1 <= int(auto_bump_args_list[1]) <= 300 and len(auto_bump_args_list[0]) == 9 and auto_bump_args_list[0].isdigit():
          te = threading.Event()
          t = threading.Thread(target=auto_bump, args=(int(auto_bump_args_list[0]), message.channel, int(auto_bump_args_list[1]), text, te))
          t.start()
          client.send_message(message.channel, "**Авто-бамп** запущен для треда: https://2ch.hk/b/res/%s.html. Кол-во бампов: %s" % (str(auto_bump_args_list[0]),str(auto_bump_args_list[1])))
        else: raise Exception
      except Exception: client.send_message(message.channel, "**Ошибка!** Введено кол-во бампов отличное от 1-300! Либо номер треда указан неверно.")

  elif message.content.startswith('!top'):
    try:
      num=int(str(message.content).split()[1])
      if not 1 <= int(num) <= 5:
        raise ValueError
    except:
      client.send_message(message.channel, "**Ошибка!** Правильный формат: !top <num>. <num> может быть от 1 до 5")
      return
    else:
      client.send_message(message.channel, get_top(num))

  elif message.content.startswith('!lastb'):
    try:
      num=int(str(message.content).split()[1])
      if not 1 <= int(num) <= 5:
        raise ValueError
    except:
      client.send_message(message.channel, "**Ошибка!** Правильный формат: !lastb <num>. <num> может быть от 1 до 5")
      return
    else:
      client.send_message(message.channel, get_last_bump(num))

  elif message.content == '!anek':
    try:
      client.send_message(message.channel, get_anek())
    except:
      client.send_message(message.channel, '**Ошибка!** Вы делаете запрос слишком часто')
      
  elif message.content == '!anons':
    try:
      with requests.Session() as s:
        r = s.get('https://api.vk.com/method/wall.get?owner_id=-85854864&offset=0&count=1&filter=owner', timeout=5)
        if 'is_pinned' in r.json()['response'][1]: r = s.get('https://api.vk.com/method/wall.get?owner_id=-85854864&offset=1&count=1&filter=owner', timeout=5)
      client.send_message(message.channel, '%s\nДата новости: %s\nСсылка на стрим: http://www.ustream.tv/channel/strimach' %(r.json()['response'][1]['text'].replace('<br>','\n'),datetime.fromtimestamp(r.json()['response'][1]['date'])))
    except:
      client.send_message(message.channel, '**Ошибка!** Timeout запроса')

  elif message.content == '!anon.fm':
    try:
      client.send_message(message.channel, get_anon_fm())
    except:
      client.send_message(message.channel, '**Ошибка!** Вы делаете запрос слишком часто')
 
  elif message.content == '!help':
    client.send_message(message.channel, u'**Доступные команды:**\n\n**!news <1-3>**: Выводит список последних новостей 2ch.hk. В скобках указывается кол-во выводимых новостей, от 1 до 3;\n**!top <1-5>**: Выводит топ треадов /b/ по Score (одному Абу известно что это блять за очки такие). Может быть от 1 до 5;\n**!lastb <1-5>**: Выводит топ треадов /b/ по последнему бампу. Может быть от 1 до 5;\n**!anek**: Выдает анекдот уровня /b/;\n**!anons**: Выводит последний анонсированный фильм на Стримаче;\n**!anon.fm**: Выводит текущую композицию и анонс предстоящих трансляций anon.fm\n**!bump <thread num>,<bumps num>**: Включает Авто-бамп для выбранного треда. Бампает примерно раз в 15 секунд. *<bumps num>* - кол-во бампов от 1 до 300.')

@client.event
def on_ready():
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  print('------')
  [client.send_message(server, 'Бот зашел на канал. **!help** - список команд бота.') for server in client.servers]

client.run()

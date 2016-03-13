import requests, re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select

code = '856265569'
driver = webdriver.PhantomJS('d:/Downloads/python/phantomjs-2.1.1-windows/bin/phantomjs.exe')
pn_proxies = []
spys_list = []

with open('good_proxies.txt', 'r') as f: good_proxies = f.read().splitlines()

print('Грабим прокси...')

for country in ['RU','UA','US']:
  driver.get('http://spys.ru/proxys/'+country)
  select = Select(driver.find_element_by_id('xpp'))
  select.select_by_visible_text('200')
  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")
  for tr in soup.find_all('tr', {'class':re.compile(r'spy1x{1,2}')})[2:]:
    font = tr.find('font', {'class':"spy14"})
    spys_list.append(re.sub(r'^(\d+\.\d+\.\d+\.\d+).+\)(:\d{2,5})$', r'\1\2', font.text))
driver.quit()

with requests.Session() as s:
  try:
    r = s.post('https://hideme.ru/loginn', data={'c': code})
    r1 = s.get('http://hideme.ru/api/proxylist.txt?maxtime=5000&country=BYKZRUUAUS&out=plain', timeout=10)
    hideme_list = str(r1.text).splitlines()
    print('hideme: ', len(hideme_list))
  except Exception: hideme_list = []; print('hideme.ru error')
  
try:
  r2 = requests.get('http://freeproxy-list.ru/api/proxy?accessibility=80&anonymity=false&country=BY%2CRU%2CUA%2CGB&token=demo', timeout=10)
  freeproxy_list = str(r2.text).splitlines()
  print('freeproxy: ', len(freeproxy_list))
except Exception: freeproxy_list = []; print('freeproxy-list error')

try:
  r3 = requests.get('http://dogdev.net/Proxy/api/text/RU/r', timeout=10)
  dogdev_list = str(r3.text).splitlines()[1:]
  print('dogdev: ', len(dogdev_list))
except Exception: dogdev_list = []; print('dogdev error')

try:
  r4 = requests.get('http://txt.proxyspy.net/proxy.txt', timeout=10)
  proxyspy_list = re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)\sRU', r4.text)
  print('proxyspy: ', len(proxyspy_list))
except Exception: proxyspy_list = []; print('dogdev error')

try: r5 = requests.get('http://www.proxynova.com/proxy-server-list/country-ru/', timeout=10)
except Exception: pass; print('proxynova error')
soup = BeautifulSoup(r5.content, "html.parser")
tr = soup.findAll('tr')
for td in tr:
  try: pn_proxies.append(td.findAll('span', {'class': "row_proxy_ip"})[0].text + ':' + td.findAll('a', {'href': re.compile('/port')})[0].text)
  except Exception: pass
print('proxynova: ', len(pn_proxies))

try:
  r6 = requests.get('http://api.foxtools.ru/v2/Proxy', params={'country': 'RU'}, timeout=10)
  foxtools_list = ['%s:%s' %(i['ip'], i['port']) for i in r6.json()['response']['items']]
  print('foxtools: ', len(foxtools_list))
except Exception: foxtools_list = []; print('foxtools error')

try: r7 = requests.get('http://www.idcloak.com/proxylist/russian-proxy-list.html', timeout=10)
except Exception: pass; print('idcloak error')
soup = BeautifulSoup(r7.content, "html.parser")
idcloak_list = ['%s:%s' %(i.findAll('td')[-1].text, i.findAll('td')[-2].text) for i in soup.findAll('tr')[12:]]
print('idcloak: ', len(idcloak_list))

r8 = requests.get('http://www.gatherproxy.com/proxylist/country/?c=russia', timeout=10)
soup = BeautifulSoup(r8.content, "html.parser")
gatherproxy_list = ['%s:%s' %(re.findall(r'"PROXY_IP":"([\d\.]+)"', i.text)[0], int(re.findall(r'"PROXY_PORT":"(\w+)"', i.text)[0], 16)) for i in soup.findAll('script', {'type':'text/javascript'})[4:-4]]
print('gatherproxy: ', len(gatherproxy_list))

print('spys: ', len(spys_list))

proxy_lst = hideme_list + freeproxy_list + dogdev_list + \
proxyspy_list + foxtools_list + \
pn_proxies + good_proxies + idcloak_list + gatherproxy_list + spys_list

proxy_lst = list(set(proxy_lst))
print('\nПрокси загружено: ' + str(len(proxy_lst)))

import requests
from bs4 import BeautifulSoup

google_url = 'https://www.google.com/'

my_params = {'q': '寒流'}

r = requests.get(google_url, params = my_params)

if r.status_code == requests.codes.ok:
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup.prettify())
    # items = soup.select('div.g > h3.r > a[href^="/url"]')
    items = soup.select('div.g')
    for i in items:
      # 標題
      print("標題：" + i.text)
      # 網址
      print("網址：" + i.get('href'))
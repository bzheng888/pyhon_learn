from bs4 import BeautifulSoup
import requests
import time
import urllib.request
import os
import sys
BASE_DIR =  os.path.dirname( os.path.abspath(__file__) )#使用相对路径进行文件之间的访问和
path = BASE_DIR + '\\pics\\'
base_url = 'http://weheartit.com/inspirations/beach?page='
#proxies = {"http": "http://121.69.29.162:8118"} 反爬取使用代理
data_list = []
def get_info(url, data = None):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    pics = soup.select('div.entry-preview > a > img')
    if data == None:
        for pic in pics:
            data = {
                'url':pic.get('src'),
                'ref':pic.get('alt'),
            }
            data_list.append(data)

def get_more_pages(start,end): #根据动态网站特征获取更多内容
    for one in range(start,end):
        get_info(base_url+str(one))
        time.sleep(2)
def dl_image(url): #下载到本地
    urllib.request.urlretrieve(url, path + url.split('/')[-2] + '.jpg')

if __name__ == '__main__':
    get_more_pages(0, 2)
    for i in data_list:
        dl_image(i['url'])
        print(i['ref'])




from curl_cffi import requests
from lxml import etree
import os
import time
from multiprocessing.dummy import Pool
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}
header = {
    'referer': 'https://nhentai.net/g/450401/5/',
    'cookie':'csrftoken=rkElH0o6ECRk6poqTBjda9EVfmbcJnBUA3kNs6OuOvrPXQGqcWxWlQNPy98UQxch; cf_clearance=K43aWolURO5WdW3V.2ZYr7PiNvQZdGKOvPO9g0IN86k-1681277595-0-250',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}
url0 = 'https://nhentai.net/g/423751/'#这里是漫画地址
response0 = requests.get(url0, proxies=proxies,headers=header)
ym0 = response0.text
print('页面代码:',response0.status_code)
rrt0 =  etree.HTML(ym0)
title = rrt0.xpath('/html/body/div[2]/div[1]/div[2]/div/h2/span[@class="pretty"]/text()')#获取标题

try:
        t = title[0]
except:
        title = rrt0.xpath('/html/body/div[2]/div[1]/div[2]/div/h2/span[3]/text()')#获取标题
        t = title[0]
print('标题',t)#打印标题
time.sleep(5)
url = url0+'1'#第一页
response = requests.get(url, proxies=proxies,headers=header)
ym = response.text
code = response.status_code
print('第一页响应码',code)
rrt = etree.HTML(ym)
page = rrt.xpath('//*[@id="content"]/section[4]/div[2]/button/span[3]/text()')
imgurl = rrt.xpath('//*[@id="image-container"]/a/img/@src')
print(page[0])
print(imgurl[0])
url1 = imgurl[0].replace('1.jpg','')
print(url1)
page1 = int(page[0])#页数
x= 1
if not os.path.exists('D:/manga/%s'%t) :#判断有无文件夹
    os.makedirs(r'D:/manga/%s'%t)


def imgget(s):
    url2 = url1+'%s'%s+'.jpg'
    print(url2)
    turesponse = requests.get(url2, proxies=proxies,headers=header)
    f = open('d:/manga/%s/tu%s.jpg'%(t,s),'wb')
    f.write(turesponse.content)
   

pool = Pool(5)#线程数
s = range(page1)
pool.map(imgget,s)   
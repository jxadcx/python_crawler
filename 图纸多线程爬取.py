import requests
import os
import tqdm
from lxml import etree
from multiprocessing.pool import ThreadPool #import ThreadPool
import time
# 使用requests库获取网页内容
response = requests.get('https://www.gadget-manual.com/dell/')
html = response.content

# 使用xpath解析网页内容
selector = etree.HTML(html)
#download_links0 = selector.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div/div[2]/div/p/a/@href')#nvidia or amd or anrock
#download_links0 = selector.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div/div[2]/div/p/a/@href')
download_links0 = selector.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div/div[2]/div/p/u/a/@href')#hp
if len(download_links0)<50:
    download_links0 = selector.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div/div[2]/div/p/a/@href')
if len(download_links0)<50:
    download_links0 = selector.xpath('/html/body/div[1]/div/div[4]/div/div[2]/div/div[2]/div/div/div[1]/div/p/u/a/@href')

# 创建文件夹
if not os.path.exists('D:/tuzhi'):
    os.makedirs('D:/tuzhi')
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}
he = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

max = len(download_links0)
print('链接数量',max)
x1 = 0

#定义下载函数
def download(link0):
    try:
        x=download_links0.index(link0)
        print('开始第{}个'.format(x))
        response0 = requests.get(link0,proxies=proxies,headers=he,timeout=6)
        html0 = response0.text
        # 使用xpath解析网页内容并获取文件名
        selector0 = etree.HTML(html0)
        filename0 = selector0.xpath('/html/head/meta[4]/@content')[0]#获取文件名
        print('文件名',filename0)
        # 将文件名按规则替换为下载链接
        link = link0.replace('/view?usp=sharing', '&export=download').replace('/file/d/', '/u/0/uc?id=').replace('/open?id=', '/u/0/uc?id=').replace('/view?usp=drivesdk','&export=download')#HP
        if '&export=download' not in link:
            link=link+'&export=download'


        filepath = 'D:/tuzhi/' + filename0#文件保存路径
        print(link)#打印下载链接

        try:
            # 计算下载文件的大小，如果小于5kb就重新下载
            response = requests.get(link,proxies=proxies,headers=he, stream=True)
            with open(filepath,'wb') as f:
                f.write(response.content)
                f.close()
            if os.path.exists(filepath):# 计算下载文件的大小，如果小于5kb就重新下载
                size = os.path.getsize(filepath)
                sizekb = '%.1f'%(size/1000)
                print('第{}个文件大小{}kb'.format(x,sizekb))
                while(1):
                    if size > 5*1024:
                        print('跳过')
                        break                  
                    else:
                        time(5)
                        print('{}重来！'.format(x))
                        response = requests.get(link,proxies=proxies,headers=he, stream=True)
                        with open(filepath,'wb') as f:
                         f.write(response.content)
                         f.close()
                         size = os.path.getsize(filepath)
                         

        except:
            print('错误',link)
    except:
        print('跳过{}'.format(x))
    x+=1

#使用线程池
pool = ThreadPool(5) #线程数5
pool.map(download, download_links0[x1:max])
pool.close()
pool.join()


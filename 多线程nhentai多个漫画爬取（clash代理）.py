from curl_cffi import requests
from lxml import etree
import os
import time
from multiprocessing.dummy import Pool
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}
#url_s = 'https://nhentai.net/g/182465/'

def main():
    header = {
        'referer': 'https://nhentai.net/tags/popular?page=4',
        'cookie':'cf_clearance=bcAUyUdbiTXEa9kCBB.R.mGD_5H2WuxhQXQs.SK5PL0-1714744764-1.0.1.1-xajmTRD2.5gh88WR2Nt8qHw5XcsYQ0zMIStIxmUVJMVbNveLswiWD_xc.SHdA_vJK8EeF7h_pcrv3Aw9_yn7pw; csrftoken=HfLhaQswTpuLityOmqBmRz6ymR2qErCy3NVXegeLzE46J3yyDoUmiduyYmhst7uP; sessionid=fw2qmcuarkjnyl1nq9pn4fdtza2v1qez; cf_clearance=h2XHK0qzazaxKUISpzVRW4.THmWeji_I0YFinYKzQAg-1717234773-1.0.1.1-hEzPAKutdN4SR15yCcm.5N5Jj__ybbtXhmqx_Y45_u3jJWbIwTgGA2Qjzn69Aax_OVkBgy0vPL1arOwY8rpFRQ',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    url0 = url_s#这里是漫画地址
    print('开始',url0)
    response0 = requests.get(url0, proxies=proxies,headers=header)
    ym0 = response0.text
    print('页面代码:',response0.status_code)
    if response0.status_code == 403:
         print('403错误,停止运行')
         exit()
    eh =  etree.HTML(ym0)
    title = eh.xpath('/html/body/div[2]/div[1]/div[2]/div/h2/span[@class="pretty"]/text()')#获取标题
    try:
        try:
                t = title[0]
        except:
                title = eh.xpath('/html/body/div[2]/div[1]/div[2]/div/h2/span[3]/text()')#获取标题
                t = title[0]
    except:
        title = eh.xpath('/html/body/div[2]/div[1]/div[2]/div/h1/span[@class="pretty"]/text()')
        t = title[0]
    print('标题',t)#打印标题
    time.sleep(3)
    url = url0+'1'#第一页
    response = requests.get(url, proxies=proxies,headers=header)
    ym = response.text
    code = response.status_code
    if response.status_code == 403:
         print('第一页403错误,停止运行')
         exit()
    print('第一页响应码',code)
    eh1 = etree.HTML(ym)
    page = eh1.xpath('//*[@id="content"]/section[4]/div[2]/button/span[3]/text()')
    imgurl = eh1.xpath('//*[@id="image-container"]/a/img/@src')
    print(page[0])
    print(imgurl[0])
    url1 = imgurl[0].replace('1.jpg','')
    print(url1)
    page1 = int(page[0])#页数
    x= 1
    manga='manga/mangaero2'
    if not os.path.exists(f'D:/{manga}'): #判断是否创建manga文件夹
        os.makedirs(f'D:/{manga}')
    t =t.replace('?','')
    if not os.path.exists(f'D:/{manga}/{t}') :#判断是否创建漫画文件夹
        os.makedirs(f'D:/{manga}/{t}')


    def imgget(s):
        url2 = url1+'%s'%s+'.jpg'
        print(url2)
        try:
            turesponse = requests.get(url2, proxies=proxies,headers=header)
            f = open('d:/%s/%s/tu%s.jpg'%(manga,t,s),'wb')
            f.write(turesponse.content)
        except:
             print(s,'报错')
    

    pool = Pool(5)#线程数
    s = range(1,page1)#起始页和最终页
    pool.map(imgget,s)#多线程运行   

list = (454561,512400,450735,450732,446393,443802,474794,480044,485780,441547,441405,507830,436310,432441,)
# list = (411631,492475)
for code in list:
        url_s = f'https://nhentai.net/g/{code}/'
        # url_s = f'https://nhentai.net/g/506314/'
        print(url_s)
        try:
                main()
        except:
             print(code,'失败')
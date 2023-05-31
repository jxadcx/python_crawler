import requests
import urllib3
from lxml import etree
import os
import random
import time
import sys
urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 10

def main():
    def get_ua():#随机ua函数
        first_num = random.randint(55, 62)
        third_num = random.randint(0, 3200)
        fourth_num = random.randint(0, 140)
        os_type = [
            '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
            '(Macintosh; Intel Mac OS X 10_12_6)'
        ]
        chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

        ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                    '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                    )
        return ua
    ua = get_ua()
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
        
    }
    header = {#请求头
        'referer': 'https://nhentai.to/search?q=chinese',
        'cookie':'__PPU___PPU_SESSION_URL=%2F; _ga=GA1.2.2104026627.1679642262; _gid=GA1.2.1813232435.1679642262; __dtsu=6D0016781023829AC07C1DA108C01435; eloquent_viewable=eyJpdiI6ImlwbUw3ZFNFU3RDMVlISTkyMWx5aXc9PSIsInZhbHVlIjoiYU9zb1Fud2l3bW8xdkEzQ1JTRzM1Tkg0bUQrYmI4T284REcrLzBubHVOVGdFTHRvcjhZSkNGdWovaWxQTTNuS21KUTdISlBja1NsVUhnWlgxOHZzeFFpZURrR0tQMWxLbFc1djFPcE9jQ2c2SHRINzU1Y2dLKzEvb0lFeUVvdTciLCJtYWMiOiJlODU3ODZiMjU0NTkyZGQ2YTBlMjk3Mzg5NDgyNTk5MzM3ZjU2YjQzMmE4ZjNhOTQ4NjI0OTQwYTdlMDZiNzUyIn0%3D; XSRF-TOKEN=eyJpdiI6IlhjN1B3MTlaRHBzTTFBUXFxTmxSRkE9PSIsInZhbHVlIjoiMk9FV3lpNEprc3N6MkNBanVwdzhHMVBORUZCeUw1a3Rtd1gwbGxLRzNsQkt0ODI5THJRYUlYU3NTR1Bua050WiIsIm1hYyI6ImFjMjAxYzg1NmE0MTAyZDE4MTBmODFmY2QzMjBhMDE3ZmExODY2ZWRlZWI1NDQ0NTI3YjRiYjgxN2NmNDY2M2IifQ%3D%3D; nhentai_session=eyJpdiI6Im9zLzUxSHU1ZFQ0N3c5Y1Z3eUR2amc9PSIsInZhbHVlIjoiSFh0dzRXZXQ4Z21XWHA3djUzeVpYbklEdmdXaFhobklSOXArQzN3SVJoQkhjaVF2eXhaSmxkbmFlaStMYkNKNCIsIm1hYyI6ImI5MDJhYjdhZDZkODlmNzQ5M2Y4MmRhMzdhNGU4NWI4MDA5N2M0ZjI0Y2Q2ZTA0NzNhMWZjMTRhNzI5MDZlOTkifQ%3D%3D',
        'user-agent': ua
    }
    #print(ua)
    def get_url(url):
        try:
            response = requests.get(url, headers=header, timeout=10)  # 超时设置为10秒
        except:
            for i in range(10):  # 循环去请求网站
                response = requests.get(url, headers=header, timeout=20)
                if response.status_code == 200:
                    break
        html_str = response.content
        return html_str


    url0 = 'https://nhentai.to/g/383026'
    try:
            response0 = requests.get(url=url0,proxies = proxies,verify=False,headers=header)
    except:
            response0 = requests.get(url=url0,proxies = proxies,verify=False,headers=header)
    print("响应码:",response0.status_code)
    ym0 = response0.text
    rrt0 =  etree.HTML(ym0)
    title = rrt0.xpath('//*[@id="info"]/h2/text()')#获取标题
    page = rrt0.xpath('//*[@id="tags"]/div[6]/span/a/span/text()')#获取页数
    try:
        try:
            p = int(page[0])
        except Exception:
            page = rrt0.xpath('//*[@id="tags"]/div[7]/span/a/span/text()')
            p = int(page[0])
    except:
        page = rrt0.xpath('//*[@id="tags"]/div[5]/span/a/span/text()')
        p = int(page[0])
    
    print('总页数',p)#打印页数
    try:
        t = title[0]
    except:
        title = rrt0.xpath('//*[@id="info"]/h1/text()')#获取标题
        t = title[0]
    print('标题',t)#打印标题
    

    url = url0+'/1'#第一页
    try:
        response = requests.get(url, proxies=proxies,verify=False,headers=header)
    except:
        response = requests.get(url, proxies=proxies,verify=False,headers=header)
    ym = response.text
    print('第一页响应码',response.status_code)
    rrt = etree.HTML(ym)
    imgurl = rrt.xpath('//*[@id="image-container"]/a/img/@src')#第一页图片地址
    url1 = imgurl[0].replace('1.jpg','')#替换

    if not os.path.exists('D:/manga/%s'%t) :#如果没有文件夹,则创建
        os.makedirs(r'D:/manga/%s'%t)
        print('创建文件夹')
    print('文件夹已创建')

    #x=25
    global x
    
    while x<=p:
        
        os.environ['NO_PROXY'] = 'img.dogehls.xyz'
        url2 = url1+'%s'%x+'.jpg'
        begin_color = '\033[1;31m'
        end_color = '\033[0m'
        print(begin_color+url2+end_color)
        'try:'
        turesponse = requests.get(url2, proxies=proxies,verify=False,headers=header,timeout=15)
        print('第%s页'%x)
        content_size = int(turesponse.headers["content-length"])  # 文件总字节数
        print('[图片大小]: {:.1f} KB'.format(content_size / 1024))#转为kb单位
        '''except:
            turesponse = requests.get(url2, proxies=proxies,verify=False,headers=header,timeout=15)
            print('except进行')'''
        start_time = time.time()
        with open('d:/manga/%s/tu%s.jpg'%(t,x),'ab') as f:
         total_data = turesponse.content
         chunk_size = 1024#每次下载数据大小
         
         '''for data in response0.iter_content():
             
            f.write(data)
            size = 0
            size=len(data)
            #print('\r[下载进度]: {}{:.2f}%'.format('>' * int(size * 1 / content_size), float(size / content_size * 100)),end='')  # 下载进度条
            print('>',end = '')
            f.close'''
         f.write(total_data)
         f.close
         end_time = time.time()
         print('下载时间%.3f秒'%(end_time-start_time))
        x+=1
    else:
        print('完成,结束运行')    
        sys.exit()


x = 90#起始页数(大于等于1)
def try1():
    try:
        main()
    except Exception as e:
        print('错误信息:',str(e))
      
while(1):
    try1()
    print('重试,目前页数',x)
    #time.sleep(3)
    
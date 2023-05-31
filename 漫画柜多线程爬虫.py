

import requests
# import json
import time
# import random
from multiprocessing.dummy import Pool
import re
import os
# import sys
# import urllib.parse
# import http.cookiejar
from bs4 import BeautifulSoup
import lzstring
import execjs 
# 设置代理端口
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 爬取漫画
def get_comic():
    lz = lzstring.LZString()
    # 漫画首页
    url = 'https://www.manhuagui.com/comic/23953/'
    
    # 请求头
    headers = {
        'Sec-Ch-Ua-Platform':"Windows",
        # 'Upgrade-Insecure-Requests':1,
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/258.109.130.111 Safari/537.3'}
    print('开始访问漫画链首页',url)
    # 获取漫画首页
    for x in range(4):
            try:
                response = requests.get(url, headers=headers, proxies=proxies,timeout=15)
                if response.status_code==200:
                    print('成功')
                    break
                else:
                    print('失败')
            except:
                print('重试',x)
                if x==3:
                    print('访问漫画页失败,停止运行')
                    exit()
#     print(response)
    # 解析漫画首页
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    # 获取漫画章节列表
    manga_name = soup.find_all('h1')[0].text
    print('漫画名:',manga_name)
    chapter_list = soup.find_all('a',{'class':'status0'})
#     print(chapter_list)
    # 遍历漫画章节列表
    print('总共',len(chapter_list))
    s_n = 0#起始话数
    st = s_n#计数
    for chapter in chapter_list[s_n:]:
        host = 'https://manhuagui.com'
        # 获取章节链接
        chapter_url = host+chapter['href']
        # 获取章节名称
        chapter_name = chapter.text
        # 获取章节页数
        chapter_page = int(re.findall(r'\d+', chapter_name)[0])
        # 创建章节目录
        chapter_dir = f'd:/manga/{manga_name}/{chapter_name}'#os.path.join(os.getcwd(), chapter_name)
        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)
        # 遍历章节页数
        print(f'开始访问章节{chapter_name}---{chapter_url}')
        chapter_header={
            'Referer':'https://www.manhuagui.com/user/book/shelf',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/5.101.30.11 Safari/537.3'

        }
        print('开始访问章节第一页获取eval密文')
        for x in range(5):
            try:
                page_response = requests.get(chapter_url, headers=chapter_header, proxies=proxies,timeout=15)
                if page_response==200:
                    print('成功')
                    break
            except:
                print('重试',x)
        page_soup = BeautifulSoup(page_response.text, 'html.parser')
        page_body = page_soup.find_all('body')[0]
        page_eval_n = page_body.find_all('script')[2].text#未解密的eval代码段
        # print(page_eval_n)
        try:
            lzstring_code_0 = re.findall("\d\d,\d\d,'(.*?)'", page_eval_n)[0]#获取密文
        except:
            lzstring_code_0 = re.findall("\d\d,\d\d\d,'(.*?)'", page_eval_n)[0]#获取密文
        # print(lzstring_code)
        lzstring_code = lzstring_code_0
        lzstring_decrypt = lz.decompressFromBase64(lzstring_code)#解密

        # print ('lzstring_decrypt=',lzstring_decrypt)
        page_eval_y = page_eval_n.replace(lzstring_code_0+"'"+"['\\x73\\x70\\x6c\\x69\\x63']('\\x7c')",lzstring_decrypt+"'"+".split('|')").replace('window["\\x65\\x76\\x61\\x6c"]','eval')
        
        # print(page_eval_n)
        # print('\n\n',page_eval_y,'\n\n')
        smh_code = re.findall("return p;}\('(.*?)\(",page_eval_y)[0]
        pre_code = re.findall('"\}\}\)(.*?);',page_eval_y)[0]
        page_eval_d = page_eval_y.replace(smh_code,'').replace(pre_code,'')#.replace('\\','\\\\')#删除解析函数
        # print(page_eval_d)
        page_eval_js = execjs.compile('''function e(){return %s}'''%page_eval_d)#构建函数获取json
        
        chapter_json=page_eval_js.call('e')#传参
        print(chapter_json['bname'])
        img_names = chapter_json['files']
        img_path = chapter_json['path']
        e=chapter_json['sl']['e']
        m=chapter_json['sl']['m']
        # global st
        # global st
        
        def imgget(img_number):
            img_url='https://i.hamreus.com'+img_path+img_names[img_number]#+'?e='+str(e)+'&m='+m
            print('图片链接',img_url)
            with open('d:/manga.txt','a') as fm:
                fm.write(f'{chapter_name}-{img_names[img_number]}-{img_url}\n')
                fm.close()
               
            header = {
  'Referer':'https://www.manhuagui.com/',
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
            params = {
    "e": e,
    "m": m
}           
  
            for rx in range(15):
                try:
                    img_response = requests.get(img_url,headers=header,params=params,proxies=proxies,timeout=10)
                    if img_response.status_code==200:
                        print(f'{img_number}图片响应')
                        break
                except:
                    print('重试',rx)
                    
            
            if img_response.status_code==200:
                with open(f'{chapter_dir}/{img_names[img_number]}','wb') as fi:
                    fi.write(img_response.content)
                    fi.close()
                    print(f'保存st={st}---{chapter_name}---{img_names[img_number]}\n')
                    
        
        pool = Pool(5)#线程数
        # img_name = img_names[range(len(img_names))]#列表范围
        img_number=range(len(img_names))
        pool.map(imgget,img_number)         
        st+=1
if __name__ == '__main__':
    get_comic()


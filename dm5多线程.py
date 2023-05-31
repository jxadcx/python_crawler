import requests 
import os
from lxml import etree
import re
from selenium import webdriver
import threading

url = 'https://www.dm5.com/manhua-qiangweishaonv/' # 漫画的url
response = requests.get(url) # 获取响应
print(response) # 打印响应
html = etree.HTML(response.text) # 解析响应的源代码
manga_title = html.xpath('/html/body/div[3]/section/div[2]/div[2]/p[1]/text()') # 获取漫画标题
chapter_title = html.xpath('/html/body/div[4]/div/div[2]/div[1]/div[2]/ul/li/a/text()') # 获取章节标题
chapter_links=html.xpath('/html/body/div[4]/div/div[2]/div[1]/div[2]/ul/li/a/@href') # 获取章节链接
chapter_img_count=html.xpath('/html/body/div[4]/div/div[2]/div[1]/div[2]/ul/li/a/span/text()') # 获取章节图片数量

chapter_img_count = [re.sub(r'\D', '', count) for count in chapter_img_count] # 保留每个元素中的数字
chapter_img_count = [int(count) for count in chapter_img_count] # 将每个元素转换为整数类型
chapter_links = ['https://www.dm5.com' + link for link in chapter_links] # 将前缀添加到每个链接
manga_title = manga_title[0].replace(' ','') # 去除漫画标题中的空格
chapter_title = [title.replace(' ', '') for title in chapter_title]# 去除章节标题列表中每个元素中的空格
chapter_title = list(filter(None, chapter_title))#删除空元素

print(manga_title)
print(chapter_title)
print(chapter_links)
print(chapter_img_count)

chapter_count = 2#len(chapter_links)#结束章节
x=1#开始章节

def download_chapter(xx):
    header = {
        'referer': chapter_links[x],
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }
    while xx<chapter_img_count[x]: # 当前章节的图片数量
        chapter_img_url = chapter_links[x]+'#ipg{}'.format(xx) # 当前图片页的url
        print(chapter_img_url) # 打印当前图片页的url
        driver = webdriver.Chrome() # 启动Chrome浏览器
        driver.get(chapter_img_url) # 访问当前图片页的url
        chapter_response = driver.page_source # 获取当前页面的源代码
        chapter_html = etree.HTML(chapter_response) # 解析当前页面的源代码
        img_url = chapter_html.xpath('/html/body/div[6]/div/img/@src') # 获取当前图片的url
        print(img_url) # 打印当前图片的url
        img_response = requests.get(img_url[0],headers=header) # 获取当前图片的响应

        if not os.path.exists(f'd:/manga/{manga_title}/{chapter_title[x]}'): # 如果当前章节的文件夹不存在
            os.makedirs(f'd:/manga/{manga_title}/{chapter_title[x]}') # 创建当前章节的文件夹

        with open (f'd:/manga/{manga_title}/{chapter_title[x]}/{xx}.jpg','wb') as f: # 打开当前图片的文件
            f.write(img_response.content) # 写入当前图片的内容
        xx+=1 # 图片数量加1

threads = []
while x<chapter_count:
    print('链接',chapter_links[x]) # 打印当前章节链接
    print('章节名',chapter_title[x]) # 打印当前章节名
    print('图片数',chapter_img_count[x]) # 打印当前章节图片数
    for i in range(3):
        t = threading.Thread(target=download_chapter, args=(i,)) # 创建线程
        threads.append(t) # 将线程添加到列表中
        t.start() # 启动线程
    for t in threads:
        t.join() # 等待所有线程结束
    x+=1 # 章节数加1

  

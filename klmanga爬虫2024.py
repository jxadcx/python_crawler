import requests
from lxml import etree 
from time import time
import re
import os
host='https://jestful.net'
manga_name='hwms-ojousama-no-shimobe'

chapter = '/app/manga/controllers/cont.listChapter.php?slug='+manga_name#获取章节链接(没用)
chapterid='/app/manga/controllers/cont.listChapters.php'#获取章节id,
chapterimg = '/app/manga/controllers/cont.listImg.php'#通过章节id获取章节内图片链接
header = {
'Referer':'https://jestful.net/hwms-ojousama-no-shimobe.html',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

}
def get_chapter_id_all(manga):#获取章节id,
        params={'manga':manga}
        response=requests.get(host+chapterid,params=params,headers=header)
        print("状态:",response.status_code)
        return response.json()
def get_chapter_imgpage(cid):#通过章节id获取章节包含图片链接的源码
        params={'cid':cid}
        response=requests.get(host+chapterimg,params=params,headers=header)  
        print("状态:",response.status_code) 
        response = response.text.replace('\n','').replace('\r','')
        img_url_all = re.findall("src='(.*?)' alt='Page",response)
        return img_url_all

#第一步,获取漫画所有章节id
chapter_id_all = get_chapter_id_all(manga_name)
for chapter_id in chapter_id_all:
        print(chapter_id)
        #第二步,获取
        chapter_imgpage = get_chapter_imgpage(chapter_id['id'])
        print(chapter_imgpage)
        #第三步,保存图片

        manga_folder = 'd:/manga/'+manga_name+'/'+str(chapter_id['chapter'])  
        # 检查文件夹是否存在  
        if not os.path.exists(manga_folder):  
        # 如果文件夹不存在，则创建文件夹  
                os.makedirs(manga_folder, exist_ok=True)

        n=1
        for img_url in chapter_imgpage:
                print('当前链接:%s'%img_url)
                response = requests.get(img_url,headers=header)
                print("状态:",response.status_code) 
                with open ('%s/%s.jpg'%(manga_folder,n),'wb') as f:
                        f.write(response.content)
                n+=1
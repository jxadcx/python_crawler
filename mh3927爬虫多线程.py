
import re
import os

def key_value():
    with open('D:/gm.txt', 'r', encoding='utf-8') as f:
        for line in f:
            # 检查该行是否包含“射击”，“动作”和“战略”
            if '射击' in line or '动作' in line or '战略' in line:
                # 删除关键字后面的内容并打印剩余内容
                line=line.split('射击')[0].split('动作')[0].split('战略')[0]
                # print(line)  
                line = '--'.join(line.split())
                 

                # 从line字符串中搜索'--',如果有两个,那就删掉第二个'--'保留第一个'--'
                if line.count('--') >= 2:
                    print('有一个')
                    linelist = line.split('--')
                    print(linelist)
                    line = linelist[0]+'--'+linelist[1]+linelist[2]
                    print(line)
                with open('D:/gm2.txt', 'a', encoding='utf-8') as f1:
                    f1.write(line + '\n')

  
# key_value()
def key_value2():
    with open('D:/gm.txt', 'r', encoding='utf-8') as f:
        for line in f:
            # print(line)
            line = line.split(' ')[0]
            # line = '--'.join(line.split())
            line = line.replace(' ','')
            print(line)

            with open('D:/gm3.txt', 'a', encoding='utf-8') as f1:
                    f1.write(line + '\n')




def dictrename():
    # 读取文件并将每一行按-为分隔符拼成键值对保存到字典
    name_dict = {}
    with open('D:/gm2.txt', 'r', encoding='utf-8') as f:
        for line in f:
        
            key, value = line.strip().split('--')
            # print(key,value)
            name_dict[key] = value

    # 获取目标文件夹路径
    folder_path = r'e:/临时解压'

    # 获取目标文件夹下所有文件名
    file_names = os.listdir(folder_path)

    # 遍历文件名列表，依次修改文件名为字典中的值
    for file_name in file_names:
        # print(file_name)
        # 构造旧文件路径
        old_file_path = os.path.join(folder_path, file_name)
        # print(old_file_path)
        # 如果文件名包含在字典的键中
        keylist=[]
        keylist =name_dict.keys()
        
        for key1 in keylist:
            # print(key1)
            if key1 in file_name:
                new_file_name = name_dict[key1]+'.SMC'
                new_file_path = os.path.join(folder_path, new_file_name)
                os.rename(old_file_path, new_file_path)
                print(new_file_path)





def dictrename2():
    name_dict = {}
    with open('D:/gmx.txt', 'r', encoding='utf_8') as f:
        for line in f:
            print(line)
            name_dict[line.split('_', 1)[0]] = line.split('_', 1)[1].strip()
    
    # 获取目标文件夹路径
    folder_path = r'E:/sfcgame'
    # 获取目标文件夹下所有文件名
    file_names = os.listdir(folder_path)

    # 遍历文件名列表，依次修改文件名为字典中的值
    for file_name in file_names:
        # print(file_name)
        # 构造旧文件路径
        old_file_path = os.path.join(folder_path, file_name)
        # print(old_file_path)
        # 如果文件名包含在字典的键中
        keylist=[]
        keylist =name_dict.keys()
        
        for key1 in keylist:
            # print(key1)
            if key1 in file_name:

                new_file_name = name_dict[key1].replace('?', '').replace('/', '').replace(':', '').replace('*', '').replace('\\', '')+'.SMC'
                new_file_path = os.path.join(folder_path, new_file_name)
                print(key1)
                os.rename(old_file_path, new_file_path)
                print(new_file_path)


# dictrename2()



import requests
import os
from lxml import etree
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
url='https://mh3927.com/jp/'
def main(url):

    response=requests.get(url)
    response.encoding='utf-8'
    print(response.text)
    html = etree.HTML(response.text)
    atlas_links = html.xpath('/html/body/div[2]/div/div[2]/div/h3/a/@href')
    atlas_links = ['https://mh3927.com'+a for a in atlas_links]
    print(atlas_links)
    atlas_names = html.xpath('/html/body/div[2]/div/div[2]/div/h3/a/text()')
    print(atlas_names)
    get_img_count=0
    x=0
    while x<len(atlas_links):
        img_path=f'd:/meinv/杂志/{atlas_names[x]}'
        if not os.path.exists(img_path): # 如果当前章节的文件夹不存在
                    os.makedirs(img_path) # 创建当前章节的文件img夹

        atlas_details_response=requests.get(atlas_links[x])
        atlas_html = etree.HTML(atlas_details_response.text)
        real_atlas_url=atlas_html.xpath('/html/body/div[2]/div[4]/div/ul/li/a/@href')
        real_atlas_url='https://mh3927.com'+real_atlas_url[0]
        real_atals_response = requests.get(real_atlas_url)
        real_atlas_html=etree.HTML(real_atals_response.text)
        all_img_links=real_atlas_html.xpath('/html/body/div[2]/div[1]/div/div/div[2]/article/img/@src')
        xx=0
        print(all_img_links)
       
        
        
        def imgget(xx):
            header={
                'Referer': 'https://mh3927.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
                        }
            
            print(f'开始{x}/{len(atlas_names)}:{atlas_names[x]}的第{xx}/{len(all_img_links)}张图,总计:{get_img_count}')
            try:
                img_response = requests.get(all_img_links[xx],headers=header,verify=False,timeout=10)
                
            except:
                print('超时重试')
                img_response = requests.get(all_img_links[xx],headers=header,verify=False,timeout=14)
            with open(f'{img_path}/{xx}.jpg','wb') as f:
                f.write(img_response.content)
                print('成功')
                get_img_count+=1
            
        page1=len(all_img_links)
        pool = Pool(5)#线程数
        s = range(1,page1)#起始页和最终页
        pool.map(imgget,s)#多线程运行  


        x+=1

# https://mh3927.com/zz/list_1199_2.html

urls=[f'https://mh3927.com/zz/list_1199_{aa}.html' for aa in range(1,7)]
for url in urls:
      main(url)
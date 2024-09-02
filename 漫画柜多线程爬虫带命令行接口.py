import requests
import time
from multiprocessing.dummy import Pool
import re
import os
from bs4 import BeautifulSoup
import lzstring
import execjs 
from colorama import init
import argparse
import sys
from threading import Thread
import shutil
'''python manhuagui1.py --number 21013,5776,5812,4066,15099,893,8344,1324,5752,12431,20958,813,5755,481,21010,4231,4520,5364,8175,5642,33228,40870'''
command_key = 'c'
# 定义一个实时获取键盘输入的程序
def get_command(): 
    global command_key # 因为后续要对这个command_key 进行修改，所以这里需要声明成global
    command_key = input() # 获取输入
    get_command() # 获取下一次输入
 
# 定义一个线程   
# thd = Thread(target = get_command) #线程定义
# thd.start() # 开启线程


parser = argparse.ArgumentParser(description='接受参数')
parser.add_argument('--number',type=str,default='', help='输入需要爬取漫画的序号,多个用,分隔如 123,333,444')
parser.add_argument('--thread',type=int,default='5', help='线程数')
parser.add_argument('--mclass',type=str,default='分类', help='输入漫画分类(保存在相应文件夹)')
args = parser.parse_args()
init(autoreset=True)
# 设置代理端口
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 爬取漫画
def get_comic(url,s_n=0):
    lz = lzstring.LZString()#lzstring对象
    global ulist_lenth_count
    
    # 请求头
    headers = {
        'Sec-Ch-Ua-Platform':"Windows",
        # 'Upgrade-Insecure-Requests':1,
        'cookie': 'country=TW; SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; _ga=GA1.1.1975899830.1684890144; bitmedia_fid=eyJmaWQiOiI5MGZkYTM4NGZmNzcxZGMzZTg2N2JiNTc3YjY1ZjEwZSIsImZpZG5vdWEiOiJmNGViYmU1NmU1NDhlMjBiMmUzNDViZjBlZjQxZThhYiJ9; isAdult=1; CFFPCKUUID=2249-Sau2FbpET6VOm3MouSvMKc5fq2DIEPgc; CFFPCKUUIDMAIN=7065-2XlWqhiJApeyUjFTNxxQ3DmX8rvLXMrW; FPUUID=7065-51c52b31a76f37bf81121e30f507b679c1675ed57fdf7c26cef63781ef0634df; __htid=15e5a62d-0973-42a7-adf6-a733eff2f544; _im_vid=01H196AZJY0XAFY7Z1QKMFC2NT; cto_bundle=ajWV4l9mdUdqTldmZGdWb08zZWZxTDl4YkZjWGpHdHVkMmVqTHNVeXd3MTBIT2RodFpOZW1ReHN3UkMwSkxqNCUyQmNTMWNYNSUyRmh4TVB1aXlrV1N3andnaE5vR2JuT2hLeUMlMkJ3ZlRob3JTcVpWZW9TdGpvNHZEcHVxeEpsRHlyU3FMVXoyYWVvd3BKSm5GQlhFSGl3alEwQnlDOFElM0QlM0Q; _ga_H5F270PE29=GS1.1.1686443546.80.1.1686443640.0.0.0'
        ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.13.30.11 Safari/537.3'}
    print('开始访问漫画首页')
    # 获取漫画首页
    for x in range(4):
            try:
                response = requests.get(url, headers=headers, proxies=proxies,timeout=15)
              #   print(response.text)
                if response.status_code==200:
                    print('成功')
                    break
                else:
                    print('响应码',response.status_code)
                    print('失败')
            except:
                print('重试',x)
                if x==3:
                    print('访问漫画页失败,停止运行')
                    os._exit(0)
#     print(response)
    # 解析漫画首页
    soup = BeautifulSoup(response.text, 'html.parser')
#     print(soup)
#     print(len(response.text))
    # 获取漫画章节列表
    manga_name = soup.find_all('h1')[0].text.replace(':','')
    print('漫画名:',manga_name,'----',u)
    chapter_list = soup.find_all('a',{'class':'status0'})
    if len(chapter_list) == 0:
         print('可能为限制漫画')
         chapter_lzstring =  soup.find(id='__VIEWSTATE')['value']
         chapter_lzstring_decompress = lz.decompressFromBase64(chapter_lzstring)
         chapter_list_html = BeautifulSoup(chapter_lzstring_decompress,'html.parser')
         chapter_list = chapter_list_html.find_all('a',{'class':'status0'})
    
#     print(chapter_list)
    # 遍历漫画章节列表
    with open('d:/mangalist.txt','a',encoding='utf-8') as ml:
         ml.write(f'{u}---{manga_name}\n')
         ml.close()
    print('总共',len(chapter_list))
#     s_n = 0#起始话数
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
        manga_name = manga_name.replace('?','').replace('？','')
        chapter_dir = f'd:/manga/{args.mclass}/{manga_name}/{chapter_name}'#os.path.join(os.getcwd(), chapter_name)
        chapter_dir = f'd:/manga/{args.mclass}/{manga_name}/{chapter_name}'#os.path.join(os.getcwd(), chapter_name)

        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)
        
        # 遍历章节页数
        print(f'开始访问章节{chapter_name}---')
        chapter_header={
            'Referer':'https://www.manhuagui.com/user/book/shelf',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.101.0.21 Safari/537.3'

        }
        print('开始访问章节第一页获取加密EVAL')
        for x in range(5):
            try:
                page_response = requests.get(chapter_url, headers=chapter_header, proxies=proxies,timeout=15)
                print(page_response)
              #   if page_response.stu==200:
              #       print('成功')
                break
            except:
                print('重试',x)
        page_soup = BeautifulSoup(page_response.text, 'html.parser')
        page_body = page_soup.find_all('body')[0]
        page_eval_n = page_body.find_all('script',type="text/javascript")[1].text#未解密的eval代码段
       #  print(page_eval_n)
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
       

        def imgget(img_number):
              global img_count
              global hard_size
              img_url='https://i.hamreus.com'+img_path+img_names[img_number]#+'?e='+str(e)+'&m='+m
            
              with open('d:/manga.txt','a') as fm:
                fm.write(f'{chapter_name}-{img_names[img_number]}-{img_url}\n')
                fm.close()
               
              header = {
  'Referer':'https://www.manhuagui.com/',
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.10.20.30 Safari/537.36'}
              params = {
                             "e": e,
                             "m": m
                            }           
              img_dir =f'{chapter_dir}/{img_names[img_number]}'
              for rx in range(10):
                     
                     try:                            
                            img_response = requests.get(img_url,headers=header,params=params,proxies=proxies,timeout=10)
                            list_light(ulist,u)
                            if img_response.status_code==200:
                                   print(f'当前链接进度{img_number}/{len(img_names)}---{img_names[img_number]}图片大小{round(len(img_response.content)/1000,1)}kb')
                                   hard_size+=round(len(img_response.content)/1000000,3)
                                   
                                   break
                     except:
                            print(u,'重试',rx)
                            if rx>4:
                                   print('失败停止运行,ip可能被拉黑')
                                   os._exit(0)
                     
              
              with open(f'{img_dir}','wb') as fi:
                                          fi.write(img_response.content)
                                          fi.close()
                                          print(f'第{img_count}张图保存!列表中第{st}个链接--{manga_name}--{chapter_name}---{img_names[img_number]} \n')
                                          img_count+=1
                
                    
        
        pool = Pool(args.thread)#线程数
        img_number=range(len(img_names))
        pool.map(imgget,img_number,chunksize=1)      
        st+=1

def color_text(text,front=33,back=40):#自定义文字颜色
              return f'\033[1;{front};{back}m'+text+'\033[0m' 

def list_light(list,light):
    for l in list:
        if l == light:
            if l == list[len(list)-1]:
                print('【'+color_text(l,36)+'】')
            else:
                print('【'+color_text(l,36)+'】',end=',')
        else:
            if l == list[len(list)-1]:
                print(l)
            else:
                print(l,end=',')


def s2hms(s):#秒转时分秒
    h = s//3600
    m = s%3600//60
    s = s-h*3600-m*60
    if not h == 0:
        return '用时{:.0f}小时{:.0f}分钟{:.2f}秒'.format(h,m,s)
    else:
        return '用时{:.0f}分{:.2f}秒'.format(m,s)
    

def get_harddisk_size(d):#参数为盘符，如d='d'或d='d:'
    dd =d
    if ':' not in d:
         dd+=':'
    gb = 1024 ** 3 #GB == gigabytemb
    mb =  1024 ** 2
    total_b, used_b, free_b = shutil.disk_usage(dd) #查看磁盘的使用情况mb
    return print('{}盘总容量{:.0f}MB，已使用{:.0f}MB,剩余{:.0f}MB({:.2%})'.format(d[0],total_b/mb,used_b/mb,free_b/mb,free_b/total_b))
if __name__ == '__main__':
    img_count = 1 #图片计数
    hard_size = 0#占用硬盘空间统计
    t1 = time.time()
    ulist = args.number.split(',')##需要爬取的漫画编号
    with open('d:/manga_command.txt','a',encoding='utf-8') as fmc:
          fmc.write(args.number+'\n')
    for u in ulist:
       url='https://www.manhuagui.com/comic/'+str(u)
       get_comic(url,0)
    t2 =time.time()
    t=t2-t1
    print('\n\n\n\n')
    print('\t\t\t统计报告')
    print(f'本次{s2hms(t)}({round(t,2)}s),占用硬盘大小{round(hard_size,2)}MB,\n平均速度{round(hard_size/t,2)}MB/s,图片平均大小：{round((hard_size/img_count)*1000,2)}KB')
    get_harddisk_size('d')
    print('\n\n\n\n')
       


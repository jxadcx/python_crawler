from multiprocessing.dummy import Pool
import requests
from lxml import etree
import time

def main():
        
        header = {
   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}
        x=2
        while x<99:
                start = time.time()
                url1 = 'https://www.woyaogexing.com/touxiang/'+f'index_{x}.html'#目标网址
                r1 = requests.get(url1,headers=header)
                print('页面响应吗',r1.status_code)#判断页面能否访问200ok,403就该换ip了
                eh = etree.HTML(r1.text)
                all_imgurl = eh.xpath('/html/body/div[3]/div[2]/div[1]/div[2]/div/a[1]/img/@src')#提取图片链接,需要你自己复制源码中的xpath路径
                img_quantity = len(all_imgurl)
                print('图片数量',img_quantity)
                pool = Pool(20)#线程数,可随意设置
                def imgget(z):
                        
                        time1 = time.time()
                        url2 = 'https:'+all_imgurl[z]
                        r2 = requests.get(url2)
                        #print('图片响应码',r2.status_code)
                        with open(f'D:/downloads/1/{z}-{time1}.png','wb') as f:
                                f.write(r2.content)
                        
                zz = range(img_quantity)#这里传参到函数内
                result = pool.map(imgget,zz)
                end = time.time()
                t = round(end-start,2)

                print(f'用时{t}秒，爬取了{img_quantity}张图')
                x+=1
main()
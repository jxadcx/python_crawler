from lxml import etree
import time
import requests
import re
def main1():#单个页面
    url0 = 'https://www.kylc.com/stats/global/yearly_overview/g_gdp_growth.html'#这里是漫画地址
    response0 = requests.get(url0, )
    ym0 = response0.text
    #print(ym0)
    print('页面代码:',response0.status_code)
    eh =  etree.HTML(ym0)
    levels = eh.xpath('/html/body/div[2]/div[1]/div[5]/div[1]/div[2]/div/div[2]/div/table/thead/tr/th[1]/text()')#排名

    country = eh.xpath('/html/body/div[2]/div[1]/div[5]/div[1]/div[2]/div/div[2]/div/table/thead/tr/th[2]/text()')#国家

    years = eh.xpath('/html/body/div[2]/div[1]/div[5]/div[1]/div[2]/div/div[2]/div/table/thead/tr/th[4]/text()')#年份

    gdp_growth_rate = eh.xpath('/html/body/div[2]/div[1]/div[5]/div[1]/div[2]/div/div[2]/div/table/thead/tr/th[5]/text()')#gdp增长率

    title = f'{levels[0]} {country[0]} {gdp_growth_rate[0]}'
    print(title)
    with open('d:/p1.txt','a') as f:
        f.write(title+'\n')
        f.close()

    x = 1
    while x<236:
        try:
            levels = eh.xpath(f'/html/body/div[2]/div[1]/div[5]/div[1]/div[2]/div/div[2]/div/table/tbody/tr[{x}]/td[1]/text()')#获取标题
            country = eh.xpath(f'/html/body/div[2]/div[1]/div[5]/div[1]/div[2]/div/div[2]/div/table/tbody/tr[{x}]/td[2]/text()')#国家
            years = eh.xpath(f'/html/body/div[2]/div[1]/div[5]/div[1]/div[2]/div/div[2]/div/table/tbody/tr[{x}]/td[4]/text()')#年份
            gdp_growth_rate = eh.xpath(f'/html/body/div[2]/div[1]/div[5]/div[1]/div[2]/div/div[2]/div/table/tbody/tr[{x}]/td[5]/text()')#gdp增长率

            title = f'{levels[0]} {country[0]} {gdp_growth_rate[0]}'
            print(title)
            with open('d:/p1.txt','a') as f:
                f.write(title+'\n')
                f.close()
        except:
            print('跳过')
        x+=1


def main2():#多个页面_各国每年人均gdp
    url0 = 'https://www.kylc.com/stats/global/yearly_overview/g_gdp_per_capita.html'#网址
    response0 = requests.get(url0)
    ym0 = response0.text
    #print(ym0)
    print('页面代码:',response0.status_code)
    eh =  etree.HTML(ym0)
    with open('d:/p3.txt','a') as f:
                f.write('年份 ')
                f.close()

    c=1
    all_country = []#所有国家列表
    while c<222:
        try:
            country = eh.xpath(f'/html/body/div[2]/div[1]/div[5]/div[1]/div[2]/div/div[2]/div/table/tbody/tr[{c}]/td[2]/text()')#国家
            gdp_per_capita = eh.xpath('/html/body/div[2]/div[1]/div[5]/div[1]/div[2]/div/div[2]/div/table/thead/tr/th[5]/text()')#人均gdp
            all_country.append(country[0])#写入列表
            #print(country,end = ' ')
            with open('d:/p3.txt','a') as f:
                f.write(country[0]+' ')
                f.close()
            
        except:
                print('跳过1',end=' ')
        c+=1
    print(all_country)
    y = 1960
    
    while y<1976:
        url1 = f'https://www.kylc.com/stats/global/yearly/g_gdp_per_capita/{y}.html'#网址
        response1 = requests.get(url1)
        ym1 = response1.text
        print(url1,'页面代码:',response0.status_code)
        eh =  etree.HTML(ym1)
        x = 1
        c_g = {}
        while x<=222:
            
            try:
                country = eh.xpath(f'/html/body/div[2]/div[1]/div[5]/div[1]/div/div/div/table/tbody/tr[{x}]/td[2]/text()')#国家
            
                gdp_per_capita = eh.xpath(f'/html/body/div[2]/div[1]/div[5]/div[1]/div/div/div/table/tbody/tr[{x}]/td[4]/text()')#人均gdp
                
                c_g[country[0]]=gdp_per_capita[0]#国家对应gdp的字典
                
            except:
                print('跳过2',end=' ')
            x+=1
        gdp = ''
        x1 = 0
        while x1<=len(all_country):
             try:
                if c_g.get(all_country[x1]) ==None:#判断国家当年有无数据
                           gdp+='xxx '
                if '万' in c_g.get(all_country[x1]):#判断数据中是否含有'万' 提取括号内的纯数字
                     gdpwan = c_g.get(all_country[x1])
                     gdp1 = re.findall('\((.*?)\)',gdpwan)
                     gdp2 = gdp1[0].replace(',','')
                     gdp+=gdp2+' '  
                else:         
                    gdp += c_g.get(all_country[x1])+' '
             except:
                  print('跳过3',end='-')
             x1+=1
        print(gdp)
        with open('d:/p3.txt','a') as f:
                    f.write('\n'+str(y)+' '+gdp)
                    f.close()
        y+=1



main2()
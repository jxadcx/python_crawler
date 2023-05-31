import requests
from lxml import etree
from bs4 import BeautifulSoup
url='https://top.baidu.com/board?tab=realtime&sa=fyb_realtime_31065'
response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')
hot_words = soup.find_all('div',class_='c-single-text-ellipsis')
values = soup.find_all('div',class_='hot-index_1Bl1a')
count = len(values)
for c in range(count):
    print(f'{c+1} {hot_words[c].get_text()} {values[c].get_text()}')

    
    
    


# html = etree.HTML(response.text)
# c1 = html.xpath('string(/html/body/div/div/main/div[2]/div/div[2]/div[5])')
# print(c1)
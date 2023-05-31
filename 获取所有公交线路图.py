import requests
from lxml import etree
from PIL import Image, ImageDraw, ImageFont


def getstation_names(url):
    url = "https://m.icauto.com.cn"+url
    response = requests.get(url)
    html = response.text
    selector = etree.HTML(html)

    # 使用xpath提取内容
    content = selector.xpath('//table[@class="bordered"]/tr/td/text()')
    # 用列表推导式过滤掉包含数字或'站序'的元素
    station_names = [elem for elem in content if not any(char.isdigit() for char in elem) and '站序' not in elem and '站名' not in elem]

    #打印站名
 
    print(station_names)
    # 创建一张图片
    img = Image.new('RGB', (1500, 1500), color = (255, 255, 255))

    # 在图片上绘制文本
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('SIMLI.TTF', 30)
    y = 15
    # 将所有站名按照格式连接成一行字符串
    station_names_str = '->'.join(station_names)
  
    
    return station_names_str



url = "https://m.icauto.com.cn/chuxing/bus_511100.html"
response = requests.get(url)
html = response.text
selector = etree.HTML(html)

# 使用xpath提取内容
url_end= selector.xpath('/html/body/div[3]/div[2]/table/tbody/tr/td[4]/a/@href')
hours_of_operation = selector.xpath('/html/body/div[3]/div[2]/table/tbody/tr/td[3]/text()')
route = selector.xpath('/html/body/div[3]/div[2]/table/tbody/tr/td[2]/text()')
bus_line = selector.xpath('/html/body/div[3]/div[2]/table/tbody/tr/td[1]/text()')
# 使用列表推导式将hours_of_operation列表每个元素中的':,'替换成':'
hours_of_operation = [elem.replace(':，',':') for elem in hours_of_operation]


img = Image.new('RGB', (3500, 14500), color = (255, 255, 255))#创建图片
z = len(url_end)
x=0
y=20
while x<z:
    station=getstation_names(url_end[x])
    title=bus_line[x]+'---'+route[x]+'---'+hours_of_operation[x]
    print(title)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('SIMLI.TTF', 20)
    draw.text((20, y), title, font=font, fill=(255, 0, 0))
    draw.text((20, y+20), station, font=font, fill=(0, 0, 0))
    x+=1
    y+=60


img.show()
img.save('D:/乐山市公交路线图.jpg')




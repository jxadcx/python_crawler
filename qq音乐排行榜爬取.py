import requests
from bs4 import BeautifulSoup
def qq_music_ranklist(save_path=None):
    #save_path为保存文件及路径名
    print('''
    流行指数榜:4,飙升榜62,热歌榜26,听歌识曲榜67,...
    ''')
    list_number=input('请输入:')
    url = 'https://y.qq.com/n/ryqq/toplist/'+str(list_number)
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    toplist__tit=soup.find('h1',class_='toplist__tit')#榜单名
    toplist_switch__data = soup.find('span',class_='toplist_switch__data')#日期
    print(toplist__tit.string,toplist_switch__data.string)

    songlist__list=soup.find('ul',class_='songlist__list')#排行榜区域


    songlist__number = songlist__list.find_all('div',class_='songlist__number')#排名
    songlist__rank = songlist__list.find_all('div',class_='songlist__rank')#涨幅
    song_list=songlist__list.find_all('span',class_='songlist__songname_txt')#歌名
    songlist__artist = soup.find_all('div',class_='songlist__artist')#歌手

    class1 = f"排名---涨幅---音乐---歌手"
    print(class1)
    if save_path:
        f = open(save_path,'w',encoding='utf-8')
        f.write(class1+'\n')
    for number_div,rank_div,music_span,artist_div in zip(songlist__number,songlist__rank,song_list,songlist__artist):
        number = number_div.string
        rank = rank_div.get_text() if rank_div.get_text() != '' else '无'
        if rank !='无':
            if rank_div.find('i',class_='icon_rank_up'):
                rank+='↑'
            if rank_div.find('i',class_='icon_rank_down'):
                rank+='↓'
        if rank_div.find('i',class_='icon_rank_new'):
            rank='new'

        music_a= music_span.find_all('a')[1]
        music = music_a.get('title')
        artist = artist_div.get_text()
        class2 = f"{number}---{rank}---{music}---{artist}"
        print(class2)
        if save_path:
            f=open(save_path,'a',encoding='utf-8')
            f.write(class2+'\n')

qq_music_ranklist()

#qq_music_ranklist('d:/music_list.txt')#保存结果
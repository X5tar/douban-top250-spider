import os

import requests
from bs4 import BeautifulSoup


def get_item(soup):
    # 获取该页第一个电影信息
    for item in soup.find_all('li'):
        if item.img:
            return item


def mkdir(item, i):
    # 创建该电影的文件夹
    path = os.getcwd()
    path = os.path.join(path, '豆瓣Top250')
    path = os.path.join(path, str(i) + '-' + item.span.string)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_txt(item, path, headers):
    # 获取电影详情页
    txt_path = os.path.join(path, '电影信息.txt')
    info_url = item.a['href']
    info_page = requests.get(info_url, headers=headers)
    info_soup = BeautifulSoup(info_page.text, 'html.parser')

    # 获取电影名
    txt = info_soup.find('span', {'property': 'v:itemreviewed'}).string + '\n'

    # 获取 info 块
    info = info_soup.find('div', id='info')
    txt += info.text.replace('链接', '编码') + '\n'

    # 获取剧情简介
    txt += '剧情简介：\n'
    if info_soup.find('span', {'class': ['all', 'hidden']}):
        for i in info_soup.find('span', {'class': ['all', 'hidden']}).strings:
            txt += ' ' * 4 + i.strip() + '\n'
    else:
        for i in info_soup.find('span', {'property': 'v:summary'}).strings:
            txt += ' ' * 4 + i.strip() + '\n'

    with open(txt_path, 'w') as f:
        f.write(txt)


def get_img(item, path):
    # 获取海报图片
    img_url = item.img['src']
    img_name = item.img['src'][item.img['src'].rfind('/') + 1:]
    img_path = os.path.join(path, img_name)
    img = requests.get(img_url).content
    with open(img_path, 'wb') as f:
        f.write(img)


def main():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    for i in range(0, 250):
        print('第%03d个电影获取中...' % (i + 1), end='')
        r = requests.get('https://movie.douban.com/top250?start={}&filter='.format(i), headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        item = get_item(soup)
        path = mkdir(item, i + 1)
        get_txt(item, path, headers)
        get_img(item, path)
        print('\r第%03d个电影已获取完成 ' % (i + 1))
    print('豆瓣 Top250 全部获取完成')


if __name__ == '__main__':
    main()

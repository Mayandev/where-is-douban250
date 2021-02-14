import re
import requests
import csv
import lxml.html

DOWNLOAD_URL = 'https://movie.douban.com/top250'


def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    }).text


def parse_html(html, writer, movies_info):
    tree = lxml.html.fromstring(html)
    movies = tree.xpath("//ol[@class='grid_view']/li")
    for movie in movies:
        name_num = len(movie.xpath("descendant::span[@class='title']"))
        name = ''
        for num in range(0, name_num):
            name += movie.xpath("descendant::span[@class='title']")[
                                num].text.strip()
        # 获取中文名
        name = name.replace('/', '').split()[0]
        # 排名，豆瓣页面
        num = movie.xpath("descendant::em/text()")[0]
        url = movie.xpath("descendant::div[@class='pic']/a/@href")[0]
        # 可播放的 url
        detail_html = download_page(url)
        enable_urls = lxml.html.fromstring(
            detail_html).xpath("//a[@class='playBtn']/@href")
        # 格式化 url
        format_url = []
        for enable_url in enable_urls:
            format_url.append(enable_url.split("?url=")[1])
        enable_urls = ";".join(format_url)
        # 年份，国家，类型
        data = movie.xpath(
            "descendant::div[@class='bd']/p")[0].xpath('string(.)')
        info = re.findall(r'\d.*', data)[0].split('/')
        year, country, category = info[0].strip(
        ), info[1].strip(), info[2].strip()
        category = ";".join(category.split(" "))
        # 得分，评分数
        score = movie.xpath("descendant::div[@class='star']/span")[1].text
        voting_num = movie.xpath("descendant::div[@class='star']/span")[3].text

        quote = movie.xpath("descendant::div[@class='bd']/p[2]/span")
        movie_info = (int(num), name, float(score), country, year,
                      category, int(voting_num[0:-3]), quote, url, enable_urls)
        movies_info.append(movie_info)
        print(movie_info)
        writer.writerow(movie_info)
    try:
        next_page = tree.xpath("//span[@class='next']/a/@href")[0]
        return DOWNLOAD_URL + next_page
    except:
        return None
       


def main():
    url = DOWNLOAD_URL
    # 将数据导入到csv文件中
    writer = csv.writer(open('175.csv', 'w', newline='', encoding='utf-8'))
    fields = ('rank',  'name', 'score', 'country', 'year', 'category', 'votes', 'quote', 'douban_url', 'enable_urls')
    writer.writerow(fields)
    movies_info = []
    while url:
        html = download_page(url)
        url = parse_html(html, writer, movies_info)

if __name__ == '__main__':
    main()

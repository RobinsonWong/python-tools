from unicodedata import category
import requests
from lxml import etree
import time
import codecs

typeDic = {'S': 'by_score', 'T': 'by_default', 'R': 'by_publication_date'}

def get_sorttype(type):
    return typeDic[type];

def get_books(url, category, sort_type, max_page_count):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0', 
        #'Content-Type': 'text/html; charset=utf-8'
    }

    start = 0
    with open('out/douban_top_' + category +'_books_' + get_sorttype(sort_type) + '.csv', 'w', encoding='utf_8_sig') as file:
        # `utf_8_sig` utf8 without bom
        file.write('No.,Name,Publication,Rate\n')
        startNum = 0
        itemNum = 0
        for page_idx in range(1, max_page_count + 1):
            startNum = (page_idx - 1) * 20
            param = "?start=" + str(startNum) + "&type=" + sort_type
            time.sleep(2)
            r = requests.get(url + param, headers=headers);
            # r.encoding = r.apparent_encoding;
            # print(r.text)
            # print("status.code=", r.status_code)
            html = etree.HTML(r.text)
            infos = html.xpath('//li[@class="subject-item"]//div[@class="info"]')
            print("page_index=" + str(page_idx) + ", item.lenth=" + str(len(infos)) + ", category=" + category + ", url=" + (url+param))
            for item_idx, info in enumerate(infos):
                try:
                    itemNum = (item_idx + 1) + (page_idx - 1) * 20;
                    title = info.xpath('h2/a/text()')[0].strip()
                    pub = info.xpath('div[@class="pub"]/text()')[0].strip()
                    rate = info.xpath('div[@class="star clearfix"]/span[@class="rating_nums"]/text()')[0]
                    file.write(str(itemNum) + "," + title + "," + pub + "," + rate + "\n")
                except IndexError as e:
                    print("IndexEror exception: item_idx=" + str(item_idx) + ", title=" + title);
                    file.write(str(itemNum) + "," + title + "," + "," + "\n")


if __name__ == "__main__":
    csTagName = '%E7%BC%96%E7%A8%8B'   # 编程
    #get_books("https://book.douban.com/tag/" + csTagName, 'programming', 'S', 50)   # 分数排序
    #get_books("https://book.douban.com/tag/" + csTagName, 'programming', 'R', 50)   # 出版日期
    #get_books("https://book.douban.com/tag/" + csTagName, 'programming', 'T', 50)    # 综合排序
    #
    get_books("https://book.douban.com/tag/" + '%E5%B0%8F%E8%AF%B4', 'novel', 'S', 50) 





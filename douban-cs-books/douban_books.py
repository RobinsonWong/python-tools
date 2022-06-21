import requests
from lxml import etree

def get_books(url, maxPageCount):
    start = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0', 
        #'Content-Type': 'text/html; charset=utf-8'
    }

    with open('out/books.csv', 'w', encoding='utf-8') as file:
        file.write('No.,Name,Publication,Rate\n')
        startNum = 0
        itemNum = 0
        for page_idx in range(1, maxPageCount):
            startNum = (page_idx - 1) * 20
            param = "?start=" + str(startNum) + "&type=S"
            r = requests.get(url + param, headers=headers);
            # r.encoding = r.apparent_encoding;
            html = etree.HTML(r.text)
            infos = html.xpath('//li[@class="subject-item"]//div[@class="info"]')
            print("page_index=" + str(page_idx) + ", item.lenth=" + str(len(infos)) + ", url.param=" + param)
            for item_idx, info in enumerate(infos):
                title = info.xpath('h2/a/text()')[0].strip()
                pub = info.xpath('div[@class="pub"]/text()')[0].strip()
                rate = info.xpath('div[@class="star clearfix"]/span[@class="rating_nums"]/text()')[0]
                itemNum = (item_idx + 1) + (page_idx - 1) * 20;
                file.write(str(itemNum) + "," + title + "," + pub + "," + rate + "\n")
            # print(r.text)
            # print("status.code=", r.status_code)


if __name__ == "__main__":
    get_books("https://book.douban.com/tag/%E7%BC%96%E7%A8%8B", 100)




import json
from lxml import etree

import requests


#获取网页源码
def request_dandan(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


#使用正则表达式解析获取想要的关键信息
def parse_html(html):
    tree = etree.HTML(html)
    #准备一个空列表
    li = []
    for i in range(20):
        dic = {}
        num = tree.xpath('//li/div[@class="list_num red" or @class="list_num "]/text()')[i]
        name = tree.xpath('//li/div[@class="name"]/a/text()')[i]
        recommend = tree.xpath('//li/div[@class="star"]/a/text()')[i]
        recommend1 = tree.xpath('//li/div[@class="star"]/span/text()')[i]
        price = tree.xpath('//li/div[@class="price"]//span[@class="price_n"]/text()')[i]
        publisher = tree.xpath('//li//div[6]/a/text()')[i]

        #更新字典内容
        dic.update({'num': num,
                    'name': name,
                    'recommend': recommend + recommend1,
                    'price': price,
                    'publisher': publisher})
        #将字典作为元素写入列表
        li.append(dic)
    return li

# 将数据写入文件
def data_write(li):
    print(f'开始写入第{page}页数据...')
    for i in range(len(li)):
        #这里需要使用追加写入模式a,否则后面写入的数据会覆盖前面的
        with open('book1.json', mode='a', encoding='utf-8') as f:
            f.write(json.dumps(li[i], ensure_ascii=False) + ',')

#使用page来实现翻页爬取
def main(page):
    #根据翻页网址变化灵活拼接
    url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
    #获取网页源代码
    html = request_dandan(url)
    #使用xpath解析源码拿到数据
    li = parse_html(html)
    data_write(li)

if __name__ == '__main__':
    # 每一页20条数据，通过循环获取前200条数据
    for page in range(1, 11):
        main(page)

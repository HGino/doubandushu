import json
import requests
import re
from requests.exceptions import RequestException


def get_one(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except  RequestException:
        return None


def parse_one(html):
    pattern = re.compile('table.*?i:\'(.*?)\'.*?</a>.*?div.*?href="(.*?)"title='+
                         '"(.*?)"</a>.*?<p\s+class="pl">(.*?)\s+/</p>'+
                        '"rating_nums">(.*?)</span>.*?<p.*?"inq">(.*?)</span>', re.S) 
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index' : items[0],
            'website' : items[1],
            'name' : items[2],
            'writer' : items[3],
            'score' : items[4],
            'a sentence' : items[5]
        }


def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')


def main(page):
    url = 'https://book.douban.com/top250?start=' + str((int(page)-1) * 25)
    html = get_one(url)
    for item in parse_one(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(i)
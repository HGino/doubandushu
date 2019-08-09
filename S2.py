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
    except RequestException:
        return None


def parse_one(html):
    pattern = re.compile(
        'pl2.*?a.?href="(.*?)".*?title="(.*?)".*?</a>.*?pl.?>(.*?)</p>.*?rating_nums.?>(.*?)</span>', re.S
    )
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'i1' : item[0],
            'i2' : item[1],
            'i3' : item[2],
            'i4' : item[3],
            'i5' : '\n'
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')


def main(page):
    url = 'https://book.douban.com/top250?start=' + str((int(page)-1) * 25)
    html = get_one(url)
    for item in parse_one(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(1,11):
        main(i)

#!/usr/bin/env python3
# coding=UTF-8

# 功能:在命令行中查询单词在有道词典网页版中的柯林斯释义
# 使用方法: `python3 dict.py word`
# 或 `alias di='python3 dict.py'` ,然后就可以直接 `di word` 查询单词了

import requests
from bs4 import BeautifulSoup
import re
import sys


# result = {
#     "query": word,
#     "collinsResult": [
#         {
#             "usage": "ADVERB USES",
#             "word": "word",
#             "spell": "/aʊt/",
#             "star": "star5",
#             "rank": "CET4 TEM4",
#             "additional_pattern": "(outing,outed,outs)",
#             "definition": [
#                 {
#                     "additional": "VERB",
#                     "trans": "When something is in a particu",
#                     "additional2": "[ADV after v]",
#                     "exampleLists": [
#                         {
#                             "examples_en": "I like the pop you",
#                             "examples_zh": "我喜欢你拔出瓶塞时弄出的那“砰”的一声。"
#                         },
#                         {
#                             "examples_en": "He took out his flipped the pages.",
#                             "examples_zh": "他拿出了笔记本，快速地翻着页。"
#                         }
#                     ]
#                 }
#             ]
#         }
#     ]
# }

def dim(w):
    return f'\033[2m{w}\033[0m'


def bright(w):
    return f'\033[1m{w}\033[0m'


def red(w):
    return f'\033[31m{w}\033[0m'


def green(w):
    return f'\033[32m{w}\033[0m'


def greenb(w):
    return f'\033[1;42m{w}\033[0m'


def yellow(w):
    return f'\033[33m{w}\033[0m'


def blue(w):
    return f'\033[34m{w}\033[0m'


def magenta(w):
    return f'\033[35m{w}\033[0m'


def cyan(w):
    return f'\033[36m{w}\033[0m'


def blueb(w):
    return f'\033[44m{w}\033[0m'


class Youdao:
    def __init__(self, word):
        self.word = word
        self.result = {'query': word}
        url = f'http://dict.youdao.com/w/{word}/#keyfrom=dict2.top'
        pagedata = requests.get(url)
        soup = BeautifulSoup(pagedata.text, 'lxml')
        self.page_source = soup.find(id='collinsResult')

    def parse(self):
        self.result['collinsResult'] = []
        try:
            wt_container = self.page_source.find('div', attrs={'class': ['collinsToggle', 'trans-container']}).find_all(
                'div', class_='wt-container')
        except AttributeError:
            return self.result

        for container in wt_container:
            item = {}
            # 用法
            try:
                item['usage'] = container.find('div', id=re.compile('^COLNAMING\d+')).span.text
                naming = container.find('div', id=re.compile('^NAMING\d+'))
            except AttributeError:
                item['usage'] = None
                naming = container
            # 显示的单词, 音标, 星级, 考试类型, 变形
            # 单词
            item['word'] = naming.h4.find('span', class_='title').text
            # 音标
            try:
                item['spell'] = naming.h4.em.text
            except AttributeError:
                item['spell'] = None
            # 星级
            try:
                item['star'] = naming.h4.find('span', title='使用频率').get('class')[-1]
            except AttributeError:
                item['star'] = None
            # 考试类型
            try:
                item['rank'] = naming.h4.find('span', class_='via rank').text
            except AttributeError:
                item['rank'] = None
            # 变形
            try:
                additional_pattern = naming.h4.find('span',
                                                    attrs={'class': ['additional', 'pattern']}).text
                item['additional_pattern'] = re.sub('\s+', ' ', additional_pattern)
            except AttributeError:
                item['additional_pattern'] = None
            # 释义
            item['definition'] = []
            info = naming.find_all('ul')
            if not info:
                print('llllllllllllllllllllllll')
                definition = dict()
                definition['order'] = None
                definition['additional'] = None
                naming.h4.extract()
                trans = naming
                trans = re.sub('\s+', ' ', str(trans))
                trans = re.sub('\s*</?div.*?>\s*', '', trans)
                trans = re.sub('<a.*?>', '\033[32m', trans)
                trans = re.sub('</a>', '\033[0m', trans)
                trans = re.sub('→\s*', '→ ', trans)
                definition['trans'] = trans
                definition['additional2'] = None
                definition['exampleLists'] = []
                item['definition'].append(definition)
                self.result['collinsResult'].append(item)
                return self.result
            for d in naming.find_all('ul')[-1].find_all('li'):
                definition = dict()
                # 第几条解释
                definition['order'] = d.find('span', class_='collinsOrder').text.strip()
                # 词性
                try:
                    additional = d.find('span', attrs={'class': 'additional', 'title': True}).text
                    definition['additional'] = additional
                except AttributeError:
                    definition['additional'] = None
                # 英文释义
                trans = d.find('div', class_='collinsMajorTrans').p
                trans = re.sub('\s+', ' ', str(trans))
                trans = re.sub('<span class.*?</span>', '', trans)
                trans = re.sub('\s*</?p>\s*', '', trans)
                trans = re.sub('<b>', '\033[32m', trans)
                trans = re.sub('</b>', '\033[0m', trans)
                trans = re.sub('<a.*?>', '\033[32m', trans)
                trans = re.sub('</a>', '\033[0m', trans)
                trans = re.sub('→\s*', '→ ', trans)
                # print(trans)
                definition['trans'] = trans
                # 翻译后面的词性
                try:
                    additional2 = d.find_all('span', attrs={'class': 'additional', 'title': False})
                    definition['additional2'] = ''.join([a.text.strip() for a in additional2])
                except AttributeError:
                    definition['additional2'] = None
                # 释义下面的例句
                definition['exampleLists'] = []
                for ex in d.find_all('div', class_='exampleLists'):
                    e = dict()
                    # 例句英文
                    e['examples_en'] = ex.div.find_all('p')[0].text.strip()
                    # 例句英文
                    e['examples_zh'] = ex.div.find_all('p')[1].text.strip()
                    definition['exampleLists'].append(e)
                item['definition'].append(definition)
            self.result['collinsResult'].append(item)
        return self.result

    def prettyprint(self):
        # print(red(self.result['query']))
        if not self.result['collinsResult']:
            print('no collins result')
            return
        for r in self.result['collinsResult']:
            if r['usage'] is not None:
                print(greenb(r['usage']))
            print(bright(r['word']), end=' ')
            if r['spell'] is not None:
                print(r['spell'], end=' ')
            else:
                pass
            if r['star'] is not None:
                print(yellow(r['star']), end=' ')
            if r['rank'] is not None:
                print(blue(r['rank']), end=' ')
            if r['additional_pattern'] is not None:
                print(dim(r['additional_pattern']), end='')
            print()
            for d in r['definition']:
                # 打印英文释义
                # 打印释义序号
                if d['order'] is not None:
                    print(yellow(d['order']), end='')
                # 打印该条释义中的词性
                if d['additional'] is not None:
                    print(cyan(d['additional']), end=' ')
                # 打印英文释义
                print(d['trans'], end='')
                # 打印释义后面的词性
                if d['additional2'] is not None:
                    print(' ' + dim(d['additional2']), end=' ')
                print()

                # 打印例句
                for e in d['exampleLists']:
                    print('    ' + magenta('eg.'), end=' ')
                    print(dim(e['examples_en']))
                    print(dim('        ') + dim(e['examples_zh']))


if __name__ == '__main__':
    word = sys.argv[1]
    # word = 'hi'
    yd = Youdao(word)
    result = yd.parse()
    yd.prettyprint()

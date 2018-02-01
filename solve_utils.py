#!/usr/bin/python
# -*- coding: utf-8 -*-
import webbrowser
import sys
import requests
import re

if sys.version_info.major == 2:
    import urllib as ul
elif sys.version_info.major == 3:
    from urllib import parse as ul
else:
    raise RuntimeError('Unknown python version')

s = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}


# 直接用浏览器打开问题
def open_webpage(question):
    webbrowser.open('https://baidu.com/s?wd=' + ul.quote(question.encode(sys.stdout.encoding)))


# 根据问题搜索结果计算每个选项出现的次数
def words_count(question, answers):
    search_page = s.get(url='https://www.baidu.com/s', params={'wd': question}, headers=headers)
    return [search_page.text.count(answer) for answer in answers]


# 计算问题＋每个选项搜索的结果数
def search_count(question, answers):
    counts = []
    for answer in answers:
        search_page = s.get(url='https://www.baidu.com/s', params={'wd': question + "%20" + answer}, headers=headers)
        m = re.search(u'百度为您找到相关结果约((\d+,)*\d+)个', search_page.text)
        counts.append(int(m.groups()[0].replace(',', '')) if m is not None else 0)
    return counts

# 找到最符合的
def find_max_index(counts):
    return counts.index(max(counts))


# 找到最不符合的
def find_min_index(counts):
    return counts.index(min(counts))


# 判断结果是否重复
def has_repeat(counts, num):
    return counts.count(counts[num])

# 找到最符合的
def find_max_index2(counts, counts2):
    the_max = max(counts)
    #如果有多个相同的最大值，传入这几个最大值对应的第二组参数
    max_list = []
    #第二组参数的原始index
    max_index_list = []

    index = 0
    for count in counts:
        if count == the_max:
            max_list.append(counts2[index])
            max_index_list.append(index)
        index += 1

    if len(max_list) > 1:
        second_index = find_max_index(max_list)
        return max_index_list[second_index]
    else :
        return counts.index(max(counts))

# 找到最不符合的
def find_min_index2(counts, counts2):
    the_min = min(counts)
    #如果有多个相同的最大值，传入这几个最大值对应的第二组参数
    min_list = []
    #第二组参数的原始index
    min_index_list = []

    index = 0
    for count in counts:
        if count == the_min:
            min_list.append(counts2[index])
            min_index_list.append(index)
        index += 1

    if len(min_list) > 1:
        second_index = find_min_index(min_list)
        return min_index_list[second_index]
    else :
        return counts.index(min(counts))

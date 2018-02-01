#!/usr/bin/python
# -*- coding: utf-8 -*-

import http_utils
import json
import time
import config
import solve_utils
import problem_utils
import re
import urllib2

result_set = set([])

#判断题目是否进行过展示，使用set去重
def isInSet(value):
    return value in result_set

#判断题干是否有某词，且这个词不在书名号，引号内
def hasWordInQuestion(question, word):
    #题干是否包含某词
    hasWord = (question.find(word) != -1)

    #对书名号，引号等做处理
    if hasWord: 
        rule = u'(.*)?《(.*)?%s(.*)?》(.*)?' % word
        matched = re.match(rule, question)
        if matched is not None:
            hasWord = False

        rule = u'(.*)?“(.*)?%s(.*)?”(.*)?' % word
        matched = re.match(rule, question)
        if matched is not None:
            hasWord = False

        rule = u'(.*)?"(.*)?%s(.*)?"(.*)?' % word
        matched = re.match(rule, question)
        if matched is not None:
            hasWord = False

        rule = u'(.*)?【(.*)?%s(.*)?】(.*)?' % word
        matched = re.match(rule, question)
        if matched is not None:
            hasWord = False

        rule = u'(.*)?「(.*)?%s(.*)?」(.*)?' % word
        matched = re.match(rule, question)
        if matched is not None:
            hasWord = False

        rule = u'(.*)?『(.*)?%s(.*)?』(.*)?' % word
        matched = re.match(rule, question)
        if matched is not None:
            hasWord = False
    return hasWord

#判断题干是否为包含否定词
def isOpposite(question):

    is_opposite = (hasWordInQuestion(question, u'不') or hasWordInQuestion(question, u'没') or hasWordInQuestion(question, u'无') or hasWordInQuestion(question, u'错'))

    # 排除特殊词语
    if (question.find(u'不丹') or question.find(u'不错') or question.find(u'没错') or question.find(u'无锡')):
        is_opposite = False
    return is_opposite

#百度搜索词频，结果数判断
def baiduSearch(question, answers, is_opposite):
    # 两种方式进行判断
    words_count = solve_utils.words_count(question, answers)
    search_count = solve_utils.search_count(question, answers)
    print(u'%-15s' * 3 % (u'', u'词频', u'结果数'))

    words_total_count = 0
    for answer, word_count, search_num in zip(answers, words_count, search_count):
        print(u'%-15s' * 3 % (answer, word_count, search_num))
        words_total_count += word_count

    print "==================="
    # 词频都不为零，则使用词频推荐答案
    if words_total_count > 0:
        if is_opposite:
            select = solve_utils.find_min_index(words_count)
        else:
            select = solve_utils.find_max_index(words_count)
    # 词频都为零，则使用搜索结果数推荐答案
    else:
        if is_opposite:
            select = solve_utils.find_min_index(search_count)
        else:
            select = solve_utils.find_max_index(search_count)
    return select

#解题策略
def AISolve(value):
    json_obj = json.loads(value)

    # 获取题干和选项
    question = json_obj['title']
    answers = json_obj['answers']

    # 打印题干和选项
    print question
    if len(answers) > 0:
        print "A." + answers[0] + "  B." + answers[1] + "  C." + answers[2]
        print "==================="
        print u"分析: " + json_obj['search_infos'][0]['summary']
        print "==================="

        is_opposite = isOpposite(question)
        if is_opposite:
            print u"！！！注意否定！！！"
            print "==================="

        # TODO:第一优先级百度百科

        # 第三优先级百度搜索
        baidu_select = baiduSearch(question, answers, is_opposite)

        print u"2.搜狗汪酱推荐答案：  " + json_obj['recommend']
        print u"3.百度搜索推荐答案：  " + answers[baidu_select]

    print ""
    # print value

#使用搜狗搜索（https://www.sogou.com/）的api自动解答
while(True):
    try:
        for value in http_utils.getAutoValue():
            if not isInSet(value):
                result_set.add(value)
                AISolve(value)
        time.sleep(0.5)
    #网络连接错误1分钟后重试
    except urllib2.URLError, e:
        print e.message
        time.sleep(60)
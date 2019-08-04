#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2019/8/1 0:20 
# @Author : wyao
# @File : config.py

resquest_33xs = {
    'host': 'https://www.33xs.com',
    'get_book_list': {
        'url': 'https://www.33xs.com/search.php?ie=utf-8&keyword={}',
        'method': 'GET'
    },
    'get_book_chapters': {
        'url': 'https://www.33xs.com{}',
        'method': 'GET'
    },
    'get_book_content': {
        'url': 'https://www.33xs.com{}',
        'method': 'GET'
    }
}

request_qb5200 = {
    'host': 'http://www.qb5200.tw',
    'get_book_list': {
        'url': 'https://so.biqusoso.com/s.php?ie=utf-8&siteid=qb5200.tw&q={}',
        'headers': {
            "Host": "so.biqusoso.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
        },
        'method': 'GET'
    },
    'get_book_chapters': {
        'url': '',
        'method': 'GET',
        'encoding': 'gbk'
    },
    'get_book_content': {
        'url': '',
        'method': 'GET',
        'encoding': 'gbk'
    }
}

source = [resquest_33xs, request_qb5200]

threadpool_size = 50

book_dir = '../books/'
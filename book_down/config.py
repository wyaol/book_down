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

threadpool_size = 50

book_dir = '../books/'
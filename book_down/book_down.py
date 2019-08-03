#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2019/8/1 0:21 
# @Author : wyao
# @File : book_down.py
from abc import abstractmethod
import threadpool
from .exceptions import BookNotFoundException
from .html_info import *
from . import config


class BookDown:

    def __init__(self, book_name: str, auther: str=''):
        self.book_name = book_name
        pass

    @abstractmethod
    def get_book_list(self):
        """
        返回书籍信息json列表
        :return list[dict]:
        [
            {
                'book_name': 'xx',
                'url': 'xx',
                'auther': 'xx',
                'breif': 'xx',
                'words_count': xx
            },
            ...
        ]
        """
        pass


    def save_book(self, book: str):
        with open('{}{}.txt'.format(config.book_dir, self.book_name), 'w', encoding='utf-8') as fp:
            fp.write(book)

    @abstractmethod
    def get_book_chapters(self, url: str):
        """
        返回书籍的章节列表
        :return
        [{
            'id': 0,
            'name': 'xx',
            'url': 'xx'
        },...]:
        """
        pass

    @abstractmethod
    def get_book_str(self, chapters: [{}]):
        pass

    @abstractmethod
    def get_chapter(self, chapter_info: dict):
        """
        得到一个章节
        chapter_info = {
            'id': 0,
            'name': 'xx',
            'url': 'xx',
            'content': ''
        }
        :param dict chapter_info:
        {
            'id': 0,
            'name': 'xx',
            'url': 'xx'
        }
        :return None:
        """
        pass

    def down_book(self):
        book_list = self.get_book_list()
        if len(book_list) == 0:
            raise BookNotFoundException('没有搜索到相关书籍')

        book_url = book_list[0]['url']
        chapters = self.get_book_chapters(book_url)
        book = self.get_book_str(chapters)
        self.save_book(book)

    def down_book_from_bok_url(self, book_url: str):
        chapters = self.get_book_chapters(book_url)
        book = self.get_book_str(chapters)
        self.save_book(book)


class BookDown_33xs(BookDown):

    def __init__(self, book_name: str):
        super().__init__(book_name)

    def get_book_list(self):
        return Get_Book_List_HI_33xs(self.book_name).info()

    def get_book_chapters(self, url: str):
        return Get_Book_Chapters_HI_33xs(url).info()

    def get_chapter(self, chapter_info: dict):
        """
        得到一个章节的内容
        :param chapter_info:
        :return None:
        """
        chapter_info['content'] = Get_Book_Content_HI_33xs(chapter_info['url']).info()

    def get_book_str(self, chapters: [{}]):
        """
        获取整本书
        :param chapters:
        :return list[dict]:
        [{
            'id': 0,
            'name': 'xx',
            'url': 'xx'
        },...]
        """
        pool = threadpool.ThreadPool(config.threadpool_size)
        requests = threadpool.makeRequests(self.get_chapter, chapters)
        [pool.putRequest(req) for req in requests]
        pool.wait()

        chapters.sort(key=lambda x:x['id'])

        res = ''
        for each in chapters:
            res += '{}\n{}\n'.format(each['name'], each['content'])

        return res
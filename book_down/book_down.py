#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2019/8/1 0:21 
# @Author : wyao
# @File : book_down.py
import threadpool
from .exceptions import BookNotFoundException
from .html_info import *
from . import config


class BookDown:

    GET_LIST_CLASS = 0
    GET_CHAPTER_CLASS = 1
    GET_CONTENT_CLASS = 2

    def __init__(self, book_name: str, auther: str=''):
        self.book_name = book_name

    @classmethod
    def class_factory_from_url(cls, url: str, class_type: int, **obj_args):
        """
        根据url和类的类型生成对象
        :param url:
        :param class_type:
        :param obj_args: 该对象初始化的额外的参数字典
        :return obj:
        """
        tmp = {
            class_type == cls.GET_LIST_CLASS and config.resquest_33xs['host'] in url: Get_Book_List_HI_33xs(
                obj_args.get('book_name', '')),
            class_type == cls.GET_CHAPTER_CLASS and config.resquest_33xs['host'] in url: Get_Book_Chapters_HI_33xs(
                url),
            class_type == cls.GET_CONTENT_CLASS and config.resquest_33xs['host'] in url: Get_Book_Content_HI_33xs(
                url),

            class_type == cls.GET_LIST_CLASS and config.request_qb5200['host'] in url: Get_Book_List_HI_qb5200(
                obj_args.get('book_name', '')),
            class_type == cls.GET_CHAPTER_CLASS and config.request_qb5200['host'] in url: Get_Book_Chapters_HI_qb5200(
                url),
            class_type == cls.GET_CONTENT_CLASS and config.request_qb5200['host'] in url: Get_Book_Content_HI_qb5200(
                url),
        }
        return tmp[True]

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
        ret = []
        for each in config.source:
            get_list_obj = BookDown.class_factory_from_url(each['host'], BookDown.GET_LIST_CLASS, book_name=self.book_name)
            ret.extend(get_list_obj.info())
        return ret


    def save_book(self, book: str):
        with open('{}{}.txt'.format(config.book_dir, self.book_name), 'w', encoding='utf-8') as fp:
            fp.write(book)

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
        get_chapters_obj = BookDown.class_factory_from_url(url, BookDown.GET_CHAPTER_CLASS)
        return get_chapters_obj.info()

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

        chapters.sort(key=lambda x: x['id'])

        res = ''
        for each in chapters:
            res += '{}\n{}\n\n\n'.format(each['name'], each['content'])

        return res

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
        get_content_obj = BookDown.class_factory_from_url(chapter_info['url'], BookDown.GET_CONTENT_CLASS)
        chapter_info['content'] = get_content_obj.info()

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
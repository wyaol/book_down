#!/usr/bin/env python3 
# -*- coding: utf-8 -*- 
# @Time : 2019/8/1 0:21 
# @Author : wyao
# @File : spider.py
import sys
from abc import abstractmethod
import requests
import re
from bs4 import BeautifulSoup
from . import config

class HtmlInfo:

    session = requests.Session()

    def __init__(self, url: str, method: str, headers: dict={}, data: str='', encoding='utf-8'):
        self.url = url
        self.method = method
        self.headers = headers
        self.data = data
        self.encoding = encoding
        pass

    def get_page(self):
        """
        从远程网页下载HTML
        :return:
        """
        if self.method == 'GET':
            page = HtmlInfo.session.get(self.url, headers=self.headers, verify=False)
        elif self.method == 'POST':
            page = HtmlInfo.session.post(self.url, headers=self.headers, data=self.data, verify=False)
        else:
            raise Exception('method设置不正确， 请检查配置文件 argvs={}   line={} file={}'.format(self.method, sys._getframe().f_lineno, __file__))

        page.encoding = self.encoding

        return page.text

    @abstractmethod
    def soup_to_info(self, soup: BeautifulSoup):
        """
        提取soup中HTML页面中标签内容， 加工成字典列表
        :param soup:
        :return list[dict]: list[dict]
        """
        pass

    def page_to_soup(self, page: str):
        return BeautifulSoup(page, 'lxml')


    def info(self):
        """
        返回
        :return list[dict]: list[dict]
        """
        page = self.get_page()
        soup = self.page_to_soup(page)
        return self.soup_to_info(soup)


class Get_Book_List_HI_33xs(HtmlInfo):

    def __init__(self, name: str):
        self.name = name
        super().__init__(
            config.resquest_33xs['get_book_list']['url'].format(name),
            config.resquest_33xs['get_book_list']['method'])
        pass

    def soup_to_info(self, soup: BeautifulSoup):
        soup_list = soup.select('.result-game-item-detail')

        info = []

        for each in soup_list:
            item = {
                'book_name': each.select_one('h3 a').get('title'),
                'url': ('{}{}').format(config.resquest_33xs['host'], each.select_one('h3 a').get('href')),
                'auther': '',
                'breif': each.select_one('.result-game-item-desc').text,
                'words_count': -1
            }
            if self.name in item['book_name']:
                info.append(item)

        return info


class Get_Book_Chapters_HI_33xs(HtmlInfo):

    def __init__(self, url: str):
        super().__init__(url, config.resquest_33xs['get_book_chapters']['method'])

    def _get_id_from_url(self, url):
        pattern = '.*/(.*?)\.'
        res = re.findall(pattern, url)
        if len(res) == 0: raise Exception('正则不匹配 该章节url异常 argvs={}   line={} file={}'.format(self.method, sys._getframe().f_lineno, __file__))
        return int(res[0])

    def soup_to_info(self, soup: BeautifulSoup):
        soup_list = soup.select('#list dd')
        info = []
        tmp_list = []

        for each in soup_list:
            url = '{}{}'.format(config.resquest_33xs['host'], each.select_one('a').get('href'))
            id = self._get_id_from_url(url)
            item = {
                'id': id,
                'name': each.select_one('a').text.strip(),
                'url': url
            }
            if url not in tmp_list:
                info.append(item)
                tmp_list.append(url)

        return info


class Get_Book_Content_HI_33xs(HtmlInfo):

    def __init__(self, url: str):
        super().__init__(url, config.resquest_33xs['get_book_content']['method'])

    def soup_to_info(self, soup: BeautifulSoup):

        cont = soup.select_one('#content').text
        paragraphs = cont.split('　　')
        paragraphs = list(filter(None, paragraphs))
        cont = '\n    '.join(paragraphs)
        return cont


class Get_Book_List_HI_qb5200(HtmlInfo):

    def __init__(self, name: str):
        self.name = name
        super().__init__(
            config.request_qb5200['get_book_list']['url'].format(name),
            config.request_qb5200['get_book_list']['method'],
            config.request_qb5200['get_book_list']['headers']
        )

    def soup_to_info(self, soup: BeautifulSoup):
        soup_list = soup.select('.search-list ul li')

        info = []

        for each in soup_list:
            try:
                item = {
                    'book_name': each.select_one('.s2 a').text,
                    'url': each.select_one('.s2 a').get('href'),
                    'auther': '',
                    'breif': each.select_one('.s4').text,
                    'words_count': -1
                }
                if self.name in item['book_name']:
                    info.append(item)
            except Exception:
                pass

        return info


class Get_Book_Chapters_HI_qb5200(HtmlInfo):

    def __init__(self, url: str):
        super().__init__(url, config.request_qb5200['get_book_chapters']['method'], encoding=config.request_qb5200['get_book_chapters']['encoding'])

    def _get_id_from_url(self, url):
        pattern = '.*/(.*?)\.'
        res = re.findall(pattern, url)
        if len(res) == 0: raise Exception('正则不匹配 该章节url异常 argvs={}   line={} file={}'.format(self.method, sys._getframe().f_lineno, __file__))
        return int(res[0])

    def soup_to_info(self, soup: BeautifulSoup):
        soup_list = soup.select('.listmain dd')
        info = []
        tmp_list = []

        for each in soup_list:
            url = '{}{}'.format(config.request_qb5200['host'], each.select_one('a').get('href'))
            id = self._get_id_from_url(url)
            item = {
                'id': id,
                'name': each.select_one('a').text.strip(),
                'url': url
            }
            if url not in tmp_list:
                info.append(item)
                tmp_list.append(url)
        return info


class Get_Book_Content_HI_qb5200(HtmlInfo):

    def __init__(self, url: str):
        super().__init__(url, config.request_qb5200['get_book_content']['method'], encoding=config.request_qb5200['get_book_content']['encoding'])

    def soup_to_info(self, soup: BeautifulSoup):

        cont = soup.select_one('#content').text
        paragraphs = cont.split('　　')
        paragraphs = list(filter(None, paragraphs))
        cont = '\n'.join(paragraphs)

        return cont
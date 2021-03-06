# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup, SoupStrainer
from multiprocessing import Process, Queue

from config import cfg, get_output_dir, get_output_path


class Parser(Process):

    def __init__(self, queue_data):
        super(Parser, self).__init__()
        self._index = 1
        self._num_empty = 0

        self._queue_data = queue_data
        self._delete = u'该文章不存在或已被删除，点击返回古诗文网首页'

    def run(self):
        while True:
            data = self._queue_data.get()
            self._index = data[0]
            html_contents = data[1]

            html_contents = re.sub('<br />', '\n', html_contents)
            only_main3 = SoupStrainer(class_="main3")
            soup_only_main3 = BeautifulSoup(
                html_contents, 'html.parser', parse_only=only_main3)

            # 没有文章了
            if self._num_empty > 1000:
                break
            # 文章不存在
            if soup_only_main3.get_text(strip=True) == self._delete:
                self._num_empty += 1
                continue
            else:
                self._num_empty = 0

            title_poetry = soup_only_main3.find(class_='son1').h1.string

            soup_only_main3.find(class_='son2').p.span.decompose()
            dynasty_poetry = soup_only_main3.find(class_='son2').p.string
            soup_only_main3.find(class_='son2').p.decompose()

            soup_only_main3.find(class_='son2').p.span.decompose()
            author_poetry = soup_only_main3.find(class_='son2').p.string
            soup_only_main3.find(class_='son2').p.decompose()

            soup_only_main3.find(class_='son2').p.decompose()
            soup_only_main3.find(class_='yizhu').decompose()
            content_poetry = soup_only_main3.find(
                class_='cont',id='cont').get_text()
            content_poetry = re.sub('[\n]+', '\n', content_poetry)
            content_poetry = content_poetry.strip('\n')

            path_html, path_txt = get_output_path(dynasty_poetry, self._index)
            file_html = open(path_html, 'w')
            file_html.writelines(data[1].encode('utf-8'))
            file_html.close()
            file_txt = open(path_txt, 'w')
            file_txt.writelines(title_poetry.encode('utf-8') + '\n')
            file_txt.writelines(dynasty_poetry.encode('utf-8') + '\n')
            file_txt.writelines(author_poetry.encode('utf-8') + '\n')
            file_txt.writelines(content_poetry.encode('utf-8') + '\n')
            file_txt.close()

            print '-----------------------------------------------------------'
            print 'Parser: ', self._index
            print '标题：', title_poetry
            print '朝代：', dynasty_poetry
            print '作者：', author_poetry
            print '原文：\n', content_poetry

        print 'Parser finish'

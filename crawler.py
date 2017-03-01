# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup, SoupStrainer
from multiprocessing import Process, Queue

from config import cfg


class Crawler(Process):

    def __init__(self, queue_data):
        super(Crawler, self).__init__()
        self._num = 0
        self._id = 0

        self._queue_data = queue_data

    def run(self):
        while True:
            self._id += 1
            if self._id < 0:
                continue
            self._num += 1
            r = requests.get(cfg.POETRY_URL.format(self._id))
            print '------------------------------------------'
            print 'Crawler: ', self._id, r.status_code

            self._queue_data.put([self._id, r.text])

        print 'Crawler finish'

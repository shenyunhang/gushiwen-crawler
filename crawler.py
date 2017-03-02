# -*- coding: utf-8 -*-

import requests
from multiprocessing import Process, Queue

from config import cfg


class Crawler(Process):

    def __init__(self, queue_data):
        super(Crawler, self).__init__()
        self._index = 1

        self._queue_data = queue_data

    def run(self):
        while True:
            if self._index > 100000:
                continue
            r = requests.get(cfg.POETRY_URL.format(self._id))
            print '------------------------------------------'
            print 'Crawler: ', self._id, r.status_code

            self._queue_data.put([self._id, r.text])
            self._index += 1

        print 'Crawler finish'

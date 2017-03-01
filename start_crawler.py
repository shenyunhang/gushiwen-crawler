#!/usr/bin/env python
# -*- coding: utf-8 -*-


from config import cfg
from crawler import Crawler
from parser import Parser
from multiprocessing import Queue

if __name__ == '__main__':
    print 'start'
    queue_data = Queue(10)
    crawler = Crawler(queue_data)
    crawler.start()

    parser = Parser(queue_data)
    parser.start()

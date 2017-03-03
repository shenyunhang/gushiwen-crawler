# -*- coding: utf-8 -*-

from crawler import Crawler
from parser import Parser
from multiprocessing import Queue

from config import cfg

if __name__ == '__main__':
    print 'start'
    queue_data = Queue(10)
    crawler = Crawler(queue_data)
    crawler.start()

    parser = Parser(queue_data)
    parser.start()

    parser.join()
    crawler.terminate()

    print 'finish'

# coding=utf-8

import logging
from datetime import datetime
import os


class LoggerFactory(object):
    _LOGGER = None

    @staticmethod
    def create_logger():
        # 루트 로거 생성
        LoggerFactory._LOGGER = logging.getLogger()
        LoggerFactory._LOGGER.setLevel(logging.INFO)
        # log 폴더 없을 시 생성
        if (os.path.exists('./log') == False):
            os.makedirs('./log')
        # 로그 포맷 생성
        formatter = logging.Formatter(
            '[%(asctime)s][%(levelname)s|%(filename)s-%(funcName)s:%(lineno)s] >> %(message)s')
        # 핸들러 생성
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        file_handler = logging.FileHandler('./log/' + datetime.now().strftime('%Y%m') + '.log')
        file_handler.setFormatter(formatter)
        LoggerFactory._LOGGER.addHandler(stream_handler)
        LoggerFactory._LOGGER.addHandler(file_handler)

    @classmethod
    def get_logger(cls):
        return cls._LOGGER
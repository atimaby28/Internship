# coding=utf-8
# This is a sample Python script.
#-*-encoding:utf-8-*-
import os
import sys
sys.path.append(r'C:\pythonProject\source\common')
sys.path.append(r'C:\pythonProject\encrypt')
sys.path.append(r'C:\pythonProject\source\database')
sys.path.append(r'C:\pythonProject\source\object')
sys.path.append(r'C:\pythonProject\source\function')

import common_information
import department as dept
import time
from multiprocessing import Pool
#import department2
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import msdatabase
import member as mem
import msdatabase as md

import logger_factory as log
#import member2
import requests
#import api_information as api_info
import difference as differ
import threading
from multiprocessing import Process
import pass_decrypt
#import department2 as dept
import treedepth
#import db_information as db_info
import pandas as pd
import time
import common_information as info

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    log.LoggerFactory.create_logger()
    logging = log.LoggerFactory._LOGGER

    logging.info(u'★☆★☆★☆★☆★☆ Hi, The Program has started ★☆★☆★☆★☆★☆')
    pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)

    # Program Import *************************************************

    common_info = info.CommonInfo()

    member = mem.Member(common_info)

    department = dept.Department(common_info)

    common_info.save_info()

    # Initial : Make Dept ===========================================

    make_tree = treedepth.TreeNode()
    #
    tree = make_tree.build_tree()
    #
    mk = make_tree.append_level(tree, len(tree), 0)
    #
    # print(mk)
    #
    logging.info(mk)
    #
    # department.make_dept(mk)

    # =================================================================

    member.add_update()
    department.add_update()

    logging.info(common_info.get_db_info())
    logging.info(common_info.get_api_info())

    diff = differ.Difference(common_info).dept_diff()

    pool = Pool(processes=1)

    pool.apply_async(member.put_update())
    #member_thread = threading.Thread(target=member.put_update)
    #member_thread.start()

    pool.apply_async(department.put_update())
    #department_thread = threading.Thread(target=department.put_update)
    #department_thread.start()

    pool.apply_async(member.post_additional_member())
    #adding_thread = threading.Thread(target=member.post_additional_member)
    #adding_thread.start()


    logging.info(u'The program has finished...')

    msdatabase.Database().close()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

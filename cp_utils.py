# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : cp_utils.py
   Author   : CoderPig
   date     : 2020-11-26 17:41 
   Desc     : 
-------------------------------------------------
"""
import os


# 判断目录是否存在，不存在则创建
def is_dir_existed(path, mkdir=True):
    if mkdir:
        if not os.path.exists(path):
            os.makedirs(path)
    else:
        return os.path.exists(path)


# 获取目录下的所有文件路径
def fetch_all_file(file_dir):
    return list(map(lambda x: os.path.join(file_dir, x), os.listdir(file_dir)))


def read_file_content(file_path):
    if not os.path.exists(file_path):
        return "文件不存在"
    else:
        with open(file_path, 'r+', encoding='utf-8') as f:
            return f.read()


def write_file(content, file_path):
    with open(file_path, "w+", encoding='utf-8') as f:
        f.write(content)

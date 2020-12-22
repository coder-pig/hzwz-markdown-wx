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
import shutil


def delete_file(file_path):
    del_list = os.listdir(file_path)
    for f in del_list:
        file_path = os.path.join(file_path, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


# 判断目录是否存在，不存在则创建
def is_dir_existed(file_path, mkdir=True, is_recreate=False):
    if mkdir:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        else:
            if is_recreate:
                delete_file(file_path)
                os.makedirs(file_path)
    else:
        return os.path.exists(file_path)


# 获取目录下的所有文件路径
def fetch_all_file(file_dir):
    return list(map(lambda x: os.path.join(file_dir, x), os.listdir(file_dir)))


# 获取目录下特定后缀的文件路径列表
def filter_file_type(file_dir, file_suffix):
    result_list = []
    file_path_list = fetch_all_file(file_dir)
    for file_path in file_path_list:
        if file_path.endswith(file_suffix):
            result_list.append(file_path)
    return result_list


# 读取文件内容
def read_file_content(file_path):
    if not os.path.exists(file_path):
        return "文件不存在"
    else:
        with open(file_path, 'r+', encoding='utf-8') as f:
            return f.read()


# 写入文件
def write_file(content, file_path):
    with open(file_path, "w+", encoding='utf-8') as f:
        f.write(content)


# 追加文件
def write_file_append(content, file_path):
    with open(file_path, "a+", encoding='utf-8') as f:
        f.write(content)

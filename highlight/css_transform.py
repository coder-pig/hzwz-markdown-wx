# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : css_transform.py
   Author   : CoderPig
   date     : 2020-12-15 06:52
   Desc     : css样式提取工具：提取class选择器样式，保存到对应ini文件中
-------------------------------------------------
"""
import os
import re
import configparser

import cp_utils
from cp_utils import read_file_content

css_pattern = re.compile(r'(\.hljs.*?){(.*?)}', re.S)  # 提取css的正则
config_dir = os.path.join(os.getcwd(), 'styles_conf')


def transform_css_to_ini(file_path):
    id_dict = {}
    file_content = read_file_content(file_path).replace("\n", '')
    result_list = css_pattern.findall(file_content)
    for result in result_list:
        id_list = result[0].rstrip().split(',')
        for id_name in id_list:
            if id_name[1:] in id_dict:
                id_dict[id_name[1:]] += result[1]
            else:
                id_dict[id_name[1:]] = result[1]
    return id_dict


if __name__ == '__main__':
    cp_utils.is_dir_existed('styles_conf', is_recreate=True)
    file_path_list = cp_utils.fetch_all_file('styles')
    css_path_list = []
    for path in file_path_list:
        if path.endswith(".css"):
            css_path_list.append(path)
    for css_path in css_path_list:
        conf = configparser.ConfigParser()
        conf_dict = transform_css_to_ini(css_path)
        conf_file_path = os.path.join(config_dir, css_path[7:].split('.')[0] + '.ini')
        if os.path.exists(conf_file_path):
            os.remove(conf_file_path)
        conf.read(conf_file_path)
        conf_list = conf.sections()
        if 'theme' not in conf_list:
            conf.add_section('theme')
        for class_id in conf_dict:
            conf.set('theme', class_id, conf_dict[class_id].replace('%', '~').lstrip())
        conf.write(open(conf_file_path, 'w+'))

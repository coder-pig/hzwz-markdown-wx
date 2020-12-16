# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : renderer_code.py
   Author   : CoderPig
   date     : 2020-12-15 15:50 
   Desc     : 渲染代码样式
-------------------------------------------------
"""
import os
import cp_utils
import configparser

config = configparser.ConfigParser()
file_dir = os.path.abspath(__file__).replace("renderer_code.py", "")
before_path = os.path.join(file_dir, 'transform/before.html')
after_path = os.path.join(file_dir, 'transform/after.html')
js_path = os.path.join(file_dir, 'renderer_code.js')


# highlight.js高亮转换
def renderer_by_node(content, theme, language=None):
    # 读取对应主题配置文件，获取class和style对应字典
    config.read(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'styles_conf/{}.ini'.format(theme)),
                encoding='utf8')
    items = config.items('theme')
    cp_utils.write_file(content, before_path)
    node_command = 'node {}'.format(js_path)
    if language is not None:
        node_command += " " + language
    os.system(node_command)
    result = ''
    with open(after_path, "r+", encoding='utf-8') as f:
        for line in f:
            # 获得左侧空格数量
            left_blank_count = 0
            for c in line:
                if c == ' ':
                    left_blank_count += 1
                else:
                    break
            result += '{}{}<br>'.format('&nbsp;' * left_blank_count, line.lstrip())
    for (key, value) in items:
        result = result.replace('class="{}"'.format(key), 'style="{}"'.format(value))
    result = result.replace("~", "%")
    return result

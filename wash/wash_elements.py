# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : wash_elements.py
   Author   : CoderPig
   date     : 2020-11-19 16:02 
   Desc     : 节点清洗
-------------------------------------------------
"""
import re

from lxml import etree, html


def read_from_file(file_path):
    content = ""
    with open(file_path, "r+", encoding='utf-8') as f:
        content += f.read()
    return content


def write_file(content, file_path):
    with open(file_path, "w+", encoding='utf-8') as f:
        f.write(content)


# 过滤无用属性值
pattern_str_list = [
    r'data-.*?=".*?"',
    r'class=".*?"',
    r'id=".*?"',
    r'data-mpa-.*?=".*?"',
    r'mpa-from-tpl=".*?"',
    r'data-mpa-powered-by=".*?"',
    r'powered-by=".*?"',
    r'data-cropselx\d=".*?"',
    r'data-cropsely\d=".*?"',
    r'data-md5=".*?"',
    r'mpa-is-content=".*?"',
    r'<mpchecktext contenteditable="false"/>'
]

if __name__ == '__main__':
    wash_pattern = re.compile('|'.join(pattern_str_list))
    html_content = read_from_file('in.html')
    result = re.sub('|'.join(pattern_str_list), "", html_content)
    write_file(etree.tostring(html.fromstring(result), encoding='unicode', pretty_print=True), 'out.html')

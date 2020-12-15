# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : css_analysis.py
   Author   : CoderPig
   date     : 2020-12-14 16:52
   Desc     : css解析脚本
-------------------------------------------------
"""
import os
import re

# (\{.*?\})
from cp_utils import read_file_content

css_pattern = re.compile(r'(\.hljs.*?){(.*?)}', re.S)  # 提取css的正则

if __name__ == '__main__':
    file_content = read_file_content('styles/default.css').replace("\n", '')
    fetch_pattern = re.compile(r'(\.hljs.*?){(.*?)}', re.S)
    result = fetch_pattern.findall(file_content)
    print(result)
    # rules = tinycss2.parse_stylesheet(read_file_content('styles/default.css'))
    # for rule in rules:
    #     if rule.type == 'qualified-rule':
    #         prelude_list = rule.prelude
    #         content_list = rule.content
    #         for p in prelude_list:
    #             print(p.value)
    #         for content in content_list:
    #             print(content.value)
    #         print(rule.prelude, rule.content, end="\n\n\n")
    # for prelude in rule.prelude:
    #     print(prelude)
    #     if prelude.type == 'ident':
    #         None
    # print(prelude.value)

    # if .type == 'ident':
    # print(rule.prelude, end="\n\n")
    # print(rule.content, end="\n\n")
    # print('*' * 100)

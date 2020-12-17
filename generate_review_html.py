# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : generate_review_html.py
   Author   : CoderPig
   date     : 2020-12-17 15:05 
   Desc     : 生成样式预览html
-------------------------------------------------
"""
import os
import cp_utils

if __name__ == '__main__':
    template_dict = {}
    template_path_list = cp_utils.fetch_all_file(os.path.join(os.getcwd(), 'template'))
    for template_path in template_path_list:
        template_dict[template_path.split(os.sep)[-1]] = cp_utils.fetch_all_file(template_path)
    result = ''
    for template in template_dict:
        result += ("<html>{}<div>".format(template))
        for template_html in template_dict[template]:
            result += cp_utils.read_file_content(template_html)
        result += "</div><br>"
    cp_utils.write_file(result, 'test.html')

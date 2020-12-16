# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : generate_article.py
   Author   : CoderPig
   date     : 2020-12-16 9:32 
   Desc     : 渲染生成文章
-------------------------------------------------
"""
import os.path
import cp_utils
from styles_renderer import render_article

md_dir = os.path.join(os.getcwd(), 'article/md')  # 待转换md文件路径
out_dir = os.path.join(os.getcwd(), 'article/out')  # 输出html文件路径
styles_dir = os.path.join(os.getcwd(), 'styles')  # 文章样式配置文件路径

if __name__ == '__main__':
    # 相关文件夹初始化
    cp_utils.is_dir_existed(md_dir)
    cp_utils.is_dir_existed(out_dir)
    # 文件检查/
    md_file_path_list = cp_utils.filter_file_type(md_dir, '.md')
    if len(md_file_path_list) == 0:
        print("当前目录无md文件，请检查后重试！")
        exit(0)
    theme_file_path_list = cp_utils.filter_file_type(styles_dir, '.ini')
    for md_file_path in md_file_path_list:
        split_list = md_file_path.split(os.sep)
        if len(split_list) > 0:
            file_name = split_list[-1]
            print("读取文件 →", file_name)
            file_content = cp_utils.read_file_content(md_file_path)
            for theme_file_path in theme_file_path_list:
                print("应用样式：→", theme_file_path)
                render_article(file_content, theme_file_path)

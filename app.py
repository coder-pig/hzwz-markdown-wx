# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : app.py
   Author   : CoderPig
   date     : 2020-12-16 9:32 
   Desc     : 渲染生成文章
-------------------------------------------------
"""
import os.path

import config_getter
import cp_utils
from styles_renderer import render_article

md_dir = os.path.join(os.getcwd(), config_getter.get_config("config", "md_dir"))  # 待转换md文件路径
out_dir = os.path.join(os.getcwd(), config_getter.get_config("config", "out_dir"))  # 输出html文件路径
styles_dir = os.path.join(os.getcwd(), config_getter.get_config("config", "styles_dir"))  # 文章样式配置文件路径
template_dir = os.path.join(os.getcwd(), config_getter.get_config("config", "template_dir"))  # 样式模板路径

if __name__ == '__main__':
    # 相关文件夹初始化
    cp_utils.is_dir_existed(md_dir)
    cp_utils.is_dir_existed(out_dir)
    cp_utils.is_dir_existed(styles_dir)
    cp_utils.is_dir_existed(template_dir)
    # 文件检查/
    md_file_path_list = cp_utils.filter_file_type(md_dir, '.md')
    if len(md_file_path_list) == 0:
        print("当前目录无md文件，请检查后重试！")
        exit(0)
    theme_file_path_list = cp_utils.filter_file_type(styles_dir, '.ini')
    if len(md_file_path_list) == 0:
        print("当前目录无样式配置文件，请检查后重试！")
        exit(0)
    for md_file_path in md_file_path_list:
        split_list = md_file_path.split(os.sep)
        if len(split_list) > 0:
            file_name = split_list[-1]
            print("读取文件 →", file_name)
            file_content = cp_utils.read_file_content(md_file_path)
            for theme_file_path in theme_file_path_list:
                theme_name = theme_file_path.split(os.sep)[-1][:-4]
                print("应用样式 →", theme_name)
                renderer_content = render_article(file_content, theme_file_path, template_dir)
                out_file_path = os.path.join(out_dir, file_name.replace(".md", "_{}.html".format(theme_name)))
                print("输出文件 →", out_file_path)
                cp_utils.write_file(renderer_content, out_file_path)

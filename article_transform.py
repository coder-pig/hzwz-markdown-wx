# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : article_transform.py
   Author   : CoderPig
   date     : 2020-11-26 16:52 
   Desc     : 生成脚本
-------------------------------------------------
"""
import os.path

import config_getter
import cp_utils
from theme.renderer_utils import renderer_theme

theme_list = config_getter.get_config("Theme", 'theme').split(',')  # 主题列表
out_dir = os.path.join(os.getcwd(), config_getter.get_config("Theme", "out_dir"))
md_dir = os.path.join(os.getcwd(), config_getter.get_config("Theme", "md_dir"))

if __name__ == '__main__':
    # 相关文件夹初始化
    cp_utils.is_dir_existed(md_dir)
    cp_utils.is_dir_existed(out_dir)
    # 判断目录中是否有md文件
    file_path_list = cp_utils.fetch_all_file(md_dir)
    md_path_list = []
    for file_path in file_path_list:
        if file_path.endswith(".md"):
            md_path_list.append(file_path)
    if len(md_path_list) == 0:
        print("当前目录无md文件，请检查后重试！")
        exit(0)
    else:
        for md_path in md_path_list:
            split_list = md_path.split(os.sep)
            if len(split_list) > 0:
                file_name = split_list[-1]
                print("读取文件 →", file_name)
                file_content = cp_utils.read_file_content(md_path)
                for theme in theme_list:
                    print("使用 === {}主题 === 渲染文件 → {}".format(theme, file_name))
                    out_file_path = os.path.join(out_dir, file_name.replace(".md", "_{}.html".format(theme)))
                    print("输出文件 →", out_file_path)
                    renderer_content = renderer_theme(file_content, theme)
                    cp_utils.write_file(renderer_content, out_file_path)

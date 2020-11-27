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

import mistune
from mistune.plugins import plugin_table

import config_getter
import cp_utils
from theme.cp_python_spider.renderer import CpPythonSpiderRenderer

# 读取配置
theme = config_getter.get_config("Theme", 'theme')  # 获取主题
wx_dir = os.path.join(os.getcwd(), config_getter.get_config("Theme", "wx_dir"))
md_dir = os.path.join(os.getcwd(), config_getter.get_config("Theme", "md_dir"))

# 头尾样式代码
header_renderer = None
footer_renderer = None


# 转换渲染
def transform(md_content):
    global header_renderer, footer_renderer
    renderer = None
    if theme == 'cp_python_spider':
        renderer = CpPythonSpiderRenderer()
        header_renderer = renderer.header_render()
        footer_renderer = renderer.footer_render()
    else:
        renderer = CpPythonSpiderRenderer()
    renderer_result = mistune.create_markdown(renderer=renderer, plugins=[plugin_table])(md_content) \
        .replace("\n", "") \
        .replace("<br><section><br>", "<br><section>") \
        .replace("<br><br>", "<br>") \
        .replace("\u200b", "")
    if header_renderer is not None:
        renderer_result = header_renderer + renderer_result
    if footer_renderer is not None:
        renderer_result += footer_renderer
    return renderer_result


if __name__ == '__main__':
    # 相关文件夹初始化
    cp_utils.is_dir_existed(md_dir)
    cp_utils.is_dir_existed(wx_dir)
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
                print("渲染文件 →", file_name)
                wx_file_path = os.path.join(wx_dir, file_name.replace(".md", ".html"))
                print("输出文件 →", wx_file_path)
                cp_utils.write_file(transform(file_content), wx_file_path)

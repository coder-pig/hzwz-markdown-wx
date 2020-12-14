# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : renderer_utils.py
   Author   : CoderPig
   date     : 2020-12-14 14:09 
   Desc     : 主题渲染工具类
-------------------------------------------------
"""
import mistune
from mistune.plugins import plugin_table

from theme.cp_kotlin_course_wx.renderer import KotlinRenderer
from theme.cp_python_spider_wx.renderer import CpPythonSpiderRenderer
from theme.default.renderer import DefaultRenderer


# 主题渲染
def renderer_theme(md_content, theme):
    if theme == 'default':
        return mistune.create_markdown(renderer=DefaultRenderer())(md_content)
    elif theme == 'cp_python_spider_wx':
        renderer = CpPythonSpiderRenderer()
        header_renderer = renderer.header_render()
        footer_renderer = renderer.footer_render()
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
    elif theme == 'cp_kotlin_course':
        renderer = KotlinRenderer()
        renderer_result = mistune.create_markdown(renderer=renderer)(md_content)
        return renderer_result

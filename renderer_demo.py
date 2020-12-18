# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : renderer_demo.py
   Author   : CoderPig
   date     : 2020-12-18 17:35 
   Desc     : 自定义渲染器Demo
-------------------------------------------------
"""
import os

import mistune
from jinja2 import Environment, FileSystemLoader


class MyRenderer(mistune.HTMLRenderer):
    def __init__(self):
        super().__init__()
        self.env = Environment(loader=FileSystemLoader(os.path.join(os.getcwd(), "template/custom")))
        self.img_template = self.env.get_template("myrenderer/image.html")
        self.p_template = self.env.get_template("myrenderer/p.html")

    def image(self, src, alt="", title=None):
        result = ''
        if self.img_template is not None:
            result += self.img_template.render(src=src)
        if self.p_template is not None and alt != '':
            result += self.p_template.render(alt=alt)
        return result


def custom_render_article(content):
    """
    渲染文章

    :param content: Markdown内容
    :return: 渲染后带样式的HTML内容
    """
    render = MyRenderer()
    content_result = mistune.create_markdown(renderer=render)(content)
    return content_result

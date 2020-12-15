# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : renderer.py
   Author   : CoderPig
   date     : 2020-12-14 18:16 
   Desc     : 抠腚男孩 → Kotlin实用教程 → https://mp.weixin.qq.com/s/why-ikTbbiCG4uzGer48IQ
-------------------------------------------------
"""
import os

import mistune
from jinja2 import Environment, FileSystemLoader

from highlight.renderer_code import renderer_by_node


class KotlinRenderer(mistune.HTMLRenderer):
    def __init__(self):
        super().__init__()
        # 创建一个包加载器对象(也可以使用PackageLoader包加载器的方式加载)
        self.env = Environment(
            loader=FileSystemLoader(os.path.join(os.getcwd(), 'theme/{}/templates'.format('cp_kotlin_course_wx'))))
        # 加载各类模板
        self.mac_window = self.env.get_template('mac_window.html')

    # 代码块
    def block_code(self, code, info=None):
        highlight_result = renderer_by_node(code, 'androidstudio', info)
        return self.mac_window.render(text=highlight_result)

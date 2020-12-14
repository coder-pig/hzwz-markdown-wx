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
from lxml import etree
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name


class KotlinRenderer(mistune.HTMLRenderer):
    # 代码块
    def block_code(self, code, info=None):
        lexer = get_lexer_by_name(info if info is not None else 'Kotlin', stripall=True)
        formatter = html.HtmlFormatter(noclasses=True, style='xcode', wrapcode=True)
        highlight_html = highlight(code, lexer, formatter).replace('div', 'section')
        # 行尾塞换行符，行首塞&nbsp;
        highlight_html_result = ''
        lines = highlight_html.split("\n")
        if len(lines) > 0:
            for index, line in enumerate(lines):
                if line == '' and index == len(lines) - 1:
                    break
                else:
                    # 获取左侧空格数量
                    left_blank_count = 0
                    for c in line:
                        if c == ' ':
                            left_blank_count += 1
                        else:
                            break
                highlight_html_result += '{}{}<br>'.format('&nbsp;' * left_blank_count, line.lstrip())
        highlight_selector = etree.HTML(highlight_html_result)
        # 创建一个包裹code节点下所有元素的节点，同时设置字体大小
        span_node = etree.Element('span', {'style': 'font-size: 12px;'})
        # 遍历code里所有的节点，添加到外层span中，清空code子节点，添加这个span结点
        code_node = highlight_selector.xpath("//code")
        if len(code_node) > 0:
            node_list = code_node[0].xpath('child::*')
            for node in node_list:
                style = node.attrib.get('style')
                if style is not None:
                    node.attrib['style'] = 'font-size: 12px; ' + style
                    if node.text.endswith('\n'):
                        print("换行")
                span_node.append(node)
            # 清空code节点
            code_text = code_node[0].text
            code_node[0].clear()
            # code节点设置水平滚动条、边距等
            code_node[0].attrib['style'] = 'display: block; padding: 5.95px; overflow-x: auto; white-space:nowrap;'
            span_node.text = code_text
            code_node[0].append(span_node)
        # etree生成的html会带上<html><body>标签，利用游标范围过滤，同时替换div标签为section
        return '<br>' + etree.tostring(highlight_selector).decode('utf-8')[12: -14].replace("div", "section")

# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : styles_renderer.py
   Author   : CoderPig
   date     : 2020-12-16 10:28 
   Desc     : 样式渲染
-------------------------------------------------
"""
import configparser
import os
import html
import mistune
from mistune.plugins import plugin_table
from jinja2 import Environment, FileSystemLoader
from highlight.renderer_code import renderer_by_node
from lxml import etree


# 表格单元格
class Cell:
    def __init__(self, text, align):
        self.text = text
        self.align = align


class StyleRenderer(mistune.HTMLRenderer):
    def __init__(self, style_file):
        super().__init__()
        self.config = configparser.ConfigParser()
        self.config.read(style_file, encoding='utf-8')
        self.items = self.config.items('style')
        # 创建一个包加载器对象(也可以使用PackageLoader包加载器的方式加载)
        self.env = Environment(loader=FileSystemLoader(os.path.join(os.getcwd(), 'template')))
        # 模板加载
        for item in self.items:
            key = item[0]
            value = item[1]
            if key == 'h1':
                self.h1_template = self.env.get_template('/h1/{}.html'.format(value)) if value != 'None' else None
            elif key == 'h2':
                self.h2_template = self.env.get_template('/h2/{}.html'.format(value)) if value != 'None' else None
            elif key == 'h3':
                self.h3_template = self.env.get_template('/h3/{}.html'.format(value)) if value != 'None' else None
            elif key == 'h4':
                self.h4_template = self.env.get_template('/h4/{}.html'.format(value)) if value != 'None' else None
            elif key == 'h5':
                self.h5_template = self.env.get_template('/h5/{}.html'.format(value)) if value != 'None' else None
            elif key == 'image':
                self.image_template = self.env.get_template('/image/{}.html'.format(value)) if value != 'None' else None
            elif key == 'li':
                self.li_template = self.env.get_template('/li/{}.html'.format(value)) if value != 'None' else None
            elif key == 'link':
                self.link_template = self.env.get_template('/link/{}.html'.format(value)) if value != 'None' else None
            elif key == 'mac_window':
                self.mac_window_template = self.env.get_template(
                    '/mac_window/{}.html'.format(value)) if value != 'None' else None
            elif key == 'p':
                self.p_template = self.env.get_template('/p/{}.html'.format(value)) if value != 'None' else None
            elif key == 'strong':
                self.strong_template = self.env.get_template(
                    '/strong/{}.html'.format(value)) if value != 'None' else None
            elif key == 'table':
                self.table_template = self.env.get_template('/table/{}.html'.format(value)) if value != 'None' else None
            elif key == 'ul':
                self.ul_template = self.env.get_template('/ul/{}.html'.format(value)) if value != 'None' else None
            elif key == 'blockquote':
                self.blockquote_template = self.env.get_template(
                    '/blockquote/{}.html'.format(value)) if value != 'None' else None
            elif key == 'codespan':
                self.codespan_template = self.env.get_template(
                    '/codespan/{}.html'.format(value)) if value != 'None' else None
            elif key == 'codestyle':
                self.codestyle = value if value != 'None' else 'xcode'
            elif key == 'header':
                self.header_template = self.env.get_template(
                    '/header/{}.html'.format(value)) if value != 'None' else None
            elif key == 'footer':
                self.footer_template = self.env.get_template(
                    '/footer/{}.html'.format(value)) if value != 'None' else None
            elif key == 'background':
                self.background_template = self.env.get_template(
                    '/background/{}.html'.format(value)) if value != 'None' else None

    # 分级标题
    def heading(self, text, level):
        if level == 1:
            if self.h1_template is not None:
                return self.h1_template.render(text=text)
            else:
                return "<h{}>{}</h{}><br>".format(level, text, level)
        elif level == 2:
            if self.h2_template is not None:
                return self.h2_template.render(text=text)
            else:
                return "<h{}>{}</h{}><br>".format(level, text, level)
        elif level == 3:
            if self.h3_template is not None:
                return self.h3_template.render(text=text)
            else:
                return "<h{}>{}</h{}><br>".format(level, text, level)
        elif level == 4:
            if self.h4_template is not None:
                return self.h4_template.render(text=text)
            else:
                return "<h{}>{}</h{}><br>".format(level, text, level)
        else:
            return "<h{}>{}</h{}><br>".format(level, text, level)

    # 图片
    def image(self, src, alt="", title=None):
        if self.image_template is not None:
            return self.image_template.render(src=src)
        else:
            return '<img src="{}" alt="{}" {}/>'.format(
                src, alt, 'title="' + escape_html(title) + '"' if title else None)

    # 粗体
    def strong(self, text):
        if self.strong_template is not None:
            return self.strong_template.render(text=text)
        else:
            return '<strong>{}</strong>'.format(text)

    # 行内代码
    def codespan(self, text):
        if self.codespan_template is not None:
            return self.codespan_template.render(text=text)
        else:
            return '<code>{}</code>'.format(escape(text))

    # 列表
    def list(self, text, ordered, level, start=None):
        if self.ul_template is not None:
            return self.ul_template.render(text=text)
        else:
            if ordered:
                return '<ol{}>\n{}</ol>\n'.format(' start=' + str(start) + '' if start is not None else '', text)
            return '<ul>\n{}</ul>\n'.format(text)

    # 列表项
    def list_item(self, text, level):
        if self.li_template is not None:
            return self.li_template.render(text=text)
        else:
            return '<li>{}</li>\n'.format(text)

    # 链接
    def link(self, link, text=None, title=None):
        if self.link_template is not None:
            return self.link_template.render(link=link, text=text)
        else:
            if text is None:
                text = link
            s = '<a href="{}"'.format(self._safe_url(link))
            if title:
                s += ' title="{}"'.format(escape_html(title))
            return s + '>{}</a>'.format((text or link))

    # 段落
    def paragraph(self, text):
        if self.p_template is not None:
            return self.p_template.render(text=text)
        else:
            return '<p>{}</p>\n'.format(text)

    # 代码块
    def block_code(self, code, info=None):
        if self.mac_window_template is not None:
            highlight_result = renderer_by_node(code, self.codestyle, info)
            return self.mac_window_template.render(text=highlight_result)
        else:
            result = '<pre><code'
            if info is not None:
                info = info.strip()
            if info:
                lang = info.split(None, 1)[0]
                lang = escape_html(lang)
                result += ' class="language-' + lang + '"'
            return result + '>' + escape(code) + '</code></pre>\n'

    # 表格
    def table(self, text):
        if self.table_template is not None:
            table_selector = etree.HTML(text)
            ths = table_selector.xpath('//tr/th')
            tds = table_selector.xpath('//tr/td')
            th_cell_list = []
            for index, value in enumerate(ths):
                style = value.attrib.get('style')[11:]
                text = value.text
                th_cell_list.append(Cell(text, style))
            td_cell_list = []
            for index, value in enumerate(tds):
                style = value.attrib.get('style')[11:]
                text = value.text
                td_cell_list.append(Cell(text, style))
            return self.table_template.render(row_count=len(ths), header_list=th_cell_list, detail_list=td_cell_list)
        else:
            return text

    # 头部
    def header(self):
        if self.header_template is not None:
            return self.header_template.render()
        else:
            return ''

    # 尾部
    def footer(self):
        if self.footer_template is not None:
            return self.footer_template.render()
        else:
            return ''

    # 背景
    def background(self, text):
        if self.background_template is not None:
            return self.background_template.render(text=text)
        else:
            return text


def escape(s, quote=True):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
    return s


def escape_html(s):
    if html is not None:
        return html.escape(html.unescape(s)).replace('&#x27;', "'")
    return escape(s)


def render_article(content, style_ini_path):
    render = StyleRenderer(os.path.join(os.getcwd(), style_ini_path))
    content_result = mistune.create_markdown(renderer=render, plugins=[plugin_table])(content)
    return render.background(text='{}{}{}'.format(render.header(), content_result, render.footer()))

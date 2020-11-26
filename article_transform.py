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
from jinja2 import Environment, FileSystemLoader
from lxml import etree
from mistune.plugins import plugin_table
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
import config_getter
import cp_utils

# 读取配置
theme = config_getter.get_config("Theme", 'theme')  # 获取主题
code_style = config_getter.get_config("Theme", 'style')  # 获取代码样式
wx_dir = os.path.join(os.getcwd(), config_getter.get_config("Theme", "wx_dir"))
md_dir = os.path.join(os.getcwd(), config_getter.get_config("Theme", "md_dir"))
# 创建一个包加载器对象(也可以使用PackageLoader包加载器的方式加载)
env = Environment(loader=FileSystemLoader(os.path.join(os.getcwd(), 'theme/{}/templates'.format(theme))))

# 加载各类模板
h2_template = env.get_template('h2.html')
h3_template = env.get_template('h3.html')
h4_template = env.get_template('h4.html')
p_template = env.get_template('p.html')
strong_template = env.get_template('strong.html')
blockquote_template = env.get_template('blockquote.html')
table_template = env.get_template('table.html')
li_template = env.get_template('li.html')
ul_template = env.get_template('ul.html')
image_template = env.get_template('image.html')
link_template = env.get_template('link.html')
codespan_template = env.get_template('codespan.html')
article_header_template = env.get_template('article_header.html')
article_footer_template = env.get_template('article_footer.html')


# 表格单元格
class Cell:
    text = None
    align = None
    is_head = False

    def __init__(self, text, align, is_left):
        self.text = text
        self.align = align
        self.is_left = is_left


# 自定义渲染器
class MyRenderer(mistune.HTMLRenderer):

    #  标题
    def heading(self, text, level):
        if level == 2:
            return h2_template.render(text=text)
        elif level == 3:
            return h3_template.render(text=text)
        elif level == 4:
            split_list = text.split("：")
            if len(split_list) > 0:
                return h4_template.render(order=split_list[0], text=split_list[1])
            return h4_template.render(text=text)
        else:
            return "<h{}>{}</h{}><br>".format(level, text, level)

    # 粗体
    def strong(self, text):
        return strong_template.render(text=text)

    # 行内代码
    def codespan(self, text):
        # 如果有**开头说明字体需加粗
        if text.startswith("**"):
            text = codespan_template.render(text='<strong>{}</strong>'.format(text[2: -2]))
        return codespan_template.render(text=text)

    # 引用
    def block_quote(self, text):
        is_ul = False  # 是否为列表类型
        # 判断是否为列表，是去掉换行
        if text.startswith("<br>"):
            is_ul = True
            text = text.replace("<br>", "")
        #  如果是<section>开头说明前面先被段落渲染过，提取文本
        if text.startswith("<section>"):
            section_selector = etree.HTML(text)
            spans = section_selector.xpath("descendant::span")
            text_result = ''
            if len(spans) > 0:
                for span in spans:
                    text_result += blockquote_template.render(text=span.text)
            return text_result
        render_result = blockquote_template.render(text=text)
        if is_ul:
            render_result = render_result.replace('<span style="letter-spacing: 1px; margin-left: 0.5em"><ul', "<ul")
            render_result = render_result.replace('</ul></span>', "</ul>")
        return render_result

    # 段落
    def paragraph(self, text):
        return p_template.render(text=text)

    # 列表
    def list(self, text, ordered, level, start=None):
        return ul_template.render(text=text)

    # 列表项
    def list_item(self, text, level):
        return li_template.render(text=text)

    # 表格处理
    def table(self, text):
        table_selector = etree.HTML(text.replace("<code>", "").replace("</code>", ""))
        table_headers = table_selector.xpath('//tr/th')
        table_details = table_selector.xpath('//tr/td')
        cell_header_list = []
        for index, values in enumerate(table_headers):
            style = values.attrib.get('style')
            text = values.text
            cell_header_list.append(
                Cell(text.replace(" ", "") if text is not None else None,
                     None if style is None else style[11:],
                     True if (index % 2 == 0) else False))
        cell_detail_list = []
        for index, values in enumerate(table_details):
            style = values.attrib.get('style')
            text = values.text
            cell_detail_list.append(
                Cell(text.replace(" ", "") if text is not None else None,
                     None if style is None else style[11:],
                     True if (index % 2 == 0) else False))
        return table_template.render(header_list=cell_header_list, detail_list=cell_detail_list)

    # 代码块
    def block_code(self, code, info=None):
        lexer = get_lexer_by_name(info if info is not None else 'Python', stripall=True)
        formatter = html.HtmlFormatter(noclasses=True, style=code_style, wrapcode=True)
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

    # 超链接
    def link(self, link, text=None, title=None):
        return link_template.render(text=text, link=link)

    # 图片
    def image(self, src, alt="", title=None):
        return image_template.render(src=src)


# 转换渲染
def transform(md_content):
    return mistune.create_markdown(renderer=MyRenderer(), plugins=[plugin_table])(md_content) \
        .replace("\n", "") \
        .replace("<br><section><br>", "<br><section>") \
        .replace("<br><br>", "<br>") \
        .replace("\u200b", "")


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
                renderer_result = transform(file_content)
                write_content = article_header_template.render(
                    author="CoderPig") + renderer_result + article_footer_template.render()
                wx_file_path = os.path.join(wx_dir, file_name.replace(".md", ".html"))
                print("输出文件 →", wx_file_path)
                cp_utils.write_file(write_content, wx_file_path)

# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File     : renderer.py
   Desc     : 样式渲染 (Refactored for Server)
-------------------------------------------------
"""
import html
import mistune
from mistune.plugins import plugin_table
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

from .themes import get_jinja_env

# 表格单元格
class Cell:
    def __init__(self, text, align):
        self.text = text
        self.align = align

class StyleRenderer(mistune.HTMLRenderer):
    def __init__(self, theme_data):
        super().__init__()
        self.theme_data = theme_data
        self.random_color_list = ['213, 15, 37', '51, 105, 232', '238, 178, 17', '15, 157, 88']
        self.current_color_index = -1
        self.env = get_jinja_env()
        
        # Load templates based on theme config
        self.templates = {}
        self.codestyle = 'xcode'
        
        if not self.theme_data:
            return

        for key, value in self.theme_data.items():
            if key == 'codestyle':
                self.codestyle = value if value != 'None' else 'xcode'
                continue
            
            # Map keys to template files
            # Keys in ini match folder names in template/ (mostly)
            if value != 'None':
                try:
                    # Remove leading slash for Jinja2 relative path
                    template_path = f'{key}/{value}.html'
                    self.templates[key] = self.env.get_template(template_path)
                except Exception as e:
                    print(f"Failed to load template {key}/{value}: {e}")
                    self.templates[key] = None
            else:
                self.templates[key] = None

    def _get_template(self, name):
        return self.templates.get(name)

    # 分级标题
    def heading(self, text, level):
        template = self._get_template(f'h{level}')
        if template:
            if level in [2, 3, 4]:
                if self.current_color_index != -1:
                    self.current_color_index = (self.current_color_index + 1) % len(self.random_color_list)
                else:
                    self.current_color_index = 0
                return template.render(text=text, color=self.random_color_list[self.current_color_index])
            return template.render(text=text)
        return f"<h{level}>{text}</h{level}><br>"

    # 图片
    def image(self, src, alt="", title=None):
        template = self._get_template('image')
        if template:
            return template.render(src=src)
        return f'<img src="{src}" alt="{alt}" title="{escape_html(title) if title else ""}" referrerpolicy="no-referrer" />'

    # 粗体
    def strong(self, text):
        template = self._get_template('strong')
        if template:
            return template.render(text=text)
        return f'<strong>{text}</strong>'

    # 行内代码
    def codespan(self, text):
        template = self._get_template('codespan')
        if template:
            return template.render(text=text)
        return f'<code>{escape(text)}</code>'

    # 列表
    def list(self, text, ordered, level, start=None):
        template = self._get_template('ul') # Default to ul? Original used ul_template for both?
        # Original: if self.ul_template is not None: return self.ul_template.render(text=text)
        # It seems it didn't distinguish ol/ul in template? 
        # Wait, original code:
        # if self.ul_template is not None: return self.ul_template.render(text=text)
        # else: if ordered: ... else ...
        # So if template exists, it uses it regardless of ordered status.
        
        if template:
            return template.render(text=text)
        
        if ordered:
            start_attr = f' start="{start}"' if start is not None else ''
            return f'<ol{start_attr}>\n{text}</ol>\n'
        return f'<ul>\n{text}</ul>\n'

    # 列表项
    def list_item(self, text, level):
        template = self._get_template('li')
        if template:
            return template.render(text=text)
        return f'<li>{text}</li>\n'

    # 链接
    def link(self, link, text=None, title=None):
        template = self._get_template('link')
        if template:
            return template.render(link=link, text=text)
        
        text = text or link
        title_attr = f' title="{escape_html(title)}"' if title else ''
        return f'<a href="{self._safe_url(link)}"{title_attr}>{text}</a>'

    # 段落
    def paragraph(self, text):
        template = self._get_template('p')
        if template:
            return template.render(text=text)
        return f'<p>{text}</p>\n'

    # 代码块
    def block_code(self, code, info=None):
        # Highlighting using Pygments
        lang = info.split(None, 1)[0] if info else None
        try:
            lexer = get_lexer_by_name(lang) if lang else guess_lexer(code)
        except ClassNotFound:
            lexer = guess_lexer(code)
            
        # Inline styles (noclasses=True) is crucial for WeChat
        formatter = HtmlFormatter(style=self.codestyle, noclasses=True, wrapcode=False)
        highlighted_code = highlight(code, lexer, formatter)
        
        # Pygments wraps in <div class="highlight"><pre>...</pre></div>
        # We might want to strip the outer div if the template handles the container.
        # But `highlighted_code` is the full HTML.
        
        # Original logic used `renderer_by_node` which returned content with &nbsp; and <br>
        # and then passed it to `mac_window_template.render(text=...)`.
        
        # If we pass raw HTML to template, we need to ensure template doesn't escape it?
        # Jinja2 autoescapes. We might need to mark it safe if passing to template?
        # But here we are calling render(text=...), if the template uses {{ text }}, it will be escaped.
        # We should pass it as a Markup object or ensure template uses {{ text|safe }}.
        # Since I cannot easily change all templates (there are many), I should assume they might escape.
        # BUT, the original `renderer_code.py` returned a string with HTML tags (<br>, &nbsp;, <span style...>)
        # and `styles_renderer.py` passed it to `self.mac_window_template.render(text=highlight_result)`.
        # Unless the `Environment` is configured with `autoescape=False`?
        # Mistune 2.0+ usually doesn't escape the output of renderer methods?
        # Wait, Jinja2 `Environment(loader=...)` defaults to `autoescape=False` for non-html extensions?
        # Or maybe it was False by default in older Jinja2?
        # I should check `themes.py` Env creation. I didn't set autoescape. Default is False for strings.
        
        template = self._get_template('mac_window')
        if template:
            return template.render(text=highlighted_code)
        
        # Fallback
        lang_class = f' class="language-{escape_html(lang)}"' if lang else ''
        return f'<pre><code{lang_class}>{escape(code)}</code></pre>\n'

    # 表格 (Simplified logic)
    def table(self, text):
        template = self._get_template('table')
        if template:
            # Mistune 2 passes table body/head differently? 
            # Wait, `plugin_table` in mistune 2.0a4 works by calling `table(text)`.
            # But `text` is the inner HTML of the table?
            # Original code used `etree` to parse `text` back to objects.
            # This is inefficient but necessary if we want to extract data to pass to template.
            # I will keep the original logic using lxml if possible.
            from lxml import etree
            try:
                # Wrap in table to make it valid XML for parsing
                full_table = f"<table>{text}</table>"
                table_selector = etree.HTML(full_table)
                ths = table_selector.xpath('//th')
                tds = table_selector.xpath('//td') # This might flatten rows?
                
                # We need to preserve rows.
                # Let's try to parse rows.
                rows = table_selector.xpath('//tr')
                # Header usually in first row?
                
                # Original code logic:
                # ths = table_selector.xpath('//tr/th')
                # tds = table_selector.xpath('//tr/td')
                # This seems to assume a flat list of ths and tds? 
                # And `table_template.render(row_count=len(ths), header_list=..., detail_list=...)`
                # This implies the template handles 1 header row and N data rows?
                # The `detail_list` seems to be all tds flattened?
                
                th_cell_list = []
                for value in ths:
                    style = value.attrib.get('style', '')
                    if style.startswith('text-align:'): style = style[11:]
                    th_cell_list.append(Cell(value.text, style))
                
                td_cell_list = []
                for value in tds:
                    style = value.attrib.get('style', '')
                    if style.startswith('text-align:'): style = style[11:]
                    td_cell_list.append(Cell(value.text, style))
                
                return template.render(row_count=len(ths), header_list=th_cell_list, detail_list=td_cell_list)
            except Exception as e:
                # print(f"Table parsing error: {e}")
                pass
        return text

    def header(self):
        template = self._get_template('header')
        return template.render() if template else ''

    def footer(self):
        template = self._get_template('footer')
        return template.render() if template else ''

    def background(self, text):
        template = self._get_template('background')
        return template.render(text=text) if template else text

    def thematic_break(self):
        return ''


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


def render_article(content, theme_data):
    """
    渲染文章
    """
    renderer = StyleRenderer(theme_data)
    markdown = mistune.create_markdown(renderer=renderer, plugins=[plugin_table])
    content_result = markdown(content)
    # Ensure all newlines are removed or handled to prevent extra spacing in WeChat
    # But we should trust the templates. The issue might be simply mistune adding newlines?
    # Mistune 2 adds newlines after blocks.
    return renderer.background(text=f'{renderer.header()}{content_result}{renderer.footer()}')

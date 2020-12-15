import os
from jinja2 import Environment, FileSystemLoader

# 创建一个包加载器对象(也可以使用PackageLoader包加载器的方式加载)
print(os.path.join(os.getcwd(), 'code'))
env = Environment(
    loader=FileSystemLoader(os.path.join(os.getcwd(), 'code')))
# 加载各类模板
mac_atom_one_dark = env.get_template('mac_atom_one_dark.html')


"""
目标：BeautifulSoup应用
作用：解析html
安装：pip install beautifulSoup4
导包：from bs4 import BeautifulSoup
"""
# 1、导包
from bs4 import BeautifulSoup
html_text = """
<html> 
    <head>
        <title>黑马程序员</title>
    </head> 
    <body>
        <p id="test01">软件测试</p>
        <p id="test02">2020年</p>
        <a href="/api.html">接口测试</a>
        <a href="/web.html">Web自动化测试</a> <a href="/app.html">APP自动化测试</a>
    </body>
</html>
"""
# 2、解析获取html对象
bs = BeautifulSoup(html_text, "html.parser")
# 3、获取整个标签
print(bs.title)
# 4、获取标签名
print(bs.title.name)
# 5、获取标签的值
print(bs.title.string)
# 6、获取属性
print(bs.p.get("id"))
# 7. 获取所有标签
print(bs.find_all("p"))
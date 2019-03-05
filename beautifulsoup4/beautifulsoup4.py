import bs4
from bs4 import BeautifulSoup

exampleFile = open('example.html','r',encoding='UTF-8')
exampleSoup = bs4.BeautifulSoup(exampleFile.read(), 'html5lib')
elems = exampleSoup.select('#author')
type(elems)
print(elems[0].getText())

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
tag = soup.a
tag.string = "New link text."
tag['href'] = "www.baidu.com"
print(tag)


html = '<img src="http://p1.pstatp.com/large/pgc-image/793019a3a9c046018c1a9b0903f34480" img_width="765" img_height="180" alt="实用！一整年的健康时刻表，适合贴在床头提醒自己过更健康的生活" inline="0">'
soup = BeautifulSoup(html, 'html.parser')
tag = soup.img
tag['src'] = '你要替换的路径'
print(tag)
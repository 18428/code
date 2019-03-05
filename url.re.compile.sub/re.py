
import re
pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+') # 匹配模式
html = '<img src="http://p1.pstatp.com/large/pgc-image/793019a3a9c046018c1a9b0903f34480" img_width="765" img_height="180" alt="实用！一整年的健康时刻表，适合贴在床头提醒自己过更健康的生活" inline="0">'

url = re.findall(pattern, html)
print(url)

out = re.sub(pattern, '要替换的路径', html)
print(out)
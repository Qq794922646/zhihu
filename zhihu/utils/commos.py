import hashlib
import re
def get_md5(url):
    if isinstance(url,str):
        url=url.encode('utf-8')
    m=hashlib.md5()
    m.update(url)
    return m.hexdigest()
def extract_num(text):
    # 从字符串中提取数字
    match_re=re.match('.*?(\d+).*',text)
    if match_re:
        nums=int(match_re.group(1))
    else:
        nums=0
    return nums
def question_content(str):
    if str=='显示全部':
        return '此处是显示全部所以无内容'
    else:
        return str

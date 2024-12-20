import json
import os
import re

import requests
from requests import get
from parsel import Selector
from tomd import Tomd
from re import sub
import datetime



def get_www(url):
    head = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76"
    }
    html = get(url=url, headers=head).text
    return html


def create_file_with_content():
    content = '''{"文件保存路径":"./","juejin.cn":[".article-title","#article-root"],"linux.cn":["#article_titl","#ct > div > article > div.d"],"cnblogs.com":["#cb_post_title_url > span","#cnblogs_post_body"],"weixin.qq.com":[".rich_media_title",".rich_media_content"],"zhuanlan.zhihu.com":["#root > div > main > div > article > header > h1","#root > div > main > div > article > div.Post-RichTextContainer"],"zhihu.com/question/":[".QuestionHeader-title",".RichContent-inner"],"csdn.net/":[".title-article","article"],"blog.51cto.com/":[".title > h1","#container"],"www.jianshu.com/":["h1","article"]}'''
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
            print(f"配置文件不存在，已创建 '{file_path}' ")
    else:
        print(f"成功加载配置文件")


def chose_selector(url):
    # 网站支持的选择器
    for tag, value in support_web.items():
        if tag in url:
            return value
    raise ModuleNotFoundError("该网站不在支持列表里")


def replacestr(text: str) -> str:
    # 删除多余的符号
    replace__str = {"&nbsp;": " ", "&lt;": "<", "&gt;": ">", "&amp;": "& ", "&quot;": '"', "&apos;": "'",
                    "<br.*?>": "\n", "<li>": "   ", "</li>": "   ", "</code><code>": "\n", 'data-src="': 'src="',
                    "</section>": "\n", "<section.*?>": "", " ": ""}
    for k, v in replace__str.items():
        try:
            text = re.sub(k, v, text)
        except Exception as e:
            print(e)
    return text





def get_md(url):
    # 根据URL选择合适的解析器
    kv = chose_selector(url)
    # 获取网页内容
    html = get_www(url)
    # 解析网页
    page = Selector(html)
    # 获取标题
    title_chose = kv[0]
    title = page.css(title_chose + "::text").get()  # 原始标题
    # 移除标题中的不支持字符（受限制文件名要求）
    for x in r' \/:*?？"<>|\n':
        title = title.replace(x, "")
    # 获取正文
    arctl_chose = kv[1]
    arctl = page.css(arctl_chose).get()  # 网页原文
    # 替换特殊字符
    arctl = replacestr(arctl)
    # 防盗链处理和图片插入
    arctl = sub("<(img.*?)>", r'<\1 referrerpolicy="no-referrer">\n\n', arctl)
    arctl = sub("style='.*?'", r'', arctl)
    arctl = sub('style=".*?"', r'', arctl)
    md_txt = Tomd(arctl).markdown
    md_txt = md_txt.replace("|------", "|------|------")
    with open(output_file, 'r', encoding='utf-8') as f:
        x = f.read()
        cabbc = json.loads(x)
        try:
            iii = cabbc[0].get('id')
            id = int(iii) + 1
        except Exception as e:
            id = 1
        print(id)
        xx = {
            "id": id,
            "title": title,
            "url": url,
            "content": md_txt,
            "labels": [],
            "created_at": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        cabbc.insert(0, xx)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cabbc, f, ensure_ascii=False, indent=2)

file_path = "file.json"
output_file = '../frontend/src/data/articles.json'

def geturl():
    response = requests.get("https://api.github.com/repos/kaozb/zero/issues?per_page=1")
    issues = response.json()
    title = issues[0].get('title')
    return title

if __name__ == '__main__':
    print()
    try:
        create_file_with_content()
        with open(file_path, 'r', encoding='utf-8') as file:
            support_web = json.load(file)
        savedir = support_web["文件保存路径"]
        url = geturl()# https://blog.csdn.net/OneFlow_Official/article/details/144124481
        get_md(url)

    except Exception as e:
        print(e)


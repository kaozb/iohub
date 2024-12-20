import json
import os
import re
from pyperclip import paste
from requests import get
from parsel import Selector
from tomd import Tomd
from re import sub

file_path = "file.json"


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
        # print(f"{k}\t{v}")
        # text = text.replace(k, v)
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
    # 转换为markdown格式
    md_txt = Tomd(arctl).markdown
    # 替换表格边框字符
    md_txt = md_txt.replace("|------", "|------|------").replace("\n", "")
    # 写入到文件
    # with open(r'Q:\\markdown\\docs\\T-采集\\' + title + ".md", mode="w", encoding="utf-8") as f:
    print(title)
    print(url)
    print(md_txt)
    id = 9999
    xx = {
        "id":id,
        "title":title,
        "url":url,
        "content":md_txt,


    }

'''
  {
    "id": 5705,
    "title": "【网站自荐】Cloudflare workers AI开发的ai聊天网站",
    "content": "\r\n一个使用Cloudflare workers AI提供聊天、图片生成、翻译等服务的简单网站，使用Nextjs+ ShadcnUi开发，由Cloudflare pages部署。代码开源，适合学习\r\n\r\n[网站地址](https://duyaxuan.xyz)\r\n[github地址](https://github.com/wuyangwang/my-chat-web)",
    "created_at": "2024-12-12T01:31:02Z",
    "labels": [],
    "url": "https://github.com/ruanyf/weekly/issues/5705"
  },
  '''
if __name__ == '__main__':
    try:
        create_file_with_content()
        input("复制网址后直接回车即可")
        while True:
            with open(file_path, 'r', encoding='utf-8') as file:
                support_web = json.load(file)
            savedir = support_web["文件保存路径"]
            url = paste()
            if url == "":
                print("剪切板为空")
                input("-" * 100)
                continue
            print(url)
            get_md(url)
            input("-" * 100)

    except Exception as e:
        print(e)
        input()

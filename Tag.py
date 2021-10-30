# -*- coding = utf-8 -*- 
# @Time :2021/10/24 23:22
# @Author: stach
# @File : Tag.by
# @Software: PyCharm

import urllib.request
from bs4 import BeautifulSoup

class NameTag:
    def __init__(self):  # 构造函数定义这个类的属性（变量）、函数
        self.open_net()
        self.scratch()

    def open_net(self):  # url 可不可以在主函数里面用全局变量去定义？
        url = 'https://book.douban.com/tag/?view=type'
        header = {}  # header 可不可以在主函数里面用全局变量去定义？
        header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
        req = urllib.request.Request(url, None, header)
        response = urllib.request.urlopen(req)
        html = response.read()
        return html

    def scratch(self):
        tag_dict = {}
        hhtml = BeautifulSoup(self.open_net(), "html.parser")

        title = hhtml.select('div div a h2')  # 第一步找到h2标签，因为更细致，a标签就找不到
        tag_list = []
        #print(title)
        # 然后通过h2标签找到爷爷级标签，就是div盒子了
        for i in title:
            a = i.find_parent()  # 找到父亲a标签
            div = a.find_parent()  # 找到父亲div
            tag_title = a.select('h2')[0].get_text()[:2]  # 找到h2标签取出内容并切片取出前两个字
            tags = div.select('tr td a')  # 找到td中的a标签
            #tag_list = []
            for j in tags:
                if(tag_title=="文化"):
                    tag_list.append("https://book.douban.com/tag/"+j.get_text())  # 循环取出a标签中的内容
                    tag_dict[tag_title] = tag_list
                    # html_for_tag="https://book.douban.com/tag/"+j.get_text()
                    # print(html_for_tag)
                    # tag_dict[tag_title] = tag_list
                else:
                    continue
        # for i in tag_dict:
        #     print(i + ':', end='')
        #     print(tag_dict[i])
        print (tag_list)


if __name__ == "__main__":
     NameTag()
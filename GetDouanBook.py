# -*- coding = utf-8 -*- 
# @Time :2021/10/24 19:27
# @Author: stach
# @File : GetDouanBook.by
# @Software: PyCharm

import urllib.request
from bs4 import BeautifulSoup

class GetAgent:#获取代理IP

    def __init__(self):  # 构造函数定义这个类的属性（变量）、函数

        self.IPlist = []
        self.open_net()
        self.scratch()

    def open_net(self):  # url 可不可以在主函数里面用全局变量去定义？

        req = urllib.request.Request(url, None, header)
        response = urllib.request.urlopen(req)
        html = response.read()
        return html

    def scratch(self):
        hhtml = BeautifulSoup(self.open_net(), "html.parser")
        hang = hhtml.findAll('tr')
        for each in range(0, len(hang)):
            try:
                lie = hang[each].findAll('td')
                # a=lie[0].text
                # b=lie[1].text
                # c=lie[1].text
                self.IPlist.append([lie[0].text[4:-2], lie[1].text[4:-2], lie[2].text[4:-2]])
            except:
                continue


class TestProxy:

    def __init__(self):
        self.test()

    def test(self):

        proxy_host = ip + ":" + port
        proxy_temp = {Type: proxy_host}

        proxy_support = urllib.request.ProxyHandler(proxy_temp)
        opener = urllib.request.build_opener(proxy_support)

        try:
            req = urllib.request.Request("https://www.baidu.com", None, header)
            response = opener.open(req)
            print(str(proxy_temp)+"可以登陆")
            Proxy_list.append(proxy_temp)
            # Proxy_list.append([Type,ip,port])
        except:
            print(str(proxy_temp)+"无法登陆")
            return

if __name__ == "__main__":

    header = {}  # header 可不可以在主函数里面用全局变量去定义？
    header[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'

    Proxy_list = []  # 保存可用的IP 地址
    #爬取代理IP并进行测试，测试函数将会把通过测试的代理IP存储到列表中仪表调用

    #爬取10页代理IP
    for i in range(1, 2):
        url = "https://www.89ip.cn/index_" + str(i) +'.html'
        shuchu1 = GetAgent()
        #print(shuchu1.IPlist)
        for ip, port, Type in shuchu1.IPlist:
            shuchu2 = TestProxy()
    print(Proxy_list)
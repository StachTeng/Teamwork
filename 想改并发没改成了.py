import time
import urllib.request
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import pandas as pd
import random
import threading

class Douban:
    def __init__(self):  # 构造函数定义这个类的属性（变量）、函数
        self.Book_Detail()
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
        Tag_list=[]
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
                    Tag_list.append(j.get_text())
                    tag_dict[tag_title] = tag_list
                    # html_for_tag="https://book.douban.com/tag/"+j.get_text()
                    # print(html_for_tag)
                    # tag_dict[tag_title] = tag_list
                else:
                    continue
        # for i in tag_dict:
        #     print(i + ':', end='')
        #     print(tag_dict[i])
        return Tag_list

    def GetBook(self, tag=None):
        url_t = "https://book.douban.com/tag/"  # /后面加标签名称，比如：日本文学
        url_tag = url_t + tag  # 组合成完整的网址
        print("当前书籍类别及网址", url_tag)
        bookdetails_result = []

        for i in range(1, 3, 1):  # 翻页,我们已经爬取了前面5页，还差45页，
            print("当前处于第" + str(i) + "页,正在获取网页源代码")
            url_tag = url_tag + "?start=" + str((i - 1) * 20) + "&type=T"

            # 配置浏览器IP代理设置
            chromeOptions = webdriver.ChromeOptions()
            print("正在配置网络代理，请稍后")
            current_ip = random.choice(Proxy_list)
            # chromeOptions.add_argument("--proxy-server=http://202.20.16.82:10152")
            chromeOptions.add_argument("--proxy-server=" + str(current_ip) + '"')
            print("当前IP：" + str(current_ip) + "  正在启动浏览器")

            explorer = webdriver.Chrome()  # 自动打开浏览器 模拟用户行为
            # 获取网页源代码
            explorer.get(url_tag)
            sc_book_details = explorer.page_source
            
            print(tag+str(i)+"获取网页源代码完毕！正在提取信息")

            # 以书为单位进行提取: 地址,书名, 作者，译者（如果有），出版社，出版日期，价格，评分，评价人数
            bookdetails_find = '<a href="(.*?)".*?title="(.*?)".*?<div class="pub">\n        \n  \n  (.*?)\n\n      </div>\n\n\n.*?<span class="rating_nums">(.*?)</span>.*?<span class="pl">\n        (.*?)\n    </span>\n  </div>\n\n\n\n'
            bookdetails_result = bookdetails_result + list(re.findall(bookdetails_find, sc_book_details, re.S))
            url_tag = url_t + tag
            # print("当前页提取完毕，系统正处于暂停期间")
            # time.sleep(1)  # 系统暂停活动10s
            explorer.quit()

        # 每搜索完一个类别，将信息保存在一个新的工作表内
        bookdetails = pd.DataFrame()
        bookdetails['Record'] = bookdetails_result
        bookdetails.to_excel("BookDetails22_" + str(tag) + ".xlsx")
        print("该类别图书信息保存完毕！\n")

    print("所有类别信息搜索完毕！")

    def Book_Detail(self):
        # TagNum= pd.read_excel("TagNum.xlsx", index_col= None)
        # BookTag= list(TagNum['Tag'])  #获取所有书的标签
        Tag_list= self.scratch()
        url_t = "https://book.douban.com/tag/"  # /后面加标签名称，比如：日本文学
        for i0 in range(1,9,1):
            if (i0==9):#分别爬取各个标签下的网址内容
                self.GetBook(Tag_list[1])
            else:
                i = i0*4
                tag1 = Tag_list[i]
                tag2 = Tag_list[i-1]
                tag3 = Tag_list[i-2]
                tag4 = Tag_list[i-3]

                print(tag4+tag3+tag2+tag1)
                print("------------------------"+str(i))

                aa=threading.Thread(target=self.GetBook, args=(tag1,))
                bb=threading.Thread(target=self.GetBook,args=(tag2,))
                cc=threading.Thread(target=self.GetBook,args=(tag3,))
                dd=threading.Thread(target=self.GetBook,args=(tag4,))


                aa.start()
                #time.sleep(3)
                bb.start()
                #time.sleep(20)
                cc.start()
                #time.sleep(5)
                dd.start()
                time.sleep(100+i0*600)

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
            print(str(proxy_temp)+"可以登陆")
            Proxy_list.append(proxy_temp)
            # Proxy_list.append([Type,ip,port])
        except:
            print(str(proxy_temp)+"无法登陆")
            return

if __name__ == "__main__":

    header = {}  # header 可不可以在主函数里面用全局变量去定义？
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'

    Proxy_list = []  # 保存可用的IP 地址
    #爬取代理IP并进行测试，测试函数将会把通过测试的代理IP存储到列表中仪表调用

    #爬取30页代理IP
    for i in range(75, 90):
        url = "https://www.89ip.cn/index_" + str(i) +'.html'
        shuchu1 = GetAgent()
        #print(shuchu1.IPlist)
        for ip, port, Type in shuchu1.IPlist:
            shuchu2 = TestProxy()
    print(Proxy_list)

    douban =Douban()#调用douban类爬取网页
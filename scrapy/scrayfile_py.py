#coding:utf-8

import urllib2
import urllib
import re
import time
import thread

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent ="Mozilla/4.0(compatible; MSIE 5.5;Windows NT)"
        self.headers = {'User-Agent':self.user_agent}
        self.stories = []

        self.enable =False

    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike/hot/page'+str(pageIndex)
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print(u'连接糗事百科失败，错误原因',e.reason)
                return
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print(u'出错了！')
            return
        pattern = re.compile('<div class="author clearfix">.*?href.*?<img src.*?title=.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?<i class="number">(.*?)</i>',re.S)
        items = re.findall(pattern,pageCode)
        pageStories = []
        for item in items:
            replaceBr = re.compile('<br/>')
            text = re.sub(replaceBr,'\n',item)
            pageStories.append([item[0].strip(),text.strip(),item.strip()])
            return pageStories
    def loadPage(self):

        if self.enable == True:
            if len(self.stories) < 2:
                #获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                #将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    #获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1

    #调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        #遍历一页的段子
        for story in pageStories:
            #等待用户输入
            input = raw_input()
            #每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            #如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t发布时间:%s\t赞:%s\n%s" %(page,story[0],story[2],story[3],story[1])

    #开始方法
    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        #使变量为True，程序可以正常运行
        self.enable = True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                #从全局list中获取一页的段子
                pageStories = self.stories[0]
                #当前读到的页数加一
                nowPage += 1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowPage)


spider = QSBK()
spider.start()
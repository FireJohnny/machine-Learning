# coding:utf-8

__author__ = 'FireJohnny'


class dict():
    def __init__(self):
        self.initial = {'A': 1, 'B': 2, 'C': 3}
        self.prefix = ''
        self.code =[]
        self.dictionary = self.initial
        self.dictionary1 = {}
        self.j = 3
        self.out = ''

    def enCode(self, char):#压缩
        print '输入的字符是：',char
        print '压缩过程：'
        self.prefix = char[0]#初始化
        #print self.prefix[0]
        for i in range(1,len(char)):
            self.prefix = self.prefix +char[i]#的到字符串
            self.prefix = self.dict(self.prefix)#放入字典与否

        self.out= self.out + str(self.dictionary[char[-1]])
        print char[-1],self.initial[char[-1]]
        print "压缩后的输出是：",self.out+' '

        print self.dictionary
        self.decode()

    def dict(self,char):
        if char not in self.dictionary.keys():#有没有
            temp = self.dictionary[char[0:-1]]
            self.j += 1
            self.dictionary[self.prefix]=self.j
            self.out = self.out + str(temp)
            print self.prefix," ",temp
            return char[-1]
        else:
            return char

    def decode(self):#解码
        for key ,value in self.dictionary.iteritems():
            self.dictionary1[value]=key
        print self.dictionary1
        print len(self.out)

        for t in range(len(self.out)):#
            self.code.append(self.dictionary1[int(self.out[t])])

        list= ''.join(self.code)

        print "对压缩的输出的解码：",list
dict_code = dict()
dict_code.enCode('ABABBABCABABBA')
#dict_code.enCode('ABBABABAC')



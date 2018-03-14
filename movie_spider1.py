import requests
import re
import random
import threading
import time
from lxml import etree

'''
环境Windows，python3.5
工具：pycharm，
此模块的目的是在线抓取国家新闻出版社广电总局全国电影剧本通知关于“记录影片”的数据

模块主要参数说明：
    urls 是存放父级的url列表
    USER_AGENTS 是保存请求头的列表
    Pro 是保存代理ip的列表
方法介绍：
    get_heard 是为了创建一个请求头
    get_por 是为了创建一个代理ip
    set_heard 设置url请求信息
    get_info 作为主线程获取以及保存信息
    get_url 获取父级url下的子url
    get_childinfo 获取子级url下的相关内容
    wirte_file 进行文件的读写
    
     
'''
#创建请求头列表
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
]

#创建代理IP列表
# Por = ['171.39.41.234','1.199.188.225','180.113.7.65','110.72.31.220',
#        '112.193.252.124','119.97.21.196','122.114.31.177','1.197.88.101']

def get_header():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }

# def get_pro():
#     return {
#         "http":random.choice(Por)
#     }


header = get_header()
# proxies = get_pro()
def set_header(url):
    # req = requests.get(url, headers=header, proxies=proxies)
    req = requests.get(url, headers=header)
    req.encoding = req.apparent_encoding
    return req

def middle(url):
    req = set_header(url)
    res = req.text
    selector = etree.HTML(res)
    content = selector.xpath('//div[@class="cc boxcontent"]/div/ul')
    pattern = re.compile('2017-0([8,9])-\w{2}')
    for text1 in content:
        text2 = etree.tostring(text1,encoding='utf-8').decode('utf8')
        l1 = re.findall(pattern,text2)
        print(l1)
        if l1:
            pass
        else:
            content.remove(text1)
    print(content)

    return content

def get_info(url):
    # try:
    if True:
        Res=middle(url)
        for res in Res:
            res = etree.tostring(res, encoding='utf-8').decode('utf8')
            child_url = get_url(res)  #获取备案公示标题的url
            my_info = get_childinfo(child_url)  #我要的信息
            str1 = re.search('2017-0([8,9])-\w{2}',res)
            wirte_file(str1,my_info)   #将想要的内容写入

        print('文件保存成功')
        # except:
        #     pass


def get_url(html):
    print(html)
    selector = etree.HTML(html)
    content = selector.xpath('//a/@href')
    return content


def get_childinfo(cont):
    for url in cont:
        url  = 'http://dy.chinasarft.gov.cn'+url
        time.sleep(0.1)  #防止访问太快
        req = set_header(url)
        res = req.content.decode(req.encoding)
        apttern = '<span id="span(\w)" class="announcebg"[\s\S].*纪录影片'
        str2 = re.search(apttern,res).group()
        num= re.search('\d',str2).group()
        selector = etree.HTML(res)
        re1 = '//div[@id="divf%s"]'%str(num)
        content = etree.tostring(selector.xpath(re1)[0],encoding='urf-8').decode('utf8')
        return content

def wirte_file(str,html):
    file = '%s月‘记录电影’.html'%str
    with open(file,'ab') as f:
        f.write(html)
        f.close()

urls = ['http://dy.chinasarft.gov.cn/shanty.deploy/catalog.nsp?id=0129dffcccb1015d402881cd29de91ec&pageIndex=2',]

if __name__ == '__main__':
    for url in urls:
        for i in range(5):
            t = threading.Thread(target=get_info,args=(url,))
            t.start()

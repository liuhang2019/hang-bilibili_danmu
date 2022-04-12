import requests
import re
import time
from selenium import webdriver
from time import sleep
from lxml import etree

data = input("请输入你需要查找的内容：")
num =  int(input("请输入爬取页数："))
list = []
wd = webdriver.Chrome(executable_path='D:/Apycharm/pachong/chromedriver_win32/chromedriver.exe')#,chrome_options=chrome_options, options=option)
for i in range(1, num+1):
    wd.get('https://search.bilibili.com/video?keyword='+data+'&page='+str(i))
    sleep(1)
    page_text = wd.page_source
    tree = etree.HTML(page_text)
    trrr = tree.xpath('/html/body/div[3]/div[1]/div[1]/div[2]/div/div/div[1]/div')
    print("-----------------------第%i页爬取成功正在存入列表--------------------" % i)
    for li in trrr:
        link = li.xpath('./div/div[2]/a/@href')[0]
        links = 'https:' + link
        links = links.replace('www.','www.i')
        if links not in list:
            list.append(links)
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chromeh/81.0.4044.138 Safari/537.36'
}
for url in list:
    response = requests.get(url=url, headers=header)
    treee = etree.HTML(response.text)
    url = treee.xpath('/html/body/div[1]/div/div/div/div/div[1]/div[2]/div[5]/input/@value')[0]
    response = requests.get(url=url,headers=header)
    response.encoding = "utf-8"
    content_list = re.findall('<d p=".*?">(.*?)</d>', response.text)
    print(url, '弹幕爬取成功')
    for index in content_list:
        with open('bilibili_data.txt',mode='a',encoding='utf-8') as f:
            f.write(index)
            f.write('\n')

#/usr/bin/env python
#-*- coding:utf-8 -*-

from time import sleep

import requests
from bs4 import BeautifulSoup

headers = {

    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate',
    'Upgrade-Insecure-Requests':'1',
}

url = 'https://cassandra.cerias.purdue.edu/CVE_changes/today.html'

def get_cve_urls():

    '''获取最新的cve漏洞url地址'''

    start_content = 'New entries' # 起始字符串
    end_content = 'Graduations'

    response = requests.get(url, headers=headers, timeout=60)
    response = str(response.text)
    start_index = response.index(start_content)

    if start_index >= 0:
        start_index += len(start_content)
        end_index = response.index(end_content)
        cve_urls_content = response[start_index:end_index]  # 获取网页的指定范围
        soup = BeautifulSoup(cve_urls_content,'lxml')

        cve_url_lists = []     # 存放获取到的cve url

        for u in soup.find_all('a'):
            cve_url = u["href"]
            cve_url_lists.append(cve_url)

        return cve_url_lists

def get_cve_info():

    '''获取最新cve漏洞信息'''

    print '[*] 最新cve漏洞信息：\n'
    sleep(2)
    cve_urls = get_cve_urls()

    for cve_url in cve_urls:
        response = requests.get(cve_url,headers=headers,timeout=60)
        response = response.text
        soup = BeautifulSoup(response,'lxml')

        table = soup.find("div",id="GeneratedTable").find("table")    # 获取table标签内容
        cve_id = table.find_all("tr")[1].find("td",nowrap="nowrap").find("h2").string   # cve id
        cve_description = table.find_all("tr")[3].find("td").string       # cve 介绍

        print "[+] 漏洞url：",cve_url
        print "[+] cve漏洞编号：",cve_id
        print "[+] 漏洞介绍:",cve_description


def main():
    get_cve_info()

if __name__ == "__main__":
    main()

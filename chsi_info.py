#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
"""
作者：金鹏
时间：2018-06-14
用途：爬取学信网(http://www.chsi.com.cn/)中“高校招生信息服务”板块下的“院校库”、“往年录取分数”
安装：  pip install lxml
        pip install bs4
步骤：1、爬取 院校库（http://gaokao.chsi.com.cn/sch/search--ss-on,option-qg,searchType-1,start-0.dhtml）
        获取 院校名称，院校所在地，院校隶属，院校类型，学历层次，院校特性，研究生院，满意度
      2、爬取 往年录取分数（http://gaokao.chsi.com.cn/lqfs/）
        根据 考生来源、院校名称，参考年份，科类
        获取 录取批次，录取线差，省市分数线，高校平均分，专业平均分（门类、专业名称、平均分），专业录取线差
      3、爬取 各省历年分数线
        http://gaokao.chsi.com.cn/z/gkbmfslq2014/pcx.jsp
        http://gaokao.chsi.com.cn/z/gkbmfslq2015/pcx.jsp
        http://gaokao.chsi.com.cn/z/gkbmfslq2016/pcx.jsp
        http://gaokao.chsi.com.cn/z/gkbmfslq2017/pcx.jsp
"""

import logging

logging.basicConfig(filename='./log.log',
                    format='[%(asctime)s -%(name)s-%(levelname)s-%(funcName)s]%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.DEBUG)
log = logging.getLogger('chsi_info')
sh = logging.StreamHandler()
sh.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s -%(name)s-%(levelname)s-%(funcName)s]%(message)s')
sh.setFormatter(formatter)
log.addHandler(sh)


def get_html(url):
    """
    爬取 页面内容
    """

    log.info("开始 ...")

    from urllib import request
    response_result = request.urlopen(url).read()
    html = response_result.decode('utf-8')

    log.info("结束 。")
    return html


def get_soup(url):
    """
    返回 soup 对象
    """

    log.info("开始 ...")

    from bs4 import BeautifulSoup
    html = get_html(url)
    # soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(html, 'lxml')
    # print(soup.prettify())

    log.info("结束 。")
    return soup


def get_yxk():
    """
    获取 院校库 页面内容
    """

    log.info("开始 ...")
    import time

    # 第一页地址，每页20个院校，url后缀从0开始，间隔20递增
    # url = 'http://gaokao.chsi.com.cn/sch/search--ss-on,option-qg,searchType-1,start-0.dhtml'
    # url = 'http://gaokao.chsi.com.cn/sch/search--ss-on,option-qg,searchType-1,start-20.dhtml'
    # ...
    # url = 'http://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-2700.dhtml'
    # 最后一页地址
    # url = 'http://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-2720.dhtml'

    all_content = ''
    for url_index in range(0, 40, 20):
        url = 'http://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-' + str(url_index) + '.dhtml'

        soup = get_soup(url)

        trs = soup.table.find_all('tr')
        trs_len = len(trs)

        for tr_index in range(0, trs_len):
            if (0 == tr_index) and (0 == url_index):
                tag_name = 'th'
            else:
                tag_name = 'td'

            tds = trs[tr_index].find_all(tag_name)
            if 0 < len(tds):
                all_content = all_content + "\r\n" + str(url_index) + ':' + str(tr_index) + ' '
                i = 0
                for td in tds:
                    info = ''
                    i += 1
                    for text in td.strings:
                        info = info + ' ' + text.strip()

                    for a in td.find_all('a'):
                        href = a.get('href')
                        if href.startswith('/sch/'):
                            info = info + ' ' + href.strip()

                    all_content = all_content + "\t" + info.strip()

        msg = 'url_index = ' + str(url_index) + ', trs_len = ' + str(trs_len)
        log.info(msg)
        time.sleep(1)

    log.info("结束 。")
    return all_content


def main():
    """
    主程序
    """

    log.info("开始 ...")

    # 1、爬取 院校库（http://gaokao.chsi.com.cn/sch/search--ss-on,option-qg,searchType-1,start-0.dhtml）
    #    获取 院校名称，院校所在地，院校隶属，院校类型，学历层次，院校特性，研究生院，满意度
    yxk = get_yxk()
    print(yxk)

    log.info("结束 。")


if __name__ == '__main__':
    main()

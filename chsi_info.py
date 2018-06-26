#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
"""爬取学信网(http://www.chsi.com.cn/)中“高校招生信息服务”板块下的“院校库”、“往年录取分数”
作者：金鹏
时间：2018-06-14
用途：爬取学信网(http://www.chsi.com.cn/)中“高校招生信息服务”板块下的“院校库”、“往年录取分数”
安装：pip install lxml
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
import time

from urllib import request
from bs4 import BeautifulSoup


logging.basicConfig(filename='./log.log',
                    format='[%(asctime)s] [%(name)s] [%(levelname)s] [%(funcName)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)
log = logging.getLogger('chsi_info')
sh = logging.StreamHandler()
sh.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] [%(funcName)s] %(message)s')
sh.setFormatter(formatter)
log.addHandler(sh)


def docstring():
    """文档说明"""
    return __doc__ % globals()


def get_html(url):
    """爬取 页面内容"""
    log.info("开始 ...")

    response_result = request.urlopen(url).read()
    html = response_result.decode('utf-8')

    log.info("结束 。")
    return html


def get_soup(url):
    """返回 soup 对象"""
    log.info("开始 ...")

    html = get_html(url)
    # soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(html, 'lxml')
    # print(soup.prettify())

    log.info("结束 。")
    return soup


def get_yxk():
    """获取 院校库 页面内容"""
    log.info("开始 ...")

    # 第一页地址，每页20个院校，url后缀从0开始，间隔20递增
    # url = 'http://gaokao.chsi.com.cn/sch/search--ss-on,option-qg,searchType-1,start-0.dhtml'
    # url = 'http://gaokao.chsi.com.cn/sch/search--ss-on,option-qg,searchType-1,start-20.dhtml'
    # ...
    # url = 'http://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-2700.dhtml'
    # 最后一页地址
    # url = 'http://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-2720.dhtml'

    all_content = ''
    url_begin = 0
    url_end = 40 #2740
    url_step = 20
    for url_index in range(url_begin, url_end, url_step):
        url = 'http://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-' + str(url_index) + '.dhtml'

        soup = get_soup(url)

        trs = soup.table.find_all('tr')
        trs_len = len(trs)

        for tr_index in range(0, trs_len):
            # if (0 == tr_index) and (0 == url_index):
            #     tag_name = 'th'
            # else:
            #     tag_name = 'td'
            tag_name = 'td'

            tds = trs[tr_index].find_all(tag_name)
            if 0 < len(tds):
                all_content = all_content + str(url_index) + ',' + str(tr_index)
                for td in tds:
                    info = ''
                    for text in td.strings:
                        t = text.strip()
                        if '' != t:
                            info = info + ',' + t

                    for a in td.find_all('a'):
                        href = a.get('href')
                        if href.startswith('/sch/'):
                            sch_id = href.replace('/sch/schoolInfo--schId-', '')
                            sch_id = sch_id.replace('.dhtml', '')
                            info = info + ',' + sch_id
                            info = info + ',' + 'http://gaokao.chsi.com.cn' + href
                            info = info + ',' + 'http://gaokao.chsi.com.cn/sch/schoolInfoMain.do?schId=' + sch_id + '&ssdm=44&lqfsyear=2014&kldm=5#lqfs'
                            info = info + ',' + 'http://gaokao.chsi.com.cn/sch/schoolInfoMain.do?schId=' + sch_id + '&ssdm=44&lqfsyear=2015&kldm=5#lqfs'
                            info = info + ',' + 'http://gaokao.chsi.com.cn/sch/schoolInfoMain.do?schId=' + sch_id + '&ssdm=44&lqfsyear=2016&kldm=5#lqfs'
                            info = info + ',' + 'http://gaokao.chsi.com.cn/sch/schoolInfoMain.do?schId=' + sch_id + '&ssdm=44&lqfsyear=2017&kldm=5#lqfs'

                    all_content = all_content + info.strip()
                all_content = all_content + "\r\n"

        msg = 'url_index = ' + str(url_index) + ', trs_len = ' + str(trs_len)
        log.info(msg)
        time.sleep(1)

    log.info("结束 。")
    return all_content


def main():
    """主程序"""
    log.info("开始 ...")

    # print(docstring())
    # 1、爬取 院校库（http://gaokao.chsi.com.cn/sch/search--ss-on,option-qg,searchType-1,start-0.dhtml）
    #    获取 院校名称，院校所在地，院校隶属，院校类型，学历层次，院校特性，研究生院，满意度
    yxk = get_yxk()
    open('yxk-utf8.csv', 'wb').write(yxk.encode('UTF-8'))
    open('yxk-gb18030.csv', 'wb').write(yxk.encode('GB18030'))

    log.info("结束 。")
    return


if __name__ == '__main__':
    main()

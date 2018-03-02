#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
"""
作者：金鹏
时间：2018-03-02
用途：调整 Windows 下产生的 GB2312 文件编码为 UTF-8，脚本需要放到待调整文件的目录中
"""

import logging
logging.basicConfig(filename='log.log',
                    format='[%(asctime)s -%(name)s-%(levelname)s-%(module)s]%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.DEBUG)
log = logging.getLogger('arno')
sh = logging.StreamHandler()
sh.setLevel(level = logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s -%(name)s-%(levelname)s-%(module)s]%(message)s')
sh.setFormatter(formatter)
log.addHandler(sh)

# 改变文件编码
def change_file_encoding():
    log.info("改变文件编码 开始 ...")

    import os

    path = os.getcwd()

    file_list = os.listdir(path)
    for f in file_list:
        file_name = os.path.join(path, f)
        if file_name[-4:] == '.txt':
            log.info(file_name)

            file_content = open(file_name, 'rb').read().decode('GB2312','strict')
            new_file_name = file_name \
                .replace('（新）-SQL', '') \
                .replace('-SQL', '') \
                .replace('.txt','.sql')
            log.info(new_file_name)

            open(new_file_name, 'wb').write(file_content.encode("UTF-8"))

    log.info("改变文件编码 结束 。")

# 主程序
if __name__ == '__main__':
    log.info("主程序 开始 ...")
    change_file_encoding()
    log.info("主程序 结束 。")
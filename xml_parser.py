# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : xml_parser.py
# Time       : 2022/4/26 22:26
# Author     : lizy
# Email      : lizy0327@gmail.com
# Version    : python 3.9
# Software   : PyCharm
# Description: Welcom!!!
"""

import csv
import os
import time

import xml.etree.ElementTree as ET

from xml.etree.ElementTree import parse

# import pandas as pd

# namespaces = {'ns': 'raml20.xsd'}


def parser_xml():
    # 返回含有字典的列表数据
    res_list = []

    # file_path = str("D:\\tmp\\xmldata.xml").replace("\\", "/")
    file_path = str("D:\\tmp\\test.xml").replace("\\", "/")
    # file_path = str("D:\\tmp\\demo.xml").replace("\\", "/")
    # file_path = str("D:\\tmp\\b.xml").replace("\\", "/")
    # file_path = str("D:\\tmp\\csdn.xml").replace("\\", "/")
    print(file_path)
    tree = ET.parse(file_path)
    print(tree)
    # 根节点
    root = tree.getroot()
    # 标签名
    print('root_tag:', root)
    # print("------------------------")

    # 初始化System字典
    sys_dict = {}
    sys_dict['Provider Name'] = root[0][0][0].attrib['Name']
    sys_dict['Provider Guid'] = root[0][0][0].attrib['Guid'][1:-1]
    sys_dict['EventID'] = root[0][0][1].text
    sys_dict['EventName'] = root[0][0][2].text
    sys_dict['Version'] = root[0][0][3].text
    sys_dict['Source'] = root[0][0][4].text
    sys_dict['Level'] = root[0][0][5].text
    sys_dict['Opcode'] = root[0][0][6].text
    sys_dict['Keywords'] = root[0][0][7].text
    sys_dict['Result'] = root[0][0][8].text
    sys_dict['TimeCreated SystemTime'] = root[0][0][9].attrib['SystemTime']
    sys_dict['Channel'] = root[0][0][11].text
    sys_dict['Computer'] = root[0][0][12].text
    sys_dict['ComputerUUID'] = root[0][0][13].text

    # for key, values in sys_dict.items():
    #     print(key, values)

    evt_list = []
    for events in root:
        evt_dict = {}

        evt_dict['SubjectIP'] = events[1][0].text
        evt_dict['IPVersion'] = events[1][0].attrib['IPVersion']
        evt_dict['Name'] = events[1][1].attrib['Name']

        print(events[1][1].attrib)
        evt_dict['Uid'] = events[1][1].attrib['Uid']
        evt_dict['Gid'] = events[1][1].attrib['Gid']
        evt_dict['Local'] = events[1][1].attrib['Local']

        evt_dict['SubjectUserSid'] = events[1][2].text
        evt_dict['SubjectUserIsLocal'] = events[1][3].text
        evt_dict['SubjectDomainName'] = events[1][4].text
        evt_dict['SubjectUserName'] = events[1][5].text
        evt_dict['ObjectServer'] = events[1][6].text

        evt_dict['ObjectType'] = events[1][7].text
        evt_dict['HandleID'] = events[1][8].text
        evt_dict['ObjectName'] = events[1][9].text
        evt_dict['InformationRequested'] = events[1][10].text

        # 把解析的字典格式的数据，添加到list当中
        evt_list.append(evt_dict)

        # 在list中，每一条list记录都包含sys_dict和evt_dict这2条记录，其中sys_dict字典内容全部相等
        res_list.append({**sys_dict, **evt_dict})

    return res_list


def write_csv(report_name, res_list, report_path: str = None):
    '''
    根据性能数据list内容，写入到本地文件中
    :param report_file_name: 要写入的csv文件名称
    :param res_list: 需要写入的性能数据（list）
    :return: null
    '''
    # 默认情况下报告的目录放在python工程的同级目录下
    # if report_path is not None:
    #     report_path = os.path.abspath(os.path.join(report_path.replace("\\", "/"), ".."))
    # else:
    os.path.abspath(report_path.replace("\\", "/"))
    fileheader = res_list[0]
    path = os.path.join(report_path, report_name)
    print(path)
    with open(path, "w+", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fileheader)
        writer.writeheader()
        writer.writerows(res_list)


if __name__ == '__main__':
    file_path = "D:\\tmp\\"
    csv_name = 'report1.csv'
    res_list = parser_xml()
    write_csv(csv_name, res_list, report_path=file_path)
    # print(len(abc))
    # print(abc[0])
    # print(abc[1])
    # print(abc[2])
    # print(abc[1])
    # print(abc[1])
    pass





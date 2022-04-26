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
import xml.etree.ElementTree as ET
# import pandas as pd


def parser_xml():
    # 返回含有字典的列表数据
    res_list = []

    # file_path = str("D:\\tmp\\xmldata.xml").replace("\\", "/")
    # file_path = str("D:\\tmp\\test.xml").replace("\\", "/")
    file_path = str("D:\\tmp\\lizy-demo.xml").replace("\\", "/")
    # file_path = str("D:\\tmp\\b.xml").replace("\\", "/")
    # file_path = str("D:\\tmp\\csdn.xml").replace("\\", "/")
    print(file_path)
    tree = ET.parse(file_path)
    # 根节点
    root = tree.getroot()
    # 标签名
    print('root_tag:', root)

    evt_list = []
    # 得到event对象
    for events in root:
        evt_dict = {}

        # print(events.tag)
        # print(events.attrib)
        # 得到event里面system和eventdata对象
        for event in events:
            # print(event.tag[51:])
            # print(event.attrib)

            '''
            得到systemc和eventdata对象
            xml对象总共有3种属性：
            Tag： 使用<和>包围的部分，如<rank>成为start-tag，</rank>是end-tags；
            Tag结果是一个字符串。
            Element：被Tag包围的部分，如<rank>68</rank>，可以认为是一个节点，它可以有子节点。element的值通过element.text获得
            Attribute：在Tag中可能存在的name/value对，如<country name="Liechtenstein">中的name="Liechtenstein"，一般表示属性。
            Attribute结果是一个字典。
            '''
            for item in event:
                print("tag: ", item.tag[51:])
                if item.attrib and item.text:
                    print("attrib: ", item.attrib, type(item.attrib))
                    print('-----dict-----')
                    for k, v in item.attrib.items():
                        print(k,v)
                    print("element: ", item.text)
                elif item.attrib:
                    print("attrib: ", item.attrib, type(item.attrib))
                    print('-----dict-----')
                    for k, v in item.attrib.items():
                        print(k,v)
                elif item.text:
                    print("element: ", item.text)
                # else:
                #     print(item.tag, "faild.")
            #     print("attrib: ", item.attrib)
                # print("element: ", item.attrib)

                # if not bool(item.attrib):
                #     print("text: ", item.text)
                # else:
                #     print("attrib: ", item.attrib, type(item.attrib))
                    # print(item.text)


        # system info
        # evt_dict['Provider Name'] = events[0][0].attrib['Name']
        # evt_dict['Provider Guid'] = events[0][0].attrib['Guid'][1:-1]
        # evt_dict['EventID'] = events[0][1].text
        # evt_dict['EventName'] = events[0][2].text
        # evt_dict['Version'] = events[0][3].text
        # evt_dict['Source'] = events[0][4].text
        # evt_dict['Level'] = events[0][5].text
        # evt_dict['Opcode'] = events[0][6].text
        # evt_dict['Keywords'] = events[0][7].text
        # evt_dict['Result'] = events[0][8].text
        # evt_dict['TimeCreated SystemTime'] = events[0][9].attrib['SystemTime']
        # evt_dict['Channel'] = events[0][11].text
        # evt_dict['Computer'] = events[0][12].text
        # evt_dict['ComputerUUID'] = events[0][13].text



        # event info
        # evt_dict['SubjectIP'] = events[1][0].text
        # evt_dict['IPVersion'] = events[1][0].attrib['IPVersion']
        # evt_dict['Name'] = events[1][1].attrib['Name']
        #
        # # print(events[1][1].attrib)
        # evt_dict['Uid'] = events[1][1].attrib['Uid']
        # evt_dict['Gid'] = events[1][1].attrib['Gid']
        # evt_dict['Local'] = events[1][1].attrib['Local']
        #
        # evt_dict['SubjectUserSid'] = events[1][2].text
        # evt_dict['SubjectUserIsLocal'] = events[1][3].text
        # evt_dict['SubjectDomainName'] = events[1][4].text
        # evt_dict['SubjectUserName'] = events[1][5].text
        # evt_dict['ObjectServer'] = events[1][6].text
        #
        # evt_dict['ObjectType'] = events[1][7].text
        # evt_dict['HandleID'] = events[1][8].text
        # evt_dict['ObjectName'] = events[1][9].text
        # evt_dict['InformationRequested'] = events[1][10].text

        # 把解析的字典格式的数据，添加到list当中
        evt_list.append(evt_dict)

        # 在list中，每一条list记录都包含sys_dict和evt_dict这2条记录，其中sys_dict字典内容全部相等
        res_list.append(evt_dict)

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
    # print(path)
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





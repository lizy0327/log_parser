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
import collections
import xml.etree.ElementTree as ET


# import pandas as pd


def parser_xml():
    # 返回含有字典的列表数据
    res_list = []
    file_path = str("D:\\tmp\\demo.xml").replace("\\", "/")
    # file_path = str("D:\\tmp\\xmldata.xml").replace("\\", "/")
    # file_path = str("D:\\tmp\\test.xml").replace("\\", "/")
    # file_path = str("D:\\tmp\\lizy-demo.xml").replace("\\", "/")
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
        # 声明一个严格按照key插入顺序排序的字典
        evt_dict = collections.OrderedDict()

        # 得到event里面system和eventdata对象
        for event in events:
            # print(event.tag[51:])
            # print(event.attrib)

            '''
            对system和eventdata对象进行遍历并把结果保存到字典中
            xml对象总共有3种属性：
            Tag： 使用<和>包围的部分，如<rank>成为start-tag，</rank>是end-tags；
            Tag结果是一个字符串。
            Element：被Tag包围的部分，如<rank>68</rank>，可以认为是一个节点，它可以有子节点。element的值通过element.text获得
            Attribute：在Tag中可能存在的name/value对，如<country name="Liechtenstein">中的name="Liechtenstein"，一般表示属性。
            Attribute结果是一个字典。
            '''
            for item in event:

                # 通过最原始的for循环读写数据保存数据，缺点是对EventData对象里Data tag的处理不够自动化
                # if item.tag[51:] == "Provider":
                #     evt_dict['Provider Name'] = item.attrib['Name']
                #     evt_dict['GUID'] = item.attrib['Guid']
                # if item.tag[51:] == "TimeCreated":
                #     evt_dict['TimeCreated SystemTime'] = item.attrib['SystemTime']
                # if item.tag[51:] == "Data" and item.attrib['Name'] == "SubjectIP":
                #     evt_dict['SubjectIP'] = item.text
                #     evt_dict['IPVersion'] = item.attrib['IPVersion']
                # if item.tag[51:] == "Data" and item.attrib['Name'] == "SubjectUnix":
                #     evt_dict['SubjectUnix'] = "SubjectUnix"
                #     evt_dict['UID'] = item.attrib['Uid']
                #     evt_dict['GID'] = item.attrib['Gid']
                #     evt_dict['Local'] = item.attrib['Local']
                # if item.tag[51:] == "Data" and item.attrib['Name'] == "SubjectUserSid":
                #     evt_dict['SubjectUserSid'] = item.text
                # if item.tag[51:] == "Data" and item.attrib['Name'] == "SubjectUserIsLocal":
                #     evt_dict['SubjectUserIsLocal'] = item.text
                # if item.tag[51:] == "Data" and item.attrib['Name'] == "SubjectDomainName":
                #     evt_dict['SubjectDomainName'] = item.text
                # if item.tag[51:] == "Data" and item.attrib['Name'] == "SubjectUserName":
                #     evt_dict['SubjectUserName'] = item.text
                # if item.tag[51:] == "Data" and item.attrib['Name'] == "ObjectServer":
                #     evt_dict['ObjectServer'] = item.text
                # if item.tag[51:] == "Data" and item.attrib['Name'] == "ObjectType":
                #     evt_dict['ObjectType'] = item.text
                # if item.tag[51:] == "Data" and item.attrib['Name'] == "HandleID":
                #     evt_dict['HandleID'] = item.text
                # if item.tag[51:] == "Data" and item.attrib['Name'] == "ObjectName":
                #     evt_dict['ObjectName'] = item.text
                # if item.tag[51:] == "Data" and item.attrib['Name'] == "InformationRequested":
                #     evt_dict['InformationRequested'] = item.text
                # # 对于tag里只有element没有attrib的xml对象处理
                # if item.tag[51:] not in ["Data", "Provider", "TimeCreated", "Correlation", "Security"]:
                #     # print(item.tag[51:], item.text)
                #     evt_dict[item.tag[51:]] = item.text

                '''
                EventData对象的tag全部是Data，没法区分不同的字段
                在EventData对象的子节点里有2个比较特殊的字段，attrib有多个值，这2个需要特殊处理
                <Data Name="SubjectIP" IPVersion="4">10.128.61.231</Data>
                <Data Name="SubjectUnix" Uid="65534" Gid="65534" Local="false"/>
                '''
                if item.tag[51:] == "Data":
                    if item.attrib['Name'] == "SubjectIP":
                        evt_dict['SubjectIP'] = item.text
                        evt_dict['IPVersion'] = item.attrib['IPVersion']
                    elif item.attrib['Name'] == "SubjectUnix":
                        evt_dict['SubjectUnix'] = "SubjectUnix"
                        evt_dict['UID'] = item.attrib['Uid']
                        evt_dict['GID'] = item.attrib['Gid']
                        evt_dict['Local'] = item.attrib['Local']
                    else:
                        '''
                        EventData子节点的tag全部都是Data无法进行区分
                        子节点的attrib是一个字典格式，而且字典的key也都是Name，这个不需要
                        最终需要的数据是以：子节点attrib的value作为“key",子节点element作为"value"进行存储
                        示例：<Data Name="SubjectUserIsLocal">false</Data>
                        '''
                        for v in item.attrib.values():
                            evt_dict[v] = item.text
                else:
                    '''
                    在System对象的子节点里有2个比较特殊的字段，只有attrib，没有element，需要特殊处理，示例：
                    <Provider Name="NetApp-Security-Auditing" Guid="{3CB2A168-FE19-4A4E-BDAD-DCF422F13473}"/>
                    '''
                    if item.tag[51:] == "Provider":
                        evt_dict['Provider Name'] = item.attrib['Name']
                        evt_dict['GUID'] = item.attrib['Guid']
                    elif item.tag[51:] == "TimeCreated":
                        evt_dict['TimeCreated SystemTime'] = item.attrib['SystemTime']
                    else:
                        evt_dict[item.tag[51:]] = item.text

                # if item.attrib and item.text:
                #     print("attrib: ", item.attrib, type(item.attrib))
                #     print('-----dict-----')
                #     for k, v in item.attrib.items():
                #         print(k, v)
                #     print("element: ", item.text)
                # elif item.attrib:
                #     print("attrib: ", item.attrib, type(item.attrib))
                #     print('-----dict-----')
                #     for k, v in item.attrib.items():
                #         print(k, v)
                # elif item.text:
                #     print("element: ", item.text)


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
    pass

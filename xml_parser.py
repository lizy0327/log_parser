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
import collections
import xml.etree.ElementTree as ET


def parser_event_type(xml_path):
    """
    分析日志文件里共有多少种类型的日志
    :param xml_path: 要处理的xml文件路径
    :return: 包含所有事件类型的list列表
    """
    tree = ET.parse(xml_path)
    # 根节点
    root = tree.getroot()
    # 保存事件类型的list
    dct_type = []
    # 得到event对象合集
    for events in root:
        # print(events.tag)
        # print(events[0][1].text)
        # print(events[0][2].text)
        if events[0][2].text not in dct_type:
            dct_type.append(events[0][2].text)
    print(f"There has {len(dct_type)} type events,as the follows:")
    # 直接打印事件类型
    for d_type in dct_type:
        print(d_type)
    return dct_type


def parser_xml(xml_path):
    """
    分析xml文件，把每一条数据全部转换成字典类型的数据，并把所有的字典数据存放到一个大的list中
    :param xml_path: 要处理的xml文件路径
    :return: 所有事件的list集合
    """

    tree = ET.parse(xml_path)
    # 根节点
    root = tree.getroot()
    # 标签名
    # print('root_tag:', root)
    # 存放所有字典数据的list
    events_list = []

    # 得到event对象合集
    for events in root:
        # 声明一个严格按照key插入顺序排序的字典
        dct_name = collections.OrderedDict()
        # 得到一个完整的Event，遍历出System和EventData
        for event in events:
            # 分别对System和EventData进行遍历，并把数据存储到字典中
            for item in event:
                """
                EventData对象的tag全部是Data，没法区分不同的字段
                在EventData对象的子节点里有3个比较特殊的字段，attrib有多个值，
                Object类型事件：<Data Name="SubjectIP" IPVersion="4">10.128.61.231</Data>
                Object类型事件：<Data Name="SubjectUnix" Uid="65534" Gid="65534" Local="false"/>
                Logon类型事件：<Data Name="IpAddress" IPVersion="4">10.128.61.232</Data>
                """
                # 处理EventData节点数据
                if item.tag[51:] == "Data":
                    # Object相关的事件
                    if item.attrib['Name'] == "SubjectIP":
                        dct_name['SubjectIP'] = item.text
                        dct_name['IPVersion'] = item.attrib['IPVersion']
                    # Object相关的事件
                    elif item.attrib['Name'] == "SubjectUnix":
                        dct_name['SubjectUnix'] = "SubjectUnix"
                        dct_name['UID'] = item.attrib['Uid']
                        dct_name['GID'] = item.attrib['Gid']
                        dct_name['Local'] = item.attrib['Local']
                    # Logon相关的事件
                    elif item.attrib['Name'] == "IpAddress":
                        dct_name['IpAddress'] = item.text
                        dct_name['IPVersion'] = item.attrib['IPVersion']
                    else:
                        """
                        EventData子节点的tag全部都是Data无法进行区分
                        子节点的attrib是一个字典格式，而且字典的key也都是Name，这个不需要
                        最终需要的数据是以：子节点attrib的value作为“key",子节点element作为"value"进行存储
                        示例：<Data Name="SubjectUserIsLocal">false</Data>
                        """
                        for v in item.attrib.values():
                            dct_name[v] = item.text
                # 处理System节点数据
                else:
                    """
                    在System对象的子节点里有2个比较特殊的字段，只有attrib，没有element，需要特殊处理，示例：
                    <Provider Name="NetApp-Security-Auditing" Guid="{3CB2A168-FE19-4A4E-BDAD-DCF422F13473}"/>
                    """
                    if item.tag[51:] == "Provider":
                        dct_name['Provider Name'] = item.attrib['Name']
                        dct_name['GUID'] = item.attrib['Guid']
                    elif item.tag[51:] == "TimeCreated":
                        dct_name['TimeCreated SystemTime'] = item.attrib['SystemTime']
                    else:
                        dct_name[item.tag[51:]] = item.text
        events_list.append(dct_name)
    return events_list


def write_csv(report_name, event_list, report_path: str = None):
    """
    根据性能数据list内容，写入到本地文件中
    :param report_name: 要写入的csv文件名称，不带csv后缀
    :param event_list: 需要写入的性能数据（list列表，其中包含一条或多条字典类型的数据）
    :param report_path: 文件写入路径
    :return: null
    """
    # 默认情况下报告的目录放在python工程的同级目录下
    # if report_path is not None:
    #     report_path = os.path.abspath(os.path.join(report_path.replace("\\", "/"), ".."))
    # else:
    os.path.abspath(report_path.replace("\\", "/"))
    full_path = os.path.join(report_path, report_name)
    file_header = event_list[0]
    # 如果存在同名的报告文件，则生成新的报告文件，并在文件末尾增加时间戳
    if os.path.exists(full_path + ".csv"):
        # random_stamp = str(random.sample(range(0, 9999999), 1)[0])[:3]
        time_stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        new_path = os.path.join(full_path + "_" + time_stamp)
        with open(new_path + ".csv", "w+", newline="") as fp:
            writer = csv.DictWriter(fp, fieldnames=file_header)
            writer.writeheader()
            writer.writerows(event_list)
    else:
        with open(full_path + ".csv", "w+", newline="") as fp:
            writer = csv.DictWriter(fp, fieldnames=file_header)
            writer.writeheader()
            writer.writerows(event_list)


def archive_dct(dct_list, report_path):
    """
    根据EventName对字典进行分类，并生成不同的csv报告
    :param dct_list:未分类前的所有字典
    :param report_path:报告保存路径
    :return:
    """
    new_evt_dict = {}
    # 对所有字典进行分类
    for dct in dct_list:
        if dct['EventName'] in new_evt_dict:
            new_evt_dict[dct['EventName']].append(dct)
        else:
            new_evt_dict[dct['EventName']] = [dct]

    # 调用write_csv生成事件csv报告，其中以key(即EventName)作为报告名称，csv里内容为字典里的value
    for k, v in new_evt_dict.items():
        write_csv(report_name=k, event_list=v, report_path=report_path)


if __name__ == '__main__':
    # file_path = str("D:\\tmp\\demo.xml").replace("\\", "/")
    file_path = str("D:\\tmp\\xmldata.xml").replace("\\", "/")
    # file_path = str("D:\\tmp\\all_type.xml").replace("\\", "/")
    # file_path = str("D:\\tmp\\lizy-demo.xml").replace("\\", "/")
    # file_path = str("D:\\tmp\\b.xml").replace("\\", "/")
    # file_path = str("D:\\tmp\\csdn.xml").replace("\\", "/")
    parser_event_type(xml_path=file_path)
    all_evt_list = parser_xml(xml_path=file_path)
    archive_dct(all_evt_list, report_path="D:\\tmp\\123")

    pass

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

# 一个分析xml日志文件的小工具，使用此工具会把相同的EventName类型的日志保存到同一个csv文件中。
# 此工具还提供了分析xml里有几种EventName类型的事件的方法：parser_event_type
# 此工具暂时只支持python3
# 工具使用：
# 1.使用时命令行如下：python3 xml_parser.py <xml_file or xml_dir> [output csv dir]
# 第一个参数可以是xml文件路径，也可以是包含xml文件类型的文件夹（必选参数）
# 第二个参数是解析后csv文件保存目录（可选参数），如果省略的话会在xml文件（或目录）同级下创建以时间戳为后缀的同名文件（或目录）
# Copyright LiZhaoYang

import sys
import csv
import os
import time
import collections
import xml.etree.ElementTree as ET

version = 0.9


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


"""
xml对象总共有3种属性：
Tag： 使用<和>包围的部分，如<rank>成为start-tag，</rank>是end-tags；Tag结果是一个字符串。
Element：被Tag包围的部分，如<rank>68</rank>，可以认为是一个节点，它可以有子节点。element的值通过element.text获得
Attribute：在Tag中可能存在的name/value对，如<country name="Liechtenstein">中的name="Liechtenstein"，一般表示属性。
Attribute结果是一个字典。
"""


def parser_xml(xml_path):
    """
    分析xml文件，把每一条数据全部转换成字典类型的数据，并把所有的字典数据存放到一个大的list中
    :param xml_path: 要处理的xml文件路径
    :return: 所有事件的list集合
    """
    try:
        tree = ET.parse(xml_path)
        # 根节点
        root = tree.getroot()
        # 标签名
        # print('root_tag:', root)

        # tree = ET.parse(xml_path)

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
                            dct_name['GUID'] = item.attrib['Guid'][1:-1]
                        elif item.tag[51:] == "TimeCreated":
                            dct_name['TimeCreated SystemTime'] = item.attrib['SystemTime']
                        else:
                            dct_name[item.tag[51:]] = item.text
            events_list.append(dct_name)
        return events_list
    except SyntaxError:
        print(f"the file: {xml_path} is not xml format")
    except Exception as e:
        print(e)


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


def process_xml(input_path: str = "", output_path: str = ""):
    """
    根据传入的xml文件及生成报告的csv文件目录类型的不同，使用不同的策略。
    :param input_path: xml文件或文件路径
    :param output_path: 解析后csv文件路径，如果缺省，则在input_path同级目录下创建新目录
    :return:
    """

    # 分别传入了xml文件目录和csv报告保存目录
    if os.path.isdir(input_path) and os.path.isdir(output_path):
        print("xml dir and output dir")
        for flines in os.listdir(input_path):
            if os.path.splitext(flines)[1] == '.xml':
                time_stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
                # 在目录中根据不同的xml文件名称创建不同的目录
                new_output_path = os.path.join(
                    output_path + f"/{os.path.splitext(flines)[0]}" + "_ln_log_parser_" + time_stamp)
                if not os.path.exists(new_output_path):
                    os.mkdir(new_output_path)
                # 把路径和文件拼接成最终路径
                new_path = os.path.join(input_path, flines).replace("\\", "/")
                try:
                    # 解析xml文件
                    all_evt_list = parser_xml(xml_path=str(new_path).replace("\\", "/"))
                    # 把解析后的xml写入csv文件中
                    archive_dct(all_evt_list, report_path=str(new_output_path).replace("\\", "/"))
                except TypeError:
                    os.rmdir(new_output_path)
                except KeyError:
                    os.rmdir(new_output_path)
                    print("the file: " + str(new_path).replace("\\", "/") + " is not ln log format")
                except Exception as e:
                    os.rmdir(new_output_path)
                    print(e)
    # 只传入了xml文件目录
    elif os.path.isdir(input_path):
        print("only xml dir")
        # print(os.path.abspath(os.path.join(input_path, "../")))
        for flines in os.listdir(input_path):
            if os.path.splitext(flines)[1] == '.xml':
                time_stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
                # 获得上级目录并在同级目录下创建开头相同的文件夹，这里使用的是输入路径的绝对值+后缀的，和普通的join里使用逗号拼接是不一样的
                up_path = os.path.join(os.path.abspath(input_path) + "_ln_log_parser" + time_stamp)
                if not os.path.exists(up_path):
                    os.mkdir(up_path)
                # 在目录中根据不同的xml文件名称创建不同的目录，这里使用的是逗号拼接的目录
                new_output_path = os.path.join(
                    up_path, os.path.splitext(flines)[0] + "_ln_log_parser_" + time_stamp)
                if not os.path.exists(new_output_path):
                    os.mkdir(new_output_path)
                # 把路径和文件拼接成最终路径
                new_path = os.path.join(input_path, flines).replace("\\", "/")
                try:
                    # 解析xml文件
                    all_evt_list = parser_xml(xml_path=str(new_path).replace("\\", "/"))
                    # 把解析后的xml写入csv文件中
                    archive_dct(all_evt_list, report_path=str(new_output_path).replace("\\", "/"))
                except TypeError:
                    os.rmdir(new_output_path)
                except KeyError:
                    os.rmdir(new_output_path)
                    print("the file: " + str(new_path).replace("\\", "/") + " is not ln log format")
                except Exception as e:
                    os.rmdir(new_output_path)
                    print(e)
    # 传入了xml文件本身，及csv报告保存目录
    elif os.path.isfile(input_path) and os.path.isdir(output_path):
        print("xml file and output dir")
        try:
            all_evt_list = parser_xml(xml_path=str(input_path).replace("\\", "/"))
            archive_dct(all_evt_list, report_path=str(output_path).replace("\\", "/"))
        except TypeError:
            os.rmdir(output_path)
        except KeyError:
            os.rmdir(output_path)
            print("the file: " + str(input_path).replace("\\", "/") + " is not ln log format")
        except Exception as e:
            os.rmdir(output_path)
            print(e)
    # 只传入了xml文件本身
    elif os.path.isfile(input_path):
        print("only xml file")
        time_stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        new_output_path = os.path.join(input_path[0:-4] + "_ln_log_parser_" + time_stamp)
        os.mkdir(new_output_path)
        try:
            all_evt_list = parser_xml(xml_path=str(input_path).replace("\\", "/"))
            archive_dct(all_evt_list, report_path=str(new_output_path).replace("\\", "/"))
        except TypeError:
            os.rmdir(new_output_path)
            pass
        except KeyError:
            os.rmdir(new_output_path)
            print("the file: " + str(input_path).replace("\\", "/") + " is not ln log format")
        except Exception as e:
            os.rmdir(new_output_path)
            print(e)
    else:
        print("555555555555555555")
        print("path is error")


if __name__ == '__main__':
    # process_xml(input_path="D:\\tmp\input\\fewfew", output_path="D:\\tmp\\123")

    input_arg = sys.argv
    # print(input_arg)
    # 判断参数输入是否正确
    if len(input_arg) == 1:
        print("the xml file is must")
    elif len(input_arg) == 2:
        process_xml(input_path=str(input_arg[1]).replace("\\", "/"))
    elif len(input_arg) >= 3:
        process_xml(input_path=str(input_arg[1]).replace("\\", "/"), output_path=str(input_arg[2]).replace("\\", "/"))
    else:
        print("arg error")
    pass

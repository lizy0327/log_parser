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

from Cryptodome.Cipher import AES
from binascii import b2a_hex
import sys

version = '1.0.0'


def my_help():
    print(
        "-h --help    Show this help \n"
        "-v --version Show version \n"
        "EXAMPLES: \n"
        "gen_license <uuid> <date:20220101>"
    )


def encrypt(content):
    # content length must be a multiple of 16.
    while len(content) % 16:
        content += ' '
    content = content.encode('utf-8')

    # Encrypt content.
    # aes = AES.new(b'2023052020210520', AES.MODE_CBC, b'2023052020210520')
    aes = AES.new(b'0CoJUm3Qyw3W3jud', AES.MODE_CBC, b'0123456789123456')
    encrypted_content = aes.encrypt(content)
    return b2a_hex(encrypted_content)


def gen_license_file(uuid, date):
    license_file = './License.dat'
    with open(license_file, 'w') as LF:
        LF.write(f'UUID : {uuid}\n')
        LF.write(f'Date : {date}\n')
        sign = encrypt(f'{uuid}#{date}')
        LF.write('Sign : ' + str(sign.decode('utf-8')) + '\n')


if __name__ == '__main__':
    # arg1 = 'adf44d56-cb0b-104d-5993-986d637e513a'
    # arg2 = 20230520
    input_arg = sys.argv

    if len(input_arg) == 1:
        my_help()
    elif len(input_arg) == 2:
        # 显示版本信息
        if input_arg[1] == "-v" or input_arg[1] == "--version":
            print(version)
        elif input_arg[1] == "-h" or input_arg[1] == "--help":
            my_help()
        else:
            print("parameter error")
    elif len(input_arg) == 3:
        gen_license_file(uuid=input_arg[1], date=input_arg[2])
    else:
        print("parameter error")

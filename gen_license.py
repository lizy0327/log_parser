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


def encrypt(content):
    # content length must be a multiple of 16.
    while len(content) % 16:
        content += ' '
    content = content.encode('utf-8')

    # Encrypt content.
    # aes = AES.new(b'2023052020210520', AES.MODE_CBC, b'2023052020210520')
    aes = AES.new(b'0CoJUm3Qyw3W3jud', AES.MODE_CBC, b'0123456789123456')
    encrypted_content = aes.encrypt(content)
    return (b2a_hex(encrypted_content))


def gen_license_file():
    license_file = './License.dat'
    with open(license_file, 'w') as LF:
        LF.write('UUID : 400f4d56-dc23-fcb9-a036-44ad358cc569\n')
        LF.write('Date : 20220520\n')
        sign = encrypt('400f4d56-dc23-fcb9-a036-44ad358cc569')
        LF.write('Sign : ' + str(sign.decode('utf-8')) + '\n')


if __name__ == '__main__':
    gen_license_file()

#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'coderz'

import sys
import re

#extract brackets
s = "alpha.beta[23456] id=1111, reson:NEM, type: FULL, saa:1 , index:0"
m = re.search(r"\[([A-Za-z0-9_]+)\]", s)
print m.group(1)

for item in s.split(','):
   for key in item.split(':'):
       print key

s = 'Today is 31-05-2013'
mo = re.search(r'\d{2}-\d{2}-\d{4}', s)
print(mo.group())


str = 'Today is 2013-May-31'
mo = re.search(r'\d{4}-[A-Za-z]{3}-\d{2}', str)
print(mo.group())

str = "abc12345def"
mo = re.search(r'\d{2,}', str)
print(mo.group())
mo = re.search(r'\d+', str)
print(mo.group())

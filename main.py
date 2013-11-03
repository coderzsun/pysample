#!/usr/bin/python  
# -*- coding: utf-8 -*-
#
# File: main.py
#
#from __future__ import division  
import web
import os
import json
import sys
import config
from models import urls
from controller import Controller


reload(sys)
sys.setdefaultencoding('utf-8') #设置系统编码，解决中文编码问题



# to avoid any path issues, "cd" to the web root.
web_root = os.path.abspath(os.path.dirname(__file__))
os.chdir(web_root)
sys.path.append(web_root+'/models');
sys.path.append(web_root+'/controller');

#SQLite数据库名  ,Windows
DB_SQLITE_NAME=os.path.join(web_root,"db\pytest.db")




########===============================================================######
app = web.application(urls.urls, globals(), autoreload=True)
web.config.debug = True
########===============================================================######


if __name__ == "__main__":
		web.internalerror = web.debugerror
		app.run()


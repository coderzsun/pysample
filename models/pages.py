# -*- coding: utf-8 -*-  
#!/usr/bin/python
"""静态StaticFile和Page的抽象，并且针对mako模板引擎，和本项目细化了Page"""

__authors__ = [
  '"BigYuki" <sheyuqi@gmail.com>',
]

from mako.template import Template
from mako.lookup import TemplateLookup
import mimetypes
import web

class StaticFile:
    """针对web.py，返回静态文件。"""
    def __init__(self):
        self.staticFloder='admin/themes/'
    def GET(self, themeFloder, file,other):
        try:
            f = open(self.staticFloder+themeFloder+'/'+file, 'rb')
            #if other=='css':
            contentType=mimetypes.guess_type(file)[0]
            web.header("Content-Type", contentType)
            return f.read()
        except:
            raise web.NotFound()

class Page:
    """抽象Page。针对web.py"""
    def __init__(self):
        self.templateFilePath=""
    def render(self):
        pass
    def GET(self):
        pass
    def POST(self):
        pass

class MakoPage(Page):
    """使Page在mako模板引擎下可用。"""
    def __init__(self):
        Page.__init__(self)
    def render(self):
        lookup = TemplateLookup(
                                  directories=['',],input_encoding='utf-8',output_encoding='utf-8',
                                  )
        template = Template(
                                          filename=self.templateFilePath,
                                          input_encoding='utf-8',
                                          output_encoding='utf-8',
                                          lookup=lookup,
                                          )
        return template.render(DATA=self)

class YukiBlogPage(MakoPage):
    """针对YukiBlog文件目录，细化模板文件位置。"""
    def __init__(self):
        MakoPage.__init__(self)
        self.themeAbsDiretory='themes/'
        self.themeFolder='default'
        self.templateFile='index.html'
        self.globals={
                      'session':web.ctx.session,
                    }
    def render(self):
        self.templateFilePath=self.themeAbsDiretory+self.themeFolder+'/'+self.templateFile
        return MakoPage.render(self)
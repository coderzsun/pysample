# encoding: utf-8
# File: code.py
# -*- coding: utf-8 -*-
#from __future__ import division  
import web
import os
from web import form
from web.contrib.template import render_mako
from mako.template import Template
from mako.lookup import TemplateLookup
import json


import sys
reload(sys)
sys.setdefaultencoding('utf-8') #设置系统编码，解决BAE上面的中文编码问题


# to avoid any path issues, "cd" to the web root.
web_root = os.path.abspath(os.path.dirname(__file__))
os.chdir(web_root)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates/')
templates_admin_root = os.path.join(app_root, 'templates/admin')
static_root = os.path.join(app_root, 'static')

mylookup = TemplateLookup(directories=['./templates'], output_encoding='utf-8', encoding_errors='replace')
mytemplate = mylookup.get_template("base.html")


#render = web.template.render('templates/') 

##----------------------------------------------------------
## 两个render，一个前端，一个后台
##----------------------------------------------------------
'''
render = render_mako(
        templates_root,
        input_encoding='utf-8',
        output_encoding='utf-8',
        )
'''

render_admin = render_mako(
        templates_admin_root,
        input_encoding='utf-8',
        output_encoding='utf-8',
        )
		
render = render_mako(  directories=[os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )
		
urls = (
		'/', 'index',
		    '/ajaxdropdowns', 'ajaxdropdowns',
    '/getregionsasjson', 'getregionsasjson',
	'/getcheckbox','getcheckbox',
		'/env','env',
		'/tp','ip' ,
		'/hello/(.*)', 'hello',
		'/help/faq', 'faq',
		'/item/(\d+)', 'item',
		'/add/(.+)','add',  
		'/myadd','myadd',
		r'/(\d*)', 'Index',
		r'/view/(\d*)', 'View',
		r'/tag/(\d+)/?(\d*)', 'TagHandler',
		r'/search/([^\s/]+)/?(\d*)', 'SearchHandler',
		r'/date/(\d+)/?(\d*)', 'DateHandler',
		r'/month/(\d+)/?(\d*)', 'MonthHandler',
		r'/year/(\d+)/?(\d*)', 'YearHandler',
		r'/archive/(\d{4}-\d{2})/?(\d*)', 'ArchiveHandler',
		r'/photo/?(\w*)', 'PhotoHandler',
		r'/admin/login/?', 'Login',
		r'/admin/logout/?', 'Logout',
		r'/admin/?', 'AdminHandler',
		r'/admin/menu/?', 'MenuHandler',
		r'/admin/plist/?', 'PostListHandler',
		r'/admin/new/?', 'New',
		r'/admin/delete/(\d+)', 'Delete',
		r'/admin/edit/(\d+)', 'Edit',
		r'/admin/upload/?', 'UploadHandler',
		r'/admin/del-attac/(\d+)', 'DelAttacHandler',
		r'/admin/tag-manage/?', 'TagManageHandler',
		r'/rss/(\d*)', 'RssHandler',
		"/tasks/?", "signin",
		"/tasks/list", "listing",
		"/tasks/post", "post",
		"/tasks/chgpass", "chgpass",
		"/tasks/act", "actions",
		"/tasks/logout", "logout",
		"/settings_btn","settings_btn",
		"/tasks/signup", "signup"
		)

		
		##----------------------------------------------------------
## 公共基类
##----------------------------------------------------------
class Base():

    def __init__(self):
        self._conf = conf.site
        self.set_conf('logo_img', util.get_logo_img())
        self.login_user = util.get_login()

    def datestr(self,date):
        return web.datestr(date)

    def datefmt(self,time,fmt):
        return datetime.datetime.strftime(time, fmt)
    
    def datenow(self, fmt="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.strftime(datetime.datetime.now(), fmt)

    def get_conf(self, key):
        if self._conf.has_key(key) and self._conf[key] is not None\
           and len(self._conf[key]) > 0:
            return self._conf[key]
        else:
            return None

    def process_cont(self, cont, is_md, is_excerpt=True):
        cont = web.net.htmlunquote(cont)
        if is_excerpt:
            cont = util.excerpt(cont)
        if is_md == 1:
            cont = markdown.markdown(cont)
        return cont


    def set_conf(self, key, val):
        if self._conf is not None:
            self._conf[key] = val


    def get_recent_posts(self):
        return model.get_recent_posts()

    def get_rand_posts(self):
        return model.get_rand_posts()

    def get_tags(self):
        return model.get_tags()

    def get_archives(self):
        return model.get_archives()

    def render_page(self, currentCls):
        return util.render_page_li(self, currentCls)

    def get_sidebar(self):
        self.recentPostList = self.get_recent_posts()
        self.randPostList = self.get_rand_posts()
        self.archiveList = self.get_archives()
        self.tagCloud = self.get_tags()

		
		
app = web.application(urls, globals(), autoreload=True)


def serve_template(templatename, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    print mytemplate.render(**kwargs)


class mako_render:
     def __init__(path):
         self._lookup = TemplateLookup(directories=[path],  module_directory='mako_modules')
     def __getattr__(self, name):
         path = name + '.html'
         t = self._lookup.get_template(path)
         t.__call__ = t.render
         return t
		 
class env:
     def GET(self):
          data = StringIO.StringIO()
          for key in web.ctx.env:
               print >>data,key,'>>',web.ctx.env[key]
          content = data.getvalue()
          data.close()
          return content

class ip:
     def GET(self):
          return "user's ip address is {0}".format(web.ctx.ip) 
		  
		  
class ajaxdropdowns:        
    def GET(self):
        return render.ajaxdropdowns()

		
class index:
	def GET(self):
			return render.index()
	def POST(self):
		i = web.input()
		post_data=web.input(name=[])
		print post_data
		if not f.validates():
			return render.index()
		else:
			return "HAHA!"

			
#http://localhost/myapp/greetings/hello?name=Joe 
#http://127.0.0.1:8080/myadd?id=2

#/users/list/(.+), "list_users" 
#class add:  
#    def GET(self,name):     #对应的url里面有括号，所以有name这个参数  
#        return "Listing info about user: {0}".format(name)  
        
class myadd:  
    def GET(self):      #对应的url里面没有括号，所以没有name这个参数  
        return web.input()['id']  
        #return web.input().id  
		
##----------------------------------------------------------
## 前端处理
##----------------------------------------------------------

class Index(Base):
    def __init__(self):
        Base.__init__(self)
        self.set_conf('sub_title', None)
        self.set_conf('action_url', "/")

    def GET(self, page):
        
        tmp_posts = model.get_posts(page)
        posts = tmp_posts[0]
        pageDict = tmp_posts[1]
        newPosts = []
        for p in posts:
            p.content = self.process_cont(p.content, p.is_md)
            p.tags = model.get_tag(p.id)
            newPosts.append(p)

        self.posts = newPosts
        self.pageDict = pageDict
        self.get_sidebar()

        return render.index(page=self)

class settings_btn:
    def POST(self):
				return mytemplate.render(name=name)

class hello:
	def GET(self, name):
#		web.header('content-type', 'text/html') 
#		web.header("Content-Type", "text/plain")
		return mytemplate.render(name=name)
	def POST(self):
		ino = web.input()
		web.header('Content-Type', 'application/json')
		return json.dumps(
				{ 
			# Do trivial operations:
				'txt' : ino.mod.lower(),	'dat' : "%.3f" % float(ino.num)
				} )

class getregionsasjson:        
    def POST(self):
        try:
            country = getAjaxArg("country")

            #something here would populate this as needed
            if country == "USA":
                return json.dumps(["Alabama", "Georgia", "Michigan", "Texas"])       
            if country == "Canada":
                return json.dumps(["Newfoundland", "Manitoba", "Alberta", "France (quebec) :-)"])

        except Exception, ex:
            print ex.__str__()    
class getcheckbox:
	def POST(self):
		try:
			print "user ip is :" + web.ctx.ip
			country = getAjaxArg("checkbox")
			print country.split(',')
			return json.dumps(country.split(','))
		except Exception, ex:
			print ex.__str__()    	
def getAjaxArg(sArg, sDefault=""):
    """Picks out and returns a single value, regardless of GET or POST."""
    try:
        data = web.data()
        dic = None
        if data:
            dic = json.loads(data)
        else:
            # maybe it was a GET?  check web.input()
            dic = dict(web.input())

        if dic:
            if dic.has_key(sArg):
                if dic[sArg]:
                    return dic[sArg]
                else:
                    return sDefault
            else:
                return sDefault
        else:
            return sDefault
    except ValueError:
        raise Exception("getAjaxArg - no JSON arguments to decode. This method required a POST with JSON arguments.")


			
########===============================================================######
web.config.debug = True
if __name__ == "__main__":
		web.internalerror = web.debugerror
		app.run()


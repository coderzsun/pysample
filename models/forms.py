# -*- coding: utf-8 -*-  
#!/usr/bin/python
"""各类表单和表单验证。"""
from web import form
import os
""" 表单各种验证 """
Validation={
            'email':form.regexp(r"([a-zA-Z0-9_-])+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", "请输入正确的电子邮箱"),
            'password':form.regexp(r".{5,20}$", '密码必须大于5位'),
            'number':form.regexp(r"\d+",'必须为数字'),
            'title':form.regexp(r".{4,40}$",'标题长度不符'),
            'host':form.regexp(r"(http|https)://[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+/?$","主机格式不符"),
            'keywords':form.regexp(r"[^\s]+(,[^\s]+)*$","输入格式不对[关键字1,关键字2]"),
            'notnull':form.Validator("不能为空", bool),
            'url':form.regexp(r"[a-zA-z]+://[^\s]*","URL格式不符"),
            }
def LoginForm():
    """登陆表单"""
    newForm = form.Form(
                                  form.Textbox("login_email",Validation['email'], description=u"邮箱:"),
                                  form.Password("login_password", Validation['password'],description=u"密码:"),
                                  form.Button("login_submit", type="submit", html=u'登陆'),
                                )
    return newForm

def AlonePageNewForm():
    """ 页面新建表单 """
    newForm = form.Form(
                                  form.Textbox("page_title",Validation['title'],description="标题:"),
                                  form.Textbox("page_link", Validation['link'],description="链接:"),
                                  form.Textarea("page_content",  description="内容:"),
                                  form.Dropdown("page_display", args=[('1','是'),('0','否')],value='1',description="显示:"),
                                  form.Dropdown("page_commentEnable", args=[('1','是'),('0','否')],value='1',description="允许评论:"),
                                  form.Button("page_submit", type="submit", html=u'提交'),
                                )
    return newForm

def AlonePageUpdateForm(alonePage):
    """ 页面更新表单"""
    updateForm = form.Form(
                                  form.Hidden("page_id",value=alonePage.id),
                                  form.Textbox("page_title", description="标题:",value=alonePage.title),
                                  form.Textbox("page_link", description="链接:",value=alonePage.link),
                                  form.Textarea("page_content",  description="内容:",value=alonePage.content),
                                  form.Dropdown("page_display", args=[('1','是'),('0','否')],description="显示:",value=alonePage.display and "1" or "0"),
                                  form.Dropdown("page_commentEnable", args=[('1','是'),('0','否')],description="允许评论:",value=alonePage.commentEnable and "1" or "0"),
                                  form.Button("page_submit", type="submit", html=u'提交'),
                                )
    return updateForm

def ArticleNewForm(categoryDict):
    """ 文章新建表单   """
    newForm = form.Form(
                                  form.Textbox("article_title",Validation['notnull'], description=u"标题:"),
                                  form.Textarea("article_content",  Validation['notnull'],description=u"内容:"),
                                  form.Dropdown("article_display", args=[('1','是'),('0','否')],value='1',description=u"显示:"),
                                  form.Dropdown("article_commentEnable", args=[('1','是'),('0','否')],value='1',description=u"允许评论:"),
                                  form.Dropdown("article_category", args=categoryDict,description=u"分类:"),
                                  form.Textbox("article_tags", description=u"标签:"),
                                  form.Button("article_submit", type="submit", html=u'提交'),
                                )
    return newForm

def ArticleUpdateForm(article,categoryDict):
    """ 文章更新表单"""
    updateForm = form.Form(
                                  form.Hidden("article_id",value=article.key().id()),
                                  form.Textbox("article_title", Validation['notnull'],description=u"标题:",value=article.title),
                                  form.Textarea("article_content", Validation['notnull'], description=u"内容:",value=article.content),
                                  form.Dropdown("article_display", args=[('1','是'),('0','否')],description=u"显示:",value=article.display and "1" or "0"),
                                  form.Dropdown("article_commentEnable", args=[('1','是'),('0','否')],description=u"允许评论:",value=article.display and "1" or "0"),
                                  form.Dropdown("article_category", args=categoryDict,description=u"分类:",value=article.category.key().id()),
                                  form.Button("article_submit", type="submit", html=u'提交'),
                                )
    return updateForm

def BlogUpdateForm(blog):
    """ 博客信息更新表单"""
    def getThemesDirDict(relativePath):
        themesDirDict=[]
        dirAbsPath=os.path.abspath(
                          os.path.normpath(relativePath)
                          )
        dirlist=os.listdir(dirAbsPath)
        for dir in dirlist:
            path=os.path.join(dirAbsPath,dir)
            if os.path.isdir(path):
                themesDirDict.append((dir,dir))
        return themesDirDict
    newForm = form.Form(
                                  form.Textbox("blog_name", Validation['notnull'], description=u"名称:",value=blog.name),
                                  form.Textbox("blog_title", Validation['notnull'], description=u"标题:",value=blog.title),
                                  form.Textbox("blog_subtitle", Validation['notnull'],  description=u"子标题:",value=blog.subtitle),
                                  form.Textbox("blog_host", Validation['host'], description=u"主机:",value=blog.host),
                                  form.Dropdown("blog_theme", args=getThemesDirDict('themes'),description=u"主题:",value=blog.theme),
                                  form.Textarea("blog_description", Validation['notnull'], description=u"描述:",value=blog.description),
                                  form.Textbox("blog_keywords", Validation['keywords'],description=u"关键字:",value=blog.keywords), 
                                  form.Textarea("blog_announcement",description=u"公告:",value=blog.announcement),
                                  form.Textbox("blog_pageSize", Validation['number'],description=u"每页显示条数:",value=blog.pageSize),
                                  form.Textbox("blog_version", readonly="true",description=u"版本:",value=blog.version),
                                  form.Button("blog_submit", type="submit", html=u'提交'),
                                )
    return newForm

def BlogerUpdateForm(bloger):
    """ 博主信息更新的表单  """
    newForm = form.Form(
                                  form.Textbox("bloger_nickname", Validation['notnull'], description=u"昵称:",value=bloger.nickname),
                                  form.Textbox("bloger_email", Validation['email'], description=u"邮箱:",value=bloger.email),
                                  form.Dropdown("bloger_sex", args=[('1','男'),('0','女')],value=bloger.sex,description=u"性别:"),
                                  form.Textbox("bloger_avatar", Validation['url'],description=u"头像:",value=bloger.avatar),
                                  form.Textarea("bloger_description",Validation['notnull'], description=u"描述:",value=bloger.description),
                                  form.Button("bloger_submit", type="submit", html=u'提交'),
                                )
    return newForm

def CategoryNewForm():
    """ 分类新建表单 """
    newForm = form.Form(
                                  form.Textbox("category_name",  Validation['notnull'],description=u"分类名称:"),
                                  form.Button("category_submit", type="submit", html=u'提交'),
                                  )
    return newForm
def CategoryUpdateForm(category):
    """分类更新表单"""
    updateForm = form.Form(
                                   form.Hidden("category_id",value=category.key().id()),
                                   form.Textbox("category_name",description="分类名称:",value=category.name),
                                   form.Button("submit",type="submit",html=u'提交'),
                                   )
    return updateForm
def CommentNewForm(articleID):
    """评论新建表单"""
    newForm = form.Form(
                                  form.Hidden("comment_article_id", description="article ID:",value=articleID),
                                  form.Textbox("comment_nickname", description="昵称:"),
                                  form.Textbox("comment_email", description="邮箱:"),
                                  form.Textbox("comment_website", description="邮箱:"),
                                  form.Textarea("comment_content", description="内容:"),
                                  form.Button("comment_submit", type="submit", html=u'提交'),
                                )
    return newForm
def NavigationNewForm():
    """导航新建表单"""
    newForm = form.Form(
                                  form.Textbox("navigation_name", description=u"名称:"),
                                  form.Textbox("navigation_link", description=u"链接:"),
                                  form.Textbox("navigation_weight",description=u"优先级"),
                                  form.Button("navigation_submit", type="submit", html=u'提交'),
                                  )
    return newForm
def NavigationUpdateForm(navigation):
    """ 导航更新表单 """
    updateForm = form.Form(
                                  form.Hidden("navigation_id",value=navigation.key().id()),
                                  form.Textbox("navigation_name", description=u"名称:",value=navigation.name),
                                  form.Textbox("navigation_link", description=u"链接:",value=navigation.link),
                                  form.Textbox("navigation_weight",description=u"优先级",value=navigation.weight),
                                  form.Button("navigation_submit", type="submit", html=u'提交更新'),
                                  )
    return updateForm


def AdminUpdateForm(administrator):
    """ 管理员账号更新表单

        administrator_old_email                                    原邮箱
        administrator_old_password                           原密码
        administrator_email                                            新邮箱
        administrator_password                                    新密码
        administrator_password_confirm                   确认密码
        administrator_submit                                          提交
    """
    updateForm = form.Form(
                           form.Textbox("administrator_old_email",readonly="true", description=u"原邮箱:",value=administrator.email),
                           form.Password("administrator_old_password",Validation['password'],description=u"原密码:"),
                           form.Textbox("administrator_email",Validation['email'],description=u"新邮箱:"),
                           form.Password("administrator_password", Validation['password'],description=u"新密码:"),
                           form.Password("administrator_password_confirm", Validation['password'],description=u"确认密码:"),
                           form.Button("administrator_submit", type="submit", html=u'提交'),
                           validators = [
                                         form.Validator("确认密码不正确", lambda i: i.administrator_password == i.administrator_password_confirm)],
                           )
    return updateForm


	
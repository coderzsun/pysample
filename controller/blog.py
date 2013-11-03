# -*- coding: utf-8 -*- 
#!/usr/bin/python

class blog:
        
    def GET(self):
        posts = Posts_Controller.get_posts()
        postId = web.input(id=None)
        if postId.id == None:
            return render.blog(posts, None)
        elif int(postId.id) >= 0:
            return render.blog(posts, int(postId.id))
        
class new_post:
    
    new_post_form = form.Form(
        form.Textbox('title', description='Title: ', size=25),
        form.Textarea('content', description='Content: ', rows=30, cols=50),
        form.Button('Submit Post')
    )

    def GET(self):
        new_post_form = self.new_post_form()
        return render.new_post(new_post_form)
        
    def POST(self):
        new_post_form = self.new_post_form()
        if not new_post_form.validates():
            return render.new_post(new_post_form)
        else:
            Posts_Controller.add_post(Blog_Post(new_post_form.d.title, new_post_form.d.content))
            return render.new_post(None)


class View:  
    def GET(self, id):  
        post = model.get_post(int(id))  
        return render.view(post)  

class New:  
    form = web.form.Form(  
                         web.form.Textbox('title',  
                         web.form.notnull,  
                         size=30,  
                         description='Post title: '),  
                         web.form.Textarea('content',  
                         web.form.notnull,  
                         rows=30,  
                         cols=80,  
                         description='Post content: '),  
                         web.form.Button('Post entry'),  
                         )  
    def GET(self):  
        form = self.form()  
        return render.new(form)  
    def POST(self):  
        form = self.form()  
        if not form.validates():  
            return render.new(form)  
        model.new_post(form.d.title, form.d.content)  
        raise web.seeother('/') 

#删除文章类  
class Delete:  
    def POST(self, id):  
        model.del_post(int(id))  
        raise web.seeother('/')  
#编辑文章类  
class Edit:  
    def GET(self, id):  
        post = model.get_post(int(id))  
        form = New.form()  
        form.fill(post)  
        return render.edit(post, form)  
    def POST(self, id):  
        form = New.form()  
        post = model.get_post(int(id))  
        if not form.validates():  
            return render.edit(post, form)  
        model.update_post(int(id), form.d.title, form.d.content)  
        raise web.seeother('/')  
#退出登录  
class Logout:  
    def GET(self):  
        web.setcookie('username', '', expires=-1)  
        raise web.seeother('/')  
#定义404错误显示内容  
def notfound():  
    return web.notfound("Sorry, the page you were looking for was not found.")  
      
app.notfound = notfound  



import web  
import datetime  
#数据库连接  
db = web.database(dbn = 'mysql', db = 'test', user = 'root', pw = '123456')  
#获取所有文章  
def get_posts():  
    return db.select('entries', order = 'id DESC')  
      
#获取文章内容  
def get_post(id):  
    try:  
        return db.select('entries', where = 'id=$id', vars = locals())[0]  
    except IndexError:  
        return None  
#新建文章  
def new_post(title, text):  
    db.insert('entries',  
        title = title,  
        content = text,  
        posted_on = datetime.datetime.utcnow())  
#删除文章  
def del_post(id):  
    db.delete('entries', where = 'id = $id', vars = locals())  
      
#修改文章  
def update_post(id, title, text):  
    db.update('entries',  
        where = 'id = $id',  
        vars = locals(),  
        title = title,  
        content = text)  
		
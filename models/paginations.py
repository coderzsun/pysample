# -*- coding: utf-8 -*-  
#!/usr/bin/python2.7
"""分页器"""

__authors__ = [
  '"Coder" <coder@gmail.com>',
]
class Pagination:
    """普通基于数组的分页器"""
    def __init__(self,querySet,pageSize=10):
        self.__pageSize=pageSize
        self.__querySet=querySet
        self.__nowPage=1
    
    def getPageSize(self):
        return self.__pageSize
    def getNowNum(self):
        return self.__nowPage
    def getNextNum(self):
        return self.__nowPage+1
    def getPrevNum(self):
        return self.__nowPage-1
    def getFirstNum(self):
        return 1
    def getLastNum(self):
        if self.count()%self.getPageSize()==0:
            return self.count()/self.getPageSize()
        else:
            return (self.count()/self.getPageSize())+1
    def hasNextPage(self):
        return self.getNowNum()<self.getLastNum()
    def hasPrevPage(self):
        return self.getNowNum()>self.getFirstNum()
    def getQuerySet(self):
        return self.__querySet
    def turnToPage(self,page):
        self.__nowPage=page
    def count(self):
        return len(self.getQuerySet())
    def getResultSet(self):
        cursorStart=(self.getNowNum()-1)*self.getPageSize()
        cursorEnd=cursorStart+self.getPageSize()
        return self.getQuerySet()[cursorStart:cursorEnd]

class GaePagination(Pagination):
    """针对Google App Engine的分页器"""
    def __init__(self,querySet,pageSize=10):
        Pagination.__init__(self, querySet, pageSize)
    def count(self):
        return self.getQuerySet().count()
    def getResultSet(self):
        cursorStart=1+(self.getNowNum()-1)*self.getPageSize()
        return self.getQuerySet().fetch(self.getPageSize(),cursorStart-1)
        
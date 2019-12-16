#!/usr/bin/env python
# -*- coding: UTF-8 -*-# enable debugging
# Intro to webpy, from http://webpy.org/docs/0.3/tutorial
# Doesn't currently work easily in python3
import web
render = web.template.render('templates/')
web.config.debug = True
urls = (
  '/', 'index'
)

class index:
   def GET(self):
#   def GET(self, name):
#        return "Hello, world!"
#     name = 'Bob'
#     i = web.input(name=None)
     name = web.input()
     return render.index(name)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()



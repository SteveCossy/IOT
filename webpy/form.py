#!/usr/bin/env python
# -*- coding: UTF-8 -*- # enable debugging
# from http://webpy.org/cookbook/forms
# exmaple https://stackoverflow.com/questions/37663787/html-webpy-multilpe-forms
# files https://realpython.com/working-with-files-in-python/#directory-listing-in-legacy-python-versions
# Doesn't currently work easily in python3

import web, os
from web import form
web.config.debug = True

render = web.template.render('templates/') # your templates
urls = (
  '/', 'register'
)

entries = os.listdir('./archive')

register_form = form.Form(
    form.Dropdown(name='fileName', args=entries),
#    form.Checkbox('fileName', value="file" ),
    form.Button("submit", type="submit", description="Select File")
 )

class register:
    def GET(self):
        # do $:f.render() in the template
        f = register_form()
        return render.register(f)

    def POST(self):
        f = register_form()
        if not f.validates():
            return render.register(f)
        else:
            # do whatever is required for registration
            return f["fileName"].value

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()


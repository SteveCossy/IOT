#!/usr/bin/env python
# -*- coding: UTF-8 -*- # enable debugging
# from http://webpy.org/cookbook/forms
# example https://stackoverflow.com/questions/37663787/html-webpy-multilpe-forms
# files https://realpython.com/working-with-files-in-python/#directory-listing-in-legacy-python-versions
# Doesn't currently work easily in python3

import web, os
from urllib import quote
from web import form
from csv2json import to_geojson
# web.config.debug = True

render = web.template.render('templates/') # your templates
urls = (
  '/', 'register'
)

OutputPath ='./temp/'
InputPath  ='./archive'
TargetURL  ='http://students.pcsupport.ac.nz/OSM/'
ExtOut     ='.geojson'

entries = os.listdir(InputPath)
# entries = os.listdir('/home/cosste/CayMQTT')

register_form = form.Form(
    form.Dropdown(name='fileName', args=entries),
#    form.Checkbox('fileName', value="file" ),
    form.Button("submit", type="submit", description="Select File")
 )


class register:
    def GET(self):
        # do $:f.render() in the template
        web.header('Content-Type', 'text/html')
        f = register_form()
        return render.register(f)

    def POST(self):
        web.header('Content-Type', 'text/html')
        f = register_form()
        if not f.validates():
            return render.register(f)
        else:
            # process the file chosen
            ChosenFile=f["fileName"].value
            fileName, fileExt = os.path.splitext(ChosenFile)
            if 'csv' in fileExt:
                OutputFile = os.path.join(OutputPath, fileName+ExtOut)
            else:
                OutputFile = os.path.join(OutputPath, ChosenFile+ExtOut)
            ChosenFile = os.path.join(InputPath, ChosenFile)
            to_geojson(ChosenFile, OutputFile)
            result = '{}?{}'.format(TargetURL,OutputFile)
#            return '<a href='+TargetURL+'?'+OutputFile+'> Open '+TargetURL+'?'+OutputFile+' </a>'
            raise web.seeother(result)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()


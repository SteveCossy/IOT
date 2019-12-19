#!/usr/bin/env python
import web, webbrowser

urls = ("/.*", "hello")
# app = web.application(urls, globals())

class hello:
    def GET(self):
        webbrowser.open('http://net-informations.com', new=2)
        return 'Hello, world!'

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()


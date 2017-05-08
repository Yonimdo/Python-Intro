# pip install bottle
from bottle import route, run, template


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route("/feed.json")
def index():
    return'[]'


run(host='localhost', port=3000)

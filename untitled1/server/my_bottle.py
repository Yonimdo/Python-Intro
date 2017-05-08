# pip install bottle
from bottle import route, run, template, request
import json


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route("/feed", )
def feed():
    posts = request.json
    with open("../db/posts.json", "r", encoding='UTF-8') as f:
        return f.read()


@route("/posts/<index>.json")
def posts(index):
    with open("../db/posts.json", "r", encoding='UTF-8') as f:
        posts = json.load(f)
        post = posts[int(index)]
        return post


@route("/new_post", method='POST')
def new_post():
    body = json.load(request.body)
    return "404"


run(host='localhost', port=3000)

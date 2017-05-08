import requests

NEEDLE = "(age&#160;"
def how_old_is(name):
    html = requests.get("https://en.wikipedia.org/wiki/"+name).content.decode("utf8")
    i =html.find(NEEDLE)
    if i==-1:
        return "Age not found in page: "+"https://en.wikipedia.org/wiki/"+"_".join(name.split())
    i_d=html[i:].find(")")
    return html[i+len(NEEDLE):i+i_d]


while True:
    name = input("What Person are we looking for: ")
    print(how_old_is(name))


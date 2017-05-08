import requests
import sys

NEEDLE = r'<a class="spell" href="/search?q='
NEEDLE_2 = r'<a class="spell" href="/search?safe=off&amp;q='


def fix_spell(text):
    search_text = "+".join(text.split())
    html = requests.get('https://www.google.ie/search?q={}&ie=utf-8&oe=utf-8'.format(search_text)).content.decode(
            "utf8")
    i = html.find(NEEDLE)
    if i == -1:
        i = html.find(NEEDLE_2)
    if i == -1:
        return False, text
    i_d = html[i:].find("&amp")
    return True, " ".join(html[i + len(NEEDLE):i + i_d].split("+"))


def fix_word(text):
    is_fixed, fixed_text = fix_spell(text)
    if is_fixed:
        print("Output text: " + fixed_text)
    else:
        print("didnt found a spelling error")


if len(sys.argv) > 1:
    for word in sys.argv[1:]:
        fix_word(word)
else:
    print("Ctrl-C to exit")
    while True:
        fix_word(input("Input text: "))

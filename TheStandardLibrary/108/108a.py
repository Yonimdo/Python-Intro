import re
from pprint import pprint


#RE = re.compile(r"\b_?(?P<small>[a-z]+)(?P<big>([A-Z]+)\w+)")
INNER_RE = re.compile("[A-Z]")
RE = re.compile(r"\b_?[a-z]+[A-Z]+\w+")

def inner_replacement(match):
    s = match.group()
    return "_{}".format(s.lower())

def replacement(match):
    s = match.group()
    s_d = INNER_RE.sub(inner_replacement, s)
    return s_d

raw_file = open("Junit.py", "r")
content = raw_file.read()
raw_file.close()
content = RE.sub(replacement, content)

fixed_file = open("j_unit.py", "w")
fixed_file.write(content)
fixed_file.close()

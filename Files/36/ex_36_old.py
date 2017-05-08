import os

output_dir = "output"


templates = {"head": "<h1>{}</h1>",
             "line": "<p>{}</p>",
             "list": "<ul>{}</ul>",
             "list_item": "<li><a href='{0}.html'>{0}</a></li>",
             "new_line": "<hr/>"}


def create_html_by_lines(infile, other_links=None):
    html = ""
    content = infile.splitlines()
    html += templates["head"].format(content[0])
    for ctr in range(1, len(content)):
        html += templates["line"].format(content[ctr])
    html += templates["new_line"]
    if other_links is not None:
        html += other_links
    return html


def website_maker(index_location):
    files = {"index": open("{}.txt".format(index_location), "r")}
    file_names = []
    links = []
    for line in files.get(index_location).read().splitlines():
        tmp_location = "%s.txt" % line
        tmp_file = open(tmp_location, "r")
        links.append(templates["list_item"].format(line))
        files[line] = tmp_file.read()
        tmp_file.close()
        file_names.append(line)

    files["index"].close()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for fn in file_names:
        crnt_links = ""
        for link in links:
            if fn not in link:
                crnt_links += link
        page = open("{}/{}.html".format(output_dir, fn), "w")
        page.write(create_html_by_lines(files[fn], crnt_links))
        page.close()
    return 1


print(website_maker("index"))

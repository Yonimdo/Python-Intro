def ul(items):
    return "<ul>{}</ul>".format("".join(["<li>{}</li>".format(x) for x in items]))

assert "<ul><li>One</li><li>Two</li><li>Three</li></ul>" == ul(['One', 'Two', 'Three'])
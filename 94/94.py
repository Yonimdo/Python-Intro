from PIL import Image
from random import shuffle

n_of_parts = 20
im = Image.open("python.jpg")
im_x, im_y = im.size
region_size_x, region_size_y = im_x // n_of_parts, im_y // n_of_parts
dx, dy = 0, 0


# print(im.size, im.mode, im.format)

def new_deltas(x, y):
    if x + region_size_x >= im_x:
        return 0, y + region_size_y
    else:
        return dx + region_size_x, y


parts = []
new_image = Image.new(im.mode, (im_x + 1, im_y + 1))
for x in range(1, n_of_parts + 1):
    for y in range(1, n_of_parts + 1):
        part = im.crop((dx, dy, dx + region_size_x, dy + region_size_y))
        parts.append(part)
        new_image.paste(part, (dx, dy, dx + part.size[0], dy + part.size[1]))
        dx, dy = new_deltas(dx, dy)

dx, dy = 0, 0
shuffle(parts)

for i, part in enumerate(parts):
    new_image.paste(part, (dx, dy, dx + part.size[0], dy + part.size[1]))
    dx, dy = new_deltas(dx, dy)

new_image.save('new.png')

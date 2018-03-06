import json
from PIL import Image
from io import BytesIO, StringIO
import re
import base64
import sys
import math


def main():
    with open('cards.json') as jsfile:
        data = json.load(jsfile)

    header = 'data:image/png;base64,'
    images = []
    for datum in data:
        imgb64 = datum['cardImg']
        imgb64 = imgb64.replace(header, '')
        imgb64 = re.sub('^data:image/.+;base64,', '', imgb64)
        try:
            img = Image.open(BytesIO(base64.b64decode(imgb64)))
        except:
            print('erroneous card', datum['name'])
            sys.exit(1)

        images.append({
            'json': datum,
            'img': img
        })


    image_width, image_height = images[0]['img'].size

    print("all images assumed to be %d by %d." % (image_width, image_height))

    N = len(images)
    n_per_row = math.ceil(math.sqrt(N))
    master_width = image_width * n_per_row
    master_height = image_height * n_per_row

    print("the master image will by %d by %d" % (master_width, master_height))
    print("creating image...",)
    master = Image.new(
        mode='RGBA',
        size=(master_width, master_height),
        color=(0,0,0,0))  # fully transparent

    print("created.")

    spritedata = []
    for count, imagedict in enumerate(images):
        cardjson = imagedict['json']
        image = imagedict['img']

        xidx = count % n_per_row
        yidx = math.floor(count / n_per_row)
        x = xidx * image_width
        y = yidx * image_height
        print("idx=(%d, %d) xy=(%d, %d)..." % (xidx, yidx, x, y))
        master.paste(image,(x,y))
        print("added.")
        spritedata.append({
            'filename': cardjson['id'],
            'frame': {
                'x': x,
                'y': y,
                'w': image_width,
                'h': image_height
            },
            'rotated': False,
            'trimmed': False,
            'spriteSourceSize': {
                'x': 0,
                'y': 0,
                'w': image_width,
                'h': image_height
            },
            'sourceSize': {
                'w': image_width,
                'h': image_height
            },
            'pivot': {
                'x': 0.5,
                'y': 0.5
            }
        })
    print("done adding icons.")

    masterspritedata = {
        'frames': spritedata,
        'meta': {
            'app': 'https://github.com/confidentidiots/ccspriter'
        }
    }

    print("saving spritesheet image...",)
    master.save('cardspritesheet.png')
    print("saving spritesheet datafile...")
    with open('cardspritesheet.json', 'w') as outfile:
        json.dump(masterspritedata, outfile)
    print("saved!")

if __name__ == '__main__':
    main()

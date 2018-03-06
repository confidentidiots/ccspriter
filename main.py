import json
from PIL import Image
from io import BytesIO, StringIO
import re
import base64
import sys


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

        images.append(img)


    image_width, image_height = images[0].size

    print("all images assumed to be %d by %d." % (image_width, image_height))

    master_width = (image_width * len(images) )
    #seperate each image with lots of whitespace
    master_height = image_height
    print("the master image will by %d by %d" % (master_width, master_height))
    print("creating image...",)
    master = Image.new(
        mode='RGBA',
        size=(master_width, master_height),
        color=(0,0,0,0))  # fully transparent

    print("created.")

    for count, image in enumerate(images):
        location = image_width*count
        print("adding at %d..." % (location),)
        master.paste(image,(location,0))
        print("added.")
    print("done adding icons.")

    print("saving master...",)
    master.save('master.png')
    print("saved!")

if __name__ == '__main__':
    main()

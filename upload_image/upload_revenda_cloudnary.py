from configparser import ConfigParser
from cloudinary.uploader import upload
from PIL import Image
import cloudinary
import os
import sys
import re

SIZE = 250, 250

DEFAULT = dict(path_image_formatted=".")

config = ConfigParser(DEFAULT, allow_no_value=True)
config.read(config.read('settings\config.ini'))
conf = dict(config['CONFIG'])

cloudinary.config(cloud_name=conf['cloud_name'],
                  api_key=conf['api_key'],
                  api_secret=conf['api_secret'])


def ler_imagem(path_imagem: str) -> Image:
    return Image.open(path_imagem)


def transforma_fundo_transparente(image: Image, nome_imagem: str) -> None:
    img = image.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.thumbnail(SIZE)
    img.save(os.path.join(conf["path_image_formatted"], '{}.png'.format(nome_imagem.split('.')[0])))


if __name__ == '__main__':
    try:
        path_images = sys.argv[1]
        for infile in os.listdir(path_images):
            if re.search(r'(\w*)\.(jpg|png)', infile, re.IGNORECASE):
                transforma_fundo_transparente(ler_imagem(os.path.join(path_images, infile)), infile)
                with open('{}.png'.format(infile.split('.')[0]), 'rb') as image:
                    f = image.read()
                    img_src = bytearray(f)
                if conf["upload"] == 'true':
                    upload(img_src, use_filename=True, public_id="{}/{}".format(conf["revenda"], infile))
                    os.remove(os.path.join(conf["path_image_formatted"], '{}.png'.format(infile.split('.')[0])))
    except IndexError:
        print("Por favor digite o caminho das imagens")

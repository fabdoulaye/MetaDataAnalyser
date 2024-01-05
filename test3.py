# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 20:00:23 2023

@author: hp
"""

# from pprint import pprint
# from PIL import Image
import piexif


exif_dict = piexif.load("C:/Users/hp/Downloads/IMG_6880.jpg")

# Initialiser un dictionnaire pour stocker les informations
donnees_image = {}


for ifd in ("0th", "Exif", "GPS", "1st"):
    for tag in exif_dict[ifd]:
        #print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])
        tagdata = piexif.TAGS[ifd][tag]["name"]
        data = exif_dict[ifd][tag]
        # Imprimez le nom et la valeur du tag
        #print(f"{tagdata}: {data}")
        # Stocker les informations dans le dictionnaire
        donnees_image[tagdata] = data

# Afficher les données du dictionnaire
print(donnees_image)


# codec = 'ISO-8859-1'  # or latin-1

# def exif_to_tag(exif_dict):
#     exif_tag_dict = {}
#     thumbnail = exif_dict.pop('thumbnail')
#     exif_tag_dict['thumbnail'] = thumbnail.decode(codec)

#     for ifd in exif_dict:
#         exif_tag_dict[ifd] = {}
#         for tag in exif_dict[ifd]:
#             try:
#                 element = exif_dict[ifd][tag].decode(codec)

#             except AttributeError:
#                 element = exif_dict[ifd][tag]

#             exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

#     return exif_tag_dict

# def main():
#     filename = 'C:/Users/hp/Downloads/IMG_6880.jpg'  # obviously one of your own pictures
#     im = Image.open(filename)

#     exif_dict = piexif.load(im.info.get('exif'))
#     exif_dict = exif_to_tag(exif_dict)

#     pprint(exif_dict['GPS'])

# if __name__ == '__main__':
#    main()
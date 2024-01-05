# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 23:09:05 2023

@author: hp
"""
import getFileMetaData
from moviepy.editor import VideoFileClip
import piexif

def get_video_info(file_path):
    
    exif_dict = piexif.load(file_path)


    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in exif_dict[ifd]:
            #print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])
            tagdata = piexif.TAGS[ifd][tag]["name"]
            data = exif_dict[ifd][tag]
            # Imprimez le nom et la valeur du tag
            #print(f"{tagdata}: {data}")
            
            
    clip = VideoFileClip(file_path)
    duration = clip.duration  # Durée de la vidéo en secondes
    resolution = clip.size  # Résolution de la vidéo (largeur, hauteur)
    fps = clip.fps  # Images par seconde (FPS)
    
    return {
        "duration": duration,
        "resolution": resolution,
        "fps": fps
    }

video_path = "C:/Users/hp/Documents/MSEFC/Pentest/Cette personne qui ne sait pas montrer son affection ：.mp4"  
video_info = get_video_info(video_path)
print(video_info)

time_to_extract = 55  # Temps (en secondes) pour extraire l'image
getFileMetaData.extract_image(video_path, time_to_extract)

start_time = 10  # Temps de début du segment (en secondes)
end_time = 30  # Temps de fin du segment (en secondes)
getFileMetaData.cut_video_segment(video_path, start_time, end_time)
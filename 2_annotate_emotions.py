# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 10:33:44 2022

@author: Simon
"""
import cv2
import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from retinaface import RetinaFace
from deepface import DeepFace
import ospath
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import imageio
import utils
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
import pyshine as ps
import stimer
import json

folder = ospath.expanduser('./retinaface_aligned/')
out_folder = ospath.expanduser('./retinaface_annotated/')


if __name__=='__main__':
    
    files = ospath.list_files(folder, exts='jpg')
    os.makedirs(out_folder, exist_ok=True)

    if ospath.exists('annotations.json'):
        with open('annotations.json', 'r') as f:
            annotations = json.load(f)
    else:
        annotations = {}
    
    for file in tqdm(files):
        filename = ospath.basename(file)

        annot = annotations.get(filename)
        if annot is None:
            try:
                annot = DeepFace.analyze(file, prog_bar=False,
                                         detector_backend='retinaface')
            except Exception:
                print(file)
                continue                
        
        date = datetime.strptime(filename, '%Y.%m.%d %H.%M.%S.jpg').date()
        age = (date-datetime(1990, 9, 5).date()).days//365   
        
        img = imageio.imread(file)

        annot['date'] = date.strftime('%Y %b')
        annot['age'] = age
        
        annotations[filename] = annot
            

        # add age and date to image
        img_annotated = img.copy()
        img_annotated = ps.putBText(img_annotated, date.strftime('%Y %b'),
                                  text_offset_x=10,
                                  text_offset_y=11,
                                  vspace=9,
                                  hspace=10, font_scale=1.0,
                                  background_RGB=(255,225,255),
                                  text_RGB=(1,1,1))
        img_annotated = ps.putBText(img_annotated,f'{age} years',
                                  text_offset_x=10,
                                  text_offset_y=55,
                                  vspace=10,
                                  hspace=10, font_scale=1.0,
                                  background_RGB=(255,225,255),
                                  text_RGB=(1,1,1))
        

        out_file = f'{out_folder}/{filename}'
        
        imageio.imsave(out_file, img_annotated, quality=90)
        
        with open('annotations.json', 'w') as f:
            json.dump(annotations, f, indent=1)



        # break
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 10:33:44 2022

@author: Simon
"""
import os
from retinaface import RetinaFace
import ospath
from tqdm import tqdm
import numpy as np
import imageio
import utils


folder = ospath.expanduser('~/Nextcloud/My Visual Basic/SelfShot/selfshots')

out_folder = './retinaface_aligned/'

def eye_dist(face):
    dist = ((np.array(face['landmarks']['left_eye'])-\
           np.array(face['landmarks']['right_eye']))**2).sum()
    return dist

if __name__=='__main__':
    
    files = ospath.list_files(folder, exts='jpg')
        
    os.makedirs(out_folder, exist_ok=True)
    
    faces = {}
    for file in tqdm(files):
        filename = ospath.basename(file)
        
        img = imageio.imread(file)
        faces_detected = RetinaFace.detect_faces(img)
        if not isinstance(faces_detected, dict): continue
        faces[file] = faces_detected

        # sort face by size
        face = sorted(faces_detected.values(), key=eye_dist)[-1]

        left_eye = face['landmarks']['left_eye']
        right_eye = face['landmarks']['right_eye']
        nose = face['landmarks']['nose']
        
        img_aligned = utils.align(img, right_eye, left_eye,  
                           desiredLeftEye = (0.42,0.45),
                           desiredFaceWidth=800,
                           desiredFaceHeight=600,
                           )

        out_file = f'{out_folder}/{filename}'

        imageio.imsave(out_file, img_aligned, quality=90)

    
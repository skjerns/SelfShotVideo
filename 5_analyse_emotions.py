# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 22:52:30 2022

@author: Simon
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 10:33:44 2022

@author: Simon
"""
import ospath
import json
import numpy as np
from datetime import datetime, date
import matplotlib.pyplot as plt
from scipy.ndimage import median_filter

folder = ospath.expanduser('./retinaface_annotated/')
engine = 'retinaface'
smooth = 30


if __name__=='__main__':
    
    
    events = {date(2013, 8, 31): 'Grenoble',
              date(2014, 1, 24): 'Mannheim',
              date(2014, 3, 30): 'Osnabrück',
              date(2014, 7, 14): 'Ende Lizzy',
              date(2015, 8, 20): 'Nijmegen',
              date(2015, 8, 20): 'NL Galgenveld',
              date(2016, 6, 5): 'NL Timorstraat 1',
              date(2016, 9, 3): 'NL Timorstraat 2',
              date(2017, 4, 1): 'NL Marialaan',
              date(2019, 12, 1): 'LuWi 1',
              date(2021, 10, 22): 'LuWi 2',}
    
    
    files = ospath.list_files(folder, exts='jpg')
    with open('annotations.json', 'r') as f:
        annotations = json.load(f)
        
    dates = [datetime.strptime(key, '%Y.%m.%d %H.%M.%S.jpg').date() for key in annotations]

    fig, axs = plt.subplots(5, 1); axs=axs.flatten()
    for i, emotion in enumerate(['happy', 'sad', 'angry']):
        ax = axs[i]
        vals = [x[engine]['emotion'][emotion] for x in annotations.values()]
        vals = median_filter(vals, size=smooth)
        # vals = np.convolve(vals, np.ones(smooth)/smooth, mode='same')
        
        ax.plot(dates, vals)
        ax.set_xlabel('Zeitpunkt')
        ax.set_ylabel(emotion)
        
        ax.vlines(events.keys(), *ax.get_ylim(), color='black', alpha=0.2,
                   linestyle='dotted')
        for event, desc in events.items():
            ax.text(event, ax.get_ylim()[-1]-5, desc,  rotation=90, va='top')
               

    
    ax = axs[-1]
    vals = [x[engine]['age'] for x in annotations.values()]
    vals = np.convolve(vals, np.ones(smooth)/smooth, mode='same')
    
    ax.plot(dates, vals)
    ax.set_xlabel('Zeitpunkt')
    ax.set_ylabel('Predicted age')
    
    ax.vlines(events.keys(), *ax.get_ylim(), color='black', alpha=0.2,
               linestyle='dotted')
    
    for event, desc in events.items():
        ax.text(event, ax.get_ylim()[-1]-5, desc,  rotation=90, va='top')

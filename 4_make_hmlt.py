# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 10:33:44 2022

@author: Simon
"""
import ospath
import json

folder = ospath.expanduser('./retinaface_annotated/')
engine = 'retinaface'


if __name__=='__main__':
    
    files = ospath.list_files(folder, exts='jpg')

    with open('annotations.json', 'r') as f:
        annotations = json.load(f)

        
    characteristics = {} 
    
    sort_key = lambda arg: arg[1]['age']
    sorted_by_age = sorted(annotations.items(), key=sort_key)
    files_sorted = [x[0] for x in sorted_by_age]
    age_sorted = [x[1]['age'] for x in sorted_by_age]
    characteristics['age'] = [files_sorted, age_sorted]   
    
    sort_key = lambda arg: arg[1][engine]['age']
    sorted_by_age = sorted(annotations.items(), key=sort_key)
    files_sorted = [x[0] for x in sorted_by_age]
    age_sorted = [x[1][engine]['age'] for x in sorted_by_age]
    characteristics['age_pred'] = [files_sorted, age_sorted]
    
    # see what difference in predicted and real age is
    sort_key = lambda arg: arg[1][engine]['age'] - arg[1]['age']
    sorted_by_agediff = sorted(annotations.items(), key=sort_key)
    files_sorted = [x[0] for x in sorted_by_agediff]
    agediff_sorted = [x[1][engine]['age']-x[1]['age']  for x in sorted_by_agediff]
    characteristics['age_diff_to_pred'] = [files_sorted, agediff_sorted]               
    
     
    emotions = ['happy', 'sad', 'angry', 'fear', 'surprise', 'neutral'] 

    for emotion in emotions:
        sort_key = lambda arg: arg[1][engine]['emotion'][emotion]
        sorted_by_emotion = sorted(annotations.items(), key=sort_key)
        files_sorted = [x[0] for x in sorted_by_emotion]
        values_sorted = [x[1][engine]['emotion'][emotion] for x in sorted_by_emotion]
        characteristics[emotion] = [files_sorted, values_sorted]
 
    races = ['asian', 'black', 'indian', 'latino hispanic', 'middle eastern', 'white' ]
    for race in races:
        sort_key = lambda arg: arg[1][engine]['race'][race]
        sorted_by_emotion = sorted(annotations.items(), key=sort_key)
        files_sorted = [x[0] for x in sorted_by_emotion]
        values_sorted = [x[1][engine]['race'][race] for x in sorted_by_emotion]
        characteristics[race] = [files_sorted, values_sorted]
        


    
    
    json_data = json.dumps(characteristics)
    
    html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
.slidecontainer {
  width: 100%;
}

.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 25px;
  background: #d3d3d3;
  outline: none;
  opacity: 0.7;
  -webkit-transition: .2s;
  transition: opacity .2s;
}

.slider:hover {
  opacity: 1;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 25px;
  height: 25px;
  background: #04AA6D;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 25px;
  height: 25px;
  background: #04AA6D;
  cursor: pointer;
}
</style>
</head>
""" + \
f"""
<label for="emotions">Choose emotion or characteristic (base on {engine}):</label>

<select name="characteristics" id="characteristics">
  {' '.join([f'<option value="{chars}">{chars}</option>' for chars in characteristics])}
</select>

<div class="slidecontainer" style="width: 100%;">
    <input type="range" min="0" max="{len(files_sorted)-1}" value="1" class="slider" 
    id="slider{emotion}">
</div>
<div class="slidecontainer">
<p>Value: <span id="demo"></span><br></p>
<img src="./retinaface_annotated/{characteristics['age'][0][0]}" />
</div>
<script> 
const data = {json_data};

var slider = document.getElementById("slider{emotion}");
var selector = document.getElementById("characteristics");
var output = document.getElementById("demo");
output.innerHTML = slider.value;
"""+\
"""
const img = document.querySelector("img");

slider.oninput = function() {
    
  var file = data[selector.value][0][this.value];
  var value = data[selector.value][1][this.value];
  output.innerHTML = value;
  img.src= './retinaface_annotated/' + file;
}

selector.oninput = function() {
    
  var file = data[selector.value][0][slider.value];
  var value = data[selector.value][1][slider.value];
  output.innerHTML = value;
  img.src= './retinaface_annotated/' + file;
}

</script>

"""
    
    with open('index.html', 'w') as f:
        f.write(html)
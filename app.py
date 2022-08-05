# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 10:44:08 2022

@author: Santosh shaha
"""
#Import necessary libraries
from flask import Flask, render_template, request
 
import numpy as np
#import tensorflow as tf
import os
#from PIL import load_img
from tensorflow.keras.utils import load_img 
#from keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from keras.models import load_model
 
#load model
model =load_model("model/tomato_disease_prediction.h5")
 
print('@@ Model loaded')
def pred_tomato_disease_tomato_leaf(tomato_plant):
  test_image = load_img(tomato_plant, target_size = (150, 150)) # load image 
  print("@@ Got Image for prediction")
   
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
   
  result = model.predict(test_image).round(10)# predict diseased palnt or not
  print('@@ Raw result = ', result)
   
  pred = np.argmax(result) # get the index of max value
 
  if pred == 0:
    return "Bacterial_Spot tomato Plant", 'Bacterial_Spot_leaf.html' # if index 0 burned leaf
  elif pred == 1:
      return 'Early_blight tomato Plant', 'Early_Blight_Leaf.html' # # if index 1
  elif pred == 2:
      return 'Late_blight tomato Plant', 'Late_blight.html'  # if index 2  fresh leaf
  elif pred == 3:
      return 'Leaf_Mold tomato Plant', 'Leaf_Mold.html'  # if index 3  fresh leaf
  elif pred == 4:
      return 'Spetoria_leaf_spot tomato Plant', 'Spetorial_leaf_spot.html'  # if index 4 fresh leaf
  elif pred == 5:
      return 'Spider_mites_two_spotted_spider_mite tomato Plant', 'Spider_mites.html'  # if index 5  fresh leaf
  elif pred == 6:
      return 'Target_spot tomato Plant', 'Target_spot.html'  # if index 6  fresh leaf
  elif pred == 7:
      return 'Tomato_yellow_leaf_Curl_virus tomato Plant', 'yellow_curl.html'  # if index 7  fresh leaf
  elif pred == 8:
      return 'Tomato_Mosaic_virus tomato Plant', 'Mosaic_virus.html'  # if index 8  fresh leaf
  else:
    return "Healthy tomato Plant", 'helathy_leaf.html' # if index 9
 
#------------>>pred_tomato_dieas<<--end
     
 
# Create flask instance
app = Flask(__name__)
 
# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')
     
  
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
         
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)
 
        print("@@ Predicting class......")
        pred, output_page = pred_tomato_disease_tomato_leaf(tomato_plant=file_path)
               
        return render_template(output_page, pred_output = pred, user_image = file_path)
     
# For local system & cloud
if __name__ == "__main__":
    app.run(debug=True,threaded=False, port)
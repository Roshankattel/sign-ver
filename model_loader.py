# @Time : 21-12-19
# @Author : RK
# @Company : Digiconnect
# @File : model_loader.py
# @Software : PyCharm


import numpy as np
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import cv2
from PIL import Image


from signver.detector import Detector
from signver.cleaner import Cleaner
from signver.extractor import MetricExtractor
from signver.matcher import Matcher
from signver.utils import data_utils, visualization_utils
from signver.utils.data_utils import invert_img, resnet_preprocess
from signver.utils.visualization_utils import plot_np_array, visualize_boxes, get_image_crops, make_square

INPUT_FILE = "./images/input_files/"
EXTRACT_SIGN = "./images/extracted_signatures/"
INPUT_SIGN = "./images/input_signatures/"


detector_model_path = "./models/detector/small"
detector = Detector()
detector.load(detector_model_path)

extractor_model_path = "models/extractor/metric"
extractor = MetricExtractor() 
extractor.load(extractor_model_path)

cleaner_model_path = "models/cleaner/small"
cleaner = Cleaner() 
cleaner.load(cleaner_model_path)

def covertGreyscale(img_path):
    originalImage = cv2.imread(img_path)
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(img_path, grayImage)

def removeBg(imgPath):
  image = cv2.imread(imgPath)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  blur = cv2.GaussianBlur(gray, (25,25), 0)
  thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
  thresh2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] #only grayscale image

  # Perform morph operations, first open to remove noise, then close to combine
  noise_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
  opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, noise_kernel, iterations=2)
  close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
  close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, close_kernel, iterations=3)

  # Find enclosing boundingbox and crop ROI
  coords = cv2.findNonZero(close)
  x,y,w,h = cv2.boundingRect(coords)
  cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
  crop2 = thresh2[y:y+h, x:x+w]
  cv2.imwrite(imgPath, crop2)


def extractSign(img_name,clean):
    score =0
    img_path = INPUT_FILE + img_name
    covertGreyscale(img_path)
    inverted_image_np = data_utils.img_to_np_array(img_path, invert_image=True)
    img_tensor = tf.convert_to_tensor(inverted_image_np)
    img_tensor = img_tensor[tf.newaxis, ...]
    boxes, scores, classes, detections = detector.detect(img_tensor)
    signatures = get_image_crops(inverted_image_np, boxes, scores,  threshold = 0.22 )
    if(len(signatures)>0):
        sigs= [ resnet_preprocess( x, resnet=False ) for x in signatures ]
        if (clean):
            norm_sigs = [ x * (1./255) for x in sigs]
            sigs = cleaner.clean(np.array(norm_sigs))
            plt.imsave(EXTRACT_SIGN+img_name, sigs[0])
        else:
            image = Image.fromarray(np.uint8(sigs[0]))
            image.save(EXTRACT_SIGN+img_name)
        score = (round(scores[0],4)*100)
    return (score)

def compare(imagea,imageb,clean):
    sim =False
    img_paths =[imagea, imageb]
    [removeBg(img_path) for img_path in img_paths]
    inverted_image_np = [data_utils.img_to_np_array(x, invert_image=True) for x in img_paths]
    sigs= [ resnet_preprocess( x, resnet=False ) for x in inverted_image_np ]
    if(clean):
        norm_sigs = [ x * (1./255) for x in sigs]
        cleaned_sigs = cleaner.clean(np.array(norm_sigs))
        feats = extractor.extract(cleaned_sigs ) 
    else:
        feats = extractor.extract(np.array(sigs) / 255)
    matcher = Matcher()
    distance =matcher.cosine_distance(feats[0],feats[1])
    print(distance)
    similarity = round((1- distance),4)
    if(similarity>1):
        similarity = 1
    elif similarity<0:
        similarity=0
    if (distance<0.3):
        sim = True
    return(sim,(similarity)*100)
    
    

    

    

    
    

    



from keras.models import Sequential
from keras.layers import Conv2D, ZeroPadding2D, Activation, Input, concatenate
from keras.models import Model
from keras.layers import BatchNormalization
from keras.layers.pooling import MaxPooling2D, AveragePooling2D
from keras.layers.core import Lambda, Flatten, Dense
from keras.initializers import glorot_uniform
from keras.layers import Layer
from keras import backend as K
from keras.models import load_model
K.set_image_data_format('channels_first')
import pickle
import os.path
import os
import numpy as np
from numpy import genfromtxt, less_equal
import pandas as pd
import tensorflow as tf
from .utility import *
from .webcam_utility import *
from FaceLogin.models import *



def triplet_loss(y_true, y_pred, alpha = 0.2):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
    print("This is a custom loss function")
    print("y_list:",y_pred)
    
    # triplet formula components
    pos_dist = tf.reduce_sum( tf.square(tf.subtract(y_pred[0], y_pred[1])) )
    neg_dist = tf.reduce_sum( tf.square(tf.subtract(y_pred[0], y_pred[2])) )
    basic_loss = pos_dist - neg_dist + alpha
    
    loss = tf.maximum(basic_loss, 0.0)
   
    return loss


# load the model
def ini_model():
    path = r"FaceLogin/Face_Recognition/model/facenet_keras.h5"
    FRmodel = load_model(path, custom_objects={'triplet_loss': triplet_loss})
    # FRmodel = load_model('models/facenet_keras.h5', compile=False)
    FRmodel.compile(loss=triplet_loss)
    return FRmodel

# initialize the user database
def ini_user_database():
    # check for existing image folder
    if os.path.exists('FaceLogin/Face_Recognition/saved_image/'):
        print("saved_image folder already exist")
    else:
        os.makedirs('FaceLogin/Face_Recognition/saved_image/')
    # check for existing database
    if os.path.exists('FaceLogin/Face_Recognition/database/user_dict.pickle'):
        with open('FaceLogin/Face_Recognition/database/user_dict.pickle', 'rb') as handle:
            user_db = pickle.load(handle)   
    else:
        # make a new one
        # we use a dict for keeping track of mapping of each person with his/her face encoding
        user_db = {}
        # create the directory for saving the db pickle file
        os.makedirs('FaceLogin/Face_Recognition/database/')
        with open('FaceLogin/Face_Recognition/database/user_dict.pickle', 'wb') as handle:
            pickle.dump(user_db, handle, protocol=pickle.HIGHEST_PROTOCOL)   
    return user_db



# adds a new user face to the database using his/her image stored on disk using the image path
def add_user_img_path(user_db, FRmodel, name, img_path):
    try:
        user_db[name] = img_to_encoding(img_path, FRmodel)
        print("Encodings:",user_db[name])
        # save the database
        with open('FaceLogin/Face_Recognition/database/user_dict.pickle', 'wb') as handle:
                pickle.dump(user_db, handle, protocol=pickle.HIGHEST_PROTOCOL)
        os.remove("FaceLogin/Face_Recognition/saved_image/UserGenerated.jpg")
        print('User ' + name + ' added successfully')
        return True
    except:
        return False


# adds a new user using image taken from webcam
def add_user_webcam(user_db, FRmodel, name, password):
    # we can use the webcam to capture the user image then get it recognized
    face_found = detect_face(user_db, FRmodel)
    if face_found:
        img_loc="FaceLogin/Face_Recognition/saved_image/UserGenerated.jpg"
        resize_img(img_loc,(96,96)) 
        bol = add_user_img_path(user_db, FRmodel, name, "FaceLogin/Face_Recognition/saved_image/UserGenerated.jpg")
        UserAccount.objects.create(username=name, password=password)
        return bol
    else:
        return False
        
# deletes a registered user from database
def delete_user(user_db, username):
    popped = user_db.pop(username, None)
    
    if popped is not None:
        print('User ' + username + ' deleted successfully')
        # save the database
        with open('FaceLogin/Face_Recognition/database/user_dict.pickle', 'wb') as handle:
                pickle.dump(user_db, handle, protocol=pickle.HIGHEST_PROTOCOL)
    elif popped == None:
        print('No such user !!')


# recognize the input user face encoding by checking for it in the database
def find_face(image_path, database, model, username, threshold = 0.6):
    # find the face encodings for the input image
    print(image_path)
    encoding = img_to_encoding(image_path, model)
    
    min_dist = 5
    identity = "unknown"
    # loop over all the recorded encodings in database 
    for name in database:
        # find the similarity between the input encodings and claimed person's encodings using L2 norm
        dist = np.linalg.norm(np.subtract(database[name], encoding) )
        # check if minimum distance or not
        if dist < min_dist:
            min_dist = dist
            identity = name
    print("min_dist:",min_dist," and Identity:",identity)
    
    if min_dist < threshold: #condition reversed
        #print("User not in the database.")
        identity = 'Unknown Person'
    if  min_dist >= 5:
        print("User not in the database.")
        identity = 'Unknown Person'
        #print("dist:",dist," and Identity:",identity)
    else:  
        print ("Hi! " + str(identity) + ", L2 distance: " + str(min_dist))
    
    os.remove("FaceLogin/Face_Recognition/saved_image/UserGenerated.jpg")
    return username == identity  

# takes an input image from webcam and performs face recognition on it
def do_face_recognition_webcam(user_db, FRmodel, username, threshold = 0.7):
    # we can use the webcam to capture the user image then get it recognized
    face_found = detect_face(user_db, FRmodel)

    if face_found:
        # resize the image for the model
        img_loc="FaceLogin/Face_Recognition/saved_image/UserGenerated.jpg"
        resize_img(img_loc,(96,96))
        return find_face(img_loc, user_db, FRmodel, username, threshold)
    else:
        print('There was no face found in the visible frame. Try again...........')
        
    

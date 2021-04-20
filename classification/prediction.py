import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
import time

start = time.time()

# #Define Path
# model_path = 'classification/models_cnn/arsitektur.h5'
# model_weights_path = 'classification/models_cnn/arsitektur_weights.h5'
# test_path_crop = 'data/alien_test'
# test_path_non_crop = 'data/alien_test_non_crop'

# #Load the pre-trained models
# model = load_model(model_path)
# model.load_weights(model_weights_path)

# #Define image parameters
# img_width, img_height = 224, 224

# #Prediction Function
# def predict(file):
#   x = load_img(file, target_size=(img_width,img_height))
#   x = img_to_array(x)
#   x = np.expand_dims(x, axis=0)
#   array = model.predict(x)
#   result = array[0]
#   #print(result)
#   answer = np.argmax(result)
#   if answer == 0:
#     print("Predicted: melanoma")
#   elif answer == 1:
#     print("Predicted: nevus")
#   elif answer == 2:
#     print("Predicted: uda-1")
#   return answer
# true_total = 0
# true_total_crop = 0
# #Walk the directory for every image
# for i, ret in enumerate(os.walk(test_path_non_crop)):
#   for i, filename in enumerate(ret[2]):
#     if filename.startswith("."):
#       continue
    
#     # Splitting at ':' 
#     a = filename.split('(') 
#     b = a[1].split(')')
#     print(b[0])
#     print(ret[0] + '/' + filename)
#     result = predict(ret[0] + '/' + filename)
#     if int(b[0]) <= 20:
#       if result == 0:
#           true_total = true_total + 1
#     if int(b[0]) > 20  and int(b[0]) <=40:
#       if result == 1:
#           true_total = true_total + 1
#     if int(b[0])> 40 and int(b[0]) <=60:
#       if result == 2:
#           true_total = true_total + 1
#     print(" ")


# for i, ret in enumerate(os.walk(test_path_crop)):
#   for i, filename in enumerate(ret[2]):
#     if filename.startswith("."):
#       continue
    
#     # Splitting at ':' 
#     a = filename.split('(') 
#     b = a[1].split(')')
#     print(b[0])
#     print(ret[0] + '/' + filename)
#     result = predict(ret[0] + '/' + filename)
#     if int(b[0]) <= 20:
#       if result == 0:
#           true_total_crop = true_total_crop + 1
#     if int(b[0]) > 20  and int(b[0]) <=40:
#       if result == 1:
#           true_total_crop = true_total_crop + 1
#     if int(b[0])> 40 and int(b[0]) <=60:
#       if result == 2:
#           true_total_crop = true_total_crop + 1
#     print(" ")

# print("jumlah benar "+ str(true_total) )
# print("akurasi "+ str((true_total/60) * 100) +" %" )
 
# print("jumlah benar crop "+ str(true_total_crop) )
# print("akurasi crop "+ str((true_total_crop/60) * 100) +" %" )


# #Calculate execution time
# end = time.time()
# dur = end-start

# if dur<60:
#     print("Execution Time:",dur,"seconds")
# elif dur>60 and dur<3600:
#     dur=dur/60
#     print("Execution Time:",dur,"minutes")
# else:
#     dur=dur/(60*60)
#     print("Execution Time:",dur,"hours")


#Prediction Function
def predict(prediction_images, model_path, model_weights_path):
    #Define Path
    # model_path = 'classification/model_cnn/arsitektur.h5'
    # model_weights_path = 'classification/model_cnn/arsitektur_weights.h5'
    
    media_path = 'media'

    #Load the pre-trained models
    with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
        model = load_model("{}/{}".format(media_path, model_path))
        model._make_predict_function()
        model.load_weights("{}/{}".format(media_path, model_weights_path))

    #Define image parameters
    img_width, img_height = 188, 188

    results = []
    # mapping
    variable_mapping = {
        0: 'melanoma',
        1: 'nevus'
    }

    correct = 0

    for image in prediction_images:
        image_path = image.image
        image_nama = image.nama
        
        # load image
        image_file = load_img("{}/{}".format(media_path, image_path), target_size=(img_width,img_height))
        array_image = img_to_array(image_file)
        add_array = np.expand_dims(array_image, axis=0)
        prediction = model.predict(add_array)[0]
        answer = np.argmax(prediction)
        
        # Labels
        if answer == 0:
            prediction_label = "melanoma"
        else :
            prediction_label = "nevus"
       
        # Accuracy
        if image_nama == variable_mapping[answer]:
            correct += 1

        # Context
        context = {
            'prediction_label': prediction_label,
            'actual_label': image_nama,
            'image_url': image_path.url
        }
        results.append(context)
        
    acc = correct/len(prediction_images) * 100


    return results, acc
    

#   image = load_img(file_path, target_size=(img_width,img_height))
#   image = img_to_array(image)
#   image = np.expand_dims(image, axis=0)
#   array = model.predict(image)
#   result = array[0]
  
#   print(result)



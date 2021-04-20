from django.contrib import admin
from django.urls import path, include
from classification import views

urlpatterns = [
    path('', views.UploadModelView.as_view(), name='upload_model_prediction'),
    path('predict', views.ImagePredictionView.as_view(), name='upload_image_prediction')
]
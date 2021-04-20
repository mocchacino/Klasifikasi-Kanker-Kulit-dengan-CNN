from django import forms
from .models import PredictionImage, PredictionModel

class ImagePredictionForm(forms.ModelForm):
    class Meta:
        model = PredictionImage
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class UploadModelForm(forms.ModelForm):
    class Meta:
        model = PredictionModel
        fields = ('model', 'model_weights',)
        widgets = {
            'model': forms.ClearableFileInput(attrs={'multiple': False}),
            'model_weights': forms.ClearableFileInput(attrs={'multiple': False}),
        }
        

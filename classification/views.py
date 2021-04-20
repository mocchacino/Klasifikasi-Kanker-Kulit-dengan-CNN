from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import ImagePredictionForm, UploadModelForm
from django.http import HttpResponse
from .models import PredictionImage, PredictionModel
from .prediction import predict
from django.shortcuts import redirect
import os

def get_label(image, delimiter):
    return image.split(delimiter)[0]

class UploadModelView(FormView):
    form_class = UploadModelForm
    template_name = 'upload-model.html'
    success_url = '...'

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        # Clean upload directory
        all_model = PredictionModel.objects.all()
        for model in all_model:
            path_model = "media/{}".format(model.model)
            path_weights = "media/{}".format(model.model_weights)
            # remove file
            if os.path.isfile(path_model):
                os.remove(path_model)
            if os.path.isfile(path_weights):
                os.remove(path_weights)
            # Finally delete from db
            model.delete()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        model = request.FILES['model']
        model_weights = request.FILES['model_weights']

        if form.is_valid():
            prediction_model = PredictionModel()
            prediction_model.model = model
            prediction_model.model_weights = model_weights
            prediction_model.save()
            
            return redirect('/prediction/predict')

        else:
            return self.form_invalid(form)

class ImagePredictionView(FormView):
    form_class = ImagePredictionForm
    template_name = 'upload-image.html' 
    success_url = '...'

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        # Clean upload directory
        all_image = PredictionImage.objects.all()
        for image in all_image:
            path = "media/{}".format(image.image)
            if os.path.isfile(path):
                os.remove(path)
            # Finally delete from db
            image.delete()
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('image')       
        if form.is_valid():
            for f in files:
                image = PredictionImage()
                label = get_label(f.name, '_')
                image.nama = label
                image.image = f
                image.save()

            all_image = PredictionImage.objects.all()
            all_model = PredictionModel.objects.all()

            results, acc = predict(all_image, all_model[0].model, all_model[0].model_weights)
            context = {
                'results': results,
                'accuracy': acc
            }
            
            return render(request, 'result.html', context=context)
        else:
            return self.form_invalid(form)
    
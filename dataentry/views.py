from django.shortcuts import render, redirect
from .utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages

def import_data(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        # Store the file inside Upload Model
        upload = Upload.objects.create(file=uploaded_file, model_name=model_name)

        # Get Full Path
        file_path = str(upload.file.path)  # Correct way to get absolute file path

        # Trigger the importdata command
        try:
            call_command('importdata', file_path, model_name)
            messages.success(request,'Data imported successfully !')
        except Exception as e:
            messages.error(request,str(e))

        return redirect('import_data')
    
    else:
        custom_models = get_all_custom_models()
        context = {'custom_models': custom_models}
        return render(request, 'dataentry/importdata.html', context)

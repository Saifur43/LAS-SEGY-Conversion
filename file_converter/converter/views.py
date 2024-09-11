import os
from django.shortcuts import render
from django.conf import settings
from .forms import FileUploadForm
from .utils import convert_las_to_jpg, convert_sgy_to_jpg

def file_upload_view(request):
    converted_image_url = None  # Initialize with no image URL at first
    
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            file_path = uploaded_file.file.path
            
            # Determine file extension and handle accordingly
            ext = os.path.splitext(file_path)[1].lower()
            output_filename = f"{uploaded_file.id}.jpg"
            output_path = os.path.join(settings.MEDIA_ROOT, 'converted', output_filename)
            
            # Convert LAS or SEG-Y based on file extension
            if ext == '.las':
                convert_las_to_jpg(file_path, output_path)
            elif ext == '.sgy':
                convert_sgy_to_jpg(file_path, output_path)

            # Construct the URL for the converted image
            converted_image_url = os.path.join(settings.MEDIA_URL, 'converted', output_filename)
        else:
            form = FileUploadForm()  # Reinitialize form if invalid
    
    else:
        form = FileUploadForm()

    return render(request, 'converter/upload.html', {'form': form, 'converted_image': converted_image_url})




def homepage(request):
    return render(request, 'converter/homepage.html')  # Render homepage

# View for LAS converter
def las_converter_view(request):
    converted_image_url = None
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            file_path = uploaded_file.file.path
            output_filename = f"{uploaded_file.id}.jpg"
            output_path = os.path.join(settings.MEDIA_ROOT, 'converted', output_filename)
            
            # Convert LAS file
            convert_las_to_jpg(file_path, output_path)
            converted_image_url = os.path.join(settings.MEDIA_URL, 'converted', output_filename)
    else:
        form = FileUploadForm()

    return render(request, 'converter/las_converter.html', {'form': form, 'converted_image': converted_image_url})

# View for SEG-Y converter
def sgy_converter_view(request):
    converted_image_url = None
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            file_path = uploaded_file.file.path
            output_filename = f"{uploaded_file.id}.jpg"
            output_path = os.path.join(settings.MEDIA_ROOT, 'converted', output_filename)
            
            # Convert SEG-Y file
            convert_sgy_to_jpg(file_path, output_path)
            converted_image_url = os.path.join(settings.MEDIA_URL, 'converted', output_filename)
    else:
        form = FileUploadForm()

    return render(request, 'converter/sgy_converter.html', {'form': form, 'converted_image': converted_image_url})


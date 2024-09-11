from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Homepage to navigate to converters
    path('convert/las/', views.las_converter_view, name='las_converter'),  # LAS converter page
    path('convert/sgy/', views.sgy_converter_view, name='sgy_converter'),  # SEG-Y converter page
]

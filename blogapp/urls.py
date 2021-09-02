from django.urls import path
from . import views

urlpatterns = [
    # this represent the home page url
    path('',views.index)

]

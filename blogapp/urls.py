from django.urls import path
from . import views

urlpatterns = [
    # this represent the home page url
    # path('',views.IndexPageListView.as_view())
    path('',views.index,name='home'),
    path('post/<int:pk>/',views.PostDetail.as_view(),name='post-detail')

]

from django.urls import path,include
from . import views


urlpatterns = [
    # this represent the home page url
    # path('',views.IndexPageListView.as_view())
    path('',views.index,name='home'),
    path('post/<int:pk>/',views.PostDetail.as_view(),name='post-detail'),
    path('comment/<int:pk>/',views.create_comment,name='create_comment'),
    path('api/likes_and_dislike/<int:pk>/',views.increment_BlogLikes,name='likes_and_dislike'),
    path('filter/<searchKeyword>/<categories>/',
    views.filter_view,name='filter')

]

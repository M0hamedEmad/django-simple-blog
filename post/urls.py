from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('post/create', views.createPost, name='create_post'),

    path('<str:slug>/', views.post, name='post'),
    path('<str:slug>/edit/', views.updatePost, name='update_post'),
    path('<str:slug>/delete/', views.deletePost, name='delete_post'),

 
]
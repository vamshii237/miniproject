from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList, name='blog-home'),
    path('create-faq/', views.faq_create, name='faq-creation'),
    path('list-faq/', views.FAQList,name='list-faq'),
    path('list-faq/<slug:slug>/', views.faq_detail,  name='faq_detail'),

    path('create-post/', views.post_create, name='post_creation'),
    path('<slug:slug>/', views.post_detail,  name='post_detail'),
]
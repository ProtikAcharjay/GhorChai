from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('<int:post_id>/view/', views.post_view, name='post_view'),
    path('<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('register/', views.register, name='register'),
    path('<int:post_id>/react/', views.post_reaction, name='post_reaction'),
]

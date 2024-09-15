from django.urls import path

from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.pet_list, name='pet_list'),
    path('add/', views.add_pet, name='add_pet'),
    path('<int:pet_id>/edit/', views.edit_pet, name='edit_pet'),
    path('<int:pet_id>/delete/', views.delete_pet, name='delete_pet'),
    path('image/<int:image_id>/delete/', views.delete_pet_image, name='delete_pet_image'),
    path('<int:pet_id>/images/', views.get_pet_images, name='get_pet_images'),
]
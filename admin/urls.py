"""URL Config for admin app."""

from django.urls import path

from . import views

app_name = 'admin'

urlpatterns = [
    path('users/', views.users, name='users'),
    path('users/delete/', views.delete_user, name='delete_user'),
    path('users/create/', views.create_user, name='create_user'),
    path('reset_collabodev/', views.reset_collabodev, name='reset_collabodev'),
    path('reset_page/', views.reset_page, name='reset_page'),
    path('github/', views.github, name='github'),
    path('update/', views.update, name='update'),
]

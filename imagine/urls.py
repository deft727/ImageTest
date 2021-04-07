from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
        path('',IndexView.as_view(),name='home'),
        path('new_image/',NewImage.as_view(),name='add'),
        path('galery_detail/<int:pk>/',GalleryDetail.as_view(),name='detail'),
        path('registration/',RegistrationView.as_view(), name='registration'),
        path('login/',LoginView.as_view(), name='login'),
        path('logout/',LogoutView.as_view(next_page="/"), name='logout'),
        path('profile/',ProfileView.as_view(),name='profile'),
                ]
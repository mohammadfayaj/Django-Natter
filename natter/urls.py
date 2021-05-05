from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path
from natter import views


app_name = 'natter'

urlpatterns = [
    path('', views.home, name='home'),

    path('group_chat/', views.index, name='index'),
    path('<int:id>/', views.create_friend, name='create-friend'),
    path('remove/<str:room_name>/', views.remove_group, name='remove-group'),
    path('<str:room_name>/', login_required(views.room), name='room'),
]

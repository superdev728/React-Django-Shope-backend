# Connect the views to urls

from django.urls import path
from base.views import user_views as views       # same folder just "."


urlpatterns = [
    path('login_client/', views.MyTokenObtainPairView.as_view(), 
        name='token_obtain_pair'),

    path('register/', views.registerUser, name="register"),

    path('profile/', views.getUserProfile, name="users-profile"),
    path('profile/update/', views.updateUserProfile, name="user-profile-update"),
    path('', views.getUsers, name="users"),

    path('<str:pk>/', views.getUserById, name='user'),

    path('update/<str:pk>/', views.updateUser, name='user-update'),

    path('delete/<str:pk>/', views.deleteUser, name='user-delete'),

]


# Connect the views to urls

from django.urls import path
from base.views import shop_views as views       # same folder just "."


urlpatterns = [

    path('', views.getShops, name="shops"),
    path('<str:pk>/', views.getShop, name="shop"),

   # path('create_shop/', views.createShop, name="shop-create"),
    path('top_shop/', views.getTopShops, name='top-shops'),
  #  path('upload_shop/', views.uploadImage, name="image-upload"),

    path('<str:pk>/reviews_shop/', views.createShopReview, name="create-review_shop"),

   #path('update_shop/<str:pk>/', views.updateShop, name="shop-update"),
    #path('delete_shop/<str:pk>/', views.deleteShop, name="shop-delete"),
]



from django.urls import path
from . import views1 #import ItemAPIView,views1

# urlpatterns = [
#     path('items/', ItemAPIView.as_view(), name='item-api'),
# ]
urlpatterns = [
    path('create',views1.createuser, name='create'),
    path('getusers',views1.getusers, name='getusers'),
    path('getuser',views1.getuser, name='getuser'),
    path('update',views1.updateuser, name='create'),
    path('delete',views1.deleteuser, name='create')
]

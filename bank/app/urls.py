from django.urls import path
from . import views

urlpatterns=[
    path('',views.home),
    path('1/',views.create,name="create"),
    path('2/', views.pin,name="pin"),
    path('3/',views.balance,name="balance"),
     path('5/',views.depist,name="depist"),
    path('4/',views.withdraw,name="withdraw"),
   
    path('6/',views.acctrancefore,name="acctrancefore")
]
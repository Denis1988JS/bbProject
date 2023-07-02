from  django.urls import path
from .views import bbs, BbDetailView

urlpatterns = [
    path('bbs/',bbs),#Api - список объявлений
    path('bbs/<int:pk>',BbDetailView.as_view()),#Api - объявление по id
]

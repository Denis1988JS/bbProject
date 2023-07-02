from django.contrib import admin
from django.urls import path
from .views import index, about, LoginUser,profile, LogoutPage,ChangeUserInfoView,ChangePasswordUser,RegisterUserView, \
     DeleteUserView, by_rubric, detail, profile__bb_add,profile_bb_change, profile_bb_delete

urlpatterns = [
    path('accounts/login', LoginUser.as_view(),name='login'),#Авторизация пользователя
    path('about/', about, name='about'),#Страница о сайте
    path('profile/change', ChangeUserInfoView.as_view(), name='changeProfile'),#Изменение данных пользователя
    path('profile/changePassword', ChangePasswordUser.as_view(), name='changePassword'),#Изменение пароля пользователя
    path('profile/', profile, name='profile'),#Страница профиль пользователя
    path('profile/add',profile__bb_add,name='profile__bb_add'),#Добавление объявления
    path('profile/change/<int:pk>',profile_bb_change,name='profile_bb_change'),#Исправление объявления
    path('profile/delete/<int:pk>',profile_bb_delete,name='profile_bb_delete'),#Удаление объявления
    path('register/', RegisterUserView.as_view(), name='register'),#Страница регистрация пользователя
    path('logout/', LogoutPage.as_view(), name='logout'),#Выход пользователя
    path('delete_user/', DeleteUserView.as_view(), name='delete_user'),#Удаление пользователя
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),#Страница с объявлением
    path('<int:pk>/', by_rubric, name='by_rubric'),#Рубрика по id

    path('', index, name='index'),#Главная страница
]

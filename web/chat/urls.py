from django.urls import path
from .views import home_page, chat_page, chat_api, reset_chat

urlpatterns = [
    path("", home_page, name="home"),
    path("chat/", chat_page, name="chat_page"),
    path("api/", chat_api, name="chat_api"),
    path("reset/", reset_chat, name="reset_chat"),
]
from django.contrib import admin
from django.urls import path, include
from web.chat.views import home_page

urlpatterns = [
    path("", home_page, name="home"),
    path("chat/", include("chat.urls")),
    path("admin/", admin.site.urls),
]


from django.contrib import admin
from django.urls import path, include


app_name = "blog"
urlpatterns = [
    path("", include('blog.urls')),
    path("admin/", admin.site.urls),

]

"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from main import views as main_views

urlpatterns = [
    path('users/', include('users.urls')),
    path('', main_views.index, name="index"),
    path('img/', main_views.img_to_arr, name="img_to_arr"),
    path('admin/', admin.site.urls),
    path('solve/', main_views.solve_sudoku, name='solve_sudoku'),
    path('new/', main_views.get_sudoku_arr, name='get_sudoku_arr'),
]
"""rideshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from ride import views as ride_views

urlpatterns = [
    path('create_ride/',ride_views.create_ride,name='create_ride'),
    path('view_open/',ride_views.view_open,name='view_open'),
    path('owner_view_open/<int:ride_detail_id>/',ride_views.owner_view_open,name='owner_view_open'),
    path('sharer_view_open/<int:ride_detail_id>/',ride_views.sharer_view_open,name='sharer_view_open'),
    path('edit_ride/',ride_views.edit_ride,name='edit_ride'),
    path('sharer_edit_ride/',ride_views.sharer_edit_ride,name='sharer_edit_ride'),
    path('owner_edit_fail/',ride_views.owner_edit_fail,name='owner_edit_fail'),
    path('create_ride_success/',ride_views.create_ride_success,name='create_ride_success'),
    path('search_ride/', ride_views.search_ride, name='search_ride'),
    path('driver_search_ride/', ride_views.driver_search_ride, name='driver_search_ride'),
    path('join_ride/', ride_views.join_ride, name='join_ride'),
    path('confirm_ride/<int:ride_detail_id>/', ride_views.confirm_ride, name='confirm_ride'),
    path('complete_ride/<int:ride_detail_id>/', ride_views.complete_ride, name='complete_ride'),
    path('driver_view_confirmed/',ride_views.driver_view_confirmed, name='driver_view_confirmed'),
    path('admin/', admin.site.urls),
]

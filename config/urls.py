from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.track_index, name="track-index"),
    path('tracks/<int:track_id>/', views.track_records, name='track-times'),
    path('debug/', views.debug, name="debug"),
    path('admin/', admin.site.urls),
]

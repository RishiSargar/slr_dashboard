from django.urls import path

from . import views

urlpatterns = [
    path('getGranularData/<str:table>/<str:deviceId>/<str:granularity>', views.getGranularData),
    path('getRawData/<str:table>/<str:deviceId>', views.getRawData),
    path('displayDashboard', views.displayDashboard, name='index'),
    path('getCurrentValues/<str:table>/<str:deviceId>', views.getCurrentValues, name='index'),
    path('', views.HomeView.as_view(), name='home')
]
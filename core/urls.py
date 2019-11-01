from django.urls import path

from .views import TodayListView

urlpatterns = [
    path('', TodayListView.as_view(), name='home'),
]

from django.urls import path

from .views import (
    TodayListView, TomorrowListView,
    YesterdayListView, LiveListView,
    HighlightsListView
)

urlpatterns = [
    path('', TodayListView.as_view(), name='home'),
    path('tomorrow/', TomorrowListView.as_view(), name='tomorrow-matches'),
    path('yesterday/', YesterdayListView.as_view(), name='yesterday-matches'),
    path('live/', LiveListView.as_view(), name='live-matches'),
    path('highlights/', HighlightsListView.as_view(), name='match-highlights'),
]

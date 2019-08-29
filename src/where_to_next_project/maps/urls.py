from django.conf.urls import url
from maps.views import HomeView, TestView, ResultsView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name = 'Maps-Home'),
    url(r'^testmode/', TestView.as_view(), name = 'Maps-Test'),
    url(r'^results/', ResultsView.as_view(), name = 'Maps-Results'),
]

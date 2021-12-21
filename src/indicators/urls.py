from django.urls import path
from . import views

# url path as in the http response, it connects the url with the view and the name
urlpatterns = [
    path("countries/", views.CountriesView.as_view(), name="countries"),
    path("countries/<int:pk>/", views.IndicatorView.as_view(), name="indicators"),
    path("", views.HomeView.as_view(), name="home"),
]

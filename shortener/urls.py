from django.urls import path
from shortener.views import ExpandURLView, RedirectShortURLView, ShortenURLView

urlpatterns = [
    path("shorten/", ShortenURLView.as_view(), name="shorten-url"),
    path("expand/<str:short_code>/", ExpandURLView.as_view(), name="expand-url"),
    path("shrt/<str:short_code>/", RedirectShortURLView.as_view(), name="redirect-url"),
]

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/polls/')),
    path('polls/', include('polls.urls')),
    path("polls/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls)
]
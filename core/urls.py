from django.urls import path
from core.views import frontpage, about

app_name = "core"

urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('about/', about, name='about'),
]
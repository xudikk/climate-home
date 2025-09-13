from django.urls import path
from .views import index, detail, send_message



urlpatterns = [
    path("", index, name='home'),
    path("ctg/<slug>/", index, name='ctg_filter'),
    path('detail/<int:pk>/', detail, name='detail'),
    path('send/', send_message, name='send_message')

]






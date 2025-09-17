from django.urls import path
from .views import index, detail, send_message, product



urlpatterns = [
    path("", index, name='home'),
    path("ctg/<slug>/", index, name='ctg_filter'),
    path('detail/<int:pk>/', detail, name='detail'),
    path('send/', send_message, name='send_message'),
    path("products/", product, name='products'),
    path("products/ctg-<slug>", product, name='products-ctg'),

]






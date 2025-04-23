from django.urls import path
from . import views

app_name = 'ecommerce_app'

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('search/', views.search_books, name='search_books'),  # Search Books page
]

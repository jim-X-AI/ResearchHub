from . import views
from django.urls import path
app_name = 'resources'
urlpatterns = [
    path('fetch_resources/', views.fetch_resources, name='fetch_resources'),
    path('resources/download_video/<str:video_id>/', views.download_video, name='download_youtube_video'),

    # path('resources/download_udemy_course/', views.download_udemy_course, name='download_udemy_course'),
    # path('download_libgen_book/<str:book_id>/', views.download_libgen_book, name='download_libgen_book'),
]
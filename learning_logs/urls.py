"""Defines url patterns for learning_log"""
from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Home page
    # path('', views.index, name='index'),
    # Topics Page
    path('topics', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Page to add topics
    path('new_topic', views.new_topic, name='new_topic'),
    # Page to add new entries
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # page to edit
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # To add and share what I have learnt
    path('share_learning/', views.share_learning, name='share_learning'),
    path('learning_entries', views.learning_entries, name='learning_entries'),
    path('topic/<int:topic_id>/edit/', views.edit_topic, name='edit_topic'),
    path('topic/<int:topic_id>/delete/', views.delete_topic, name='delete_topic'),
]

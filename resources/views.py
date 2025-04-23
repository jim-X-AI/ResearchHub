import json
import logging
import os
import re
import requests
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from yt_dlp import YoutubeDL
from django.conf import settings
from django.views.decorators.http import require_GET

# Sanitize filename function for proper formatting
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def get_zlib_url(title):
    """Construct a Z-Library URL based on book title"""
    base_url = "https://www.zlib.pub/search/"
    query = title.replace(' ', '+')
    return f"{base_url}{query}"

def fetch_resources(request):
    query = request.GET.get('q', '')
    searchby = request.GET.get('searchby', 'all')  # Default to 'all'
    videos = []
    books = []
    articles = []

    if query:
        if searchby in ['all', 'videos']:
            # Fetch YouTube videos
            api_key = settings.YOUTUBE_API_KEY
            url = 'https://www.googleapis.com/youtube/v3/search'
            params = {
                'part': 'snippet',
                'q': query,
                'key': api_key,
                'maxResults': 100,
                'type': 'video'
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    video = {
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'thumbnail': item['snippet']['thumbnails']['default']['url'],
                        'video_id': item['id']['videoId']
                    }
                    videos.append(video)

        if searchby in ['all', 'books']:
            # Fetch books using Google Books API and include Z-Library download link
            books = fetch_google_books(query)

        if searchby in ['all', 'articles']:
            # Fetch research articles from CORE API
            articles = fetch_core_articles(query)

    context = {
        'videos': videos,
        'books': books,
        'articles': articles,
        'query': query,
        'searchby': searchby
    }
    return render(request, 'resources/resource_search.html', context)

def fetch_google_books(query):
    google_books_api_key = settings.GOOGLE_BOOKS_API_KEY
    search_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': query, 'maxResults': 40, 'key': google_books_api_key}

    try:
        response = requests.get(search_url, params=params)
        if response.status_code == 200:
            books_data = response.json().get('items', [])
            books = []
            for item in books_data:
                volume_info = item.get('volumeInfo', {})
                book_info = {
                    'title': volume_info.get('title', 'No Title'),
                    'author': ', '.join(volume_info.get('authors', [])) if volume_info.get('authors') else 'No Author',
                    'published_date': volume_info.get('publishedDate', 'No Date'),
                    'cover_url': volume_info.get('imageLinks', {}).get('thumbnail', 'No Image'),
                    'description': volume_info.get('description', 'No Description'),
                    'info_link': volume_info.get('infoLink', ''),
                    'zlib_link': get_zlib_url(volume_info.get('title', 'No Title'))  # Z-Library download link
                }
                books.append(book_info)
            return books
        else:
            return []
    except requests.RequestException:
        return []

def fetch_core_articles(query):
    search_url = 'https://api.core.ac.uk/v3/data-providers/86/outputs'
    search_params = {'q': query, 'limit': 100}
    headers = {'Authorization': f'Bearer {settings.CORE_API_KEY}'}

    try:
        response = requests.get(search_url, headers=headers, params=search_params)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            return []
    except requests.RequestException:
        return []

logging.basicConfig(level=logging.INFO)

# Function to handle download progress
def progress_hook(d):
    if d['status'] == 'downloading':
        progress = d['_percent_str'].strip()
        print(f"Download progress: {progress}")
        # You can send the progress to the browser using WebSockets or simply log it for now

@require_GET
def download_video(request, video_id):
    """View for downloading YouTube videos directly to user's download directory."""
    try:
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Set up yt-dlp options
        output_path = os.path.expanduser('~/Downloads')  # Get user's default download directory
        ffmpeg_path = r"C:\Users\hp\PycharmProjects\learning_log\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"  # Update to your FFmpeg location

        # yt-dlp options for 720p download and progress hook
        ydl_opts = {
            "outtmpl": f"{output_path}/%(title)s.%(ext)s",  # Download to user's download folder
            "format": "bestvideo[height=720]+bestaudio/best",  # Download 720p video and best audio
            "noplaylist": True,  # Download single video, no playlists
            "quiet": False,  # Disable quiet mode
            "merge_output_format": "mp4",  # Merge video/audio into MP4 using FFmpeg
            "ffmpeg_location": ffmpeg_path,  # Manually specify FFmpeg location
            "postprocessos": [{  # Use FFmpeg to merge audio and video
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }],
            "progress_hooks": [progress_hook],  # Add progress hook for real-time progress updates
        }

        # Start downloading the video
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = sanitize_filename(info_dict.get('title', 'video')) + '.mp4'
            video_download_url = info_dict['formats'][0]['url']

            # Log the video URL and title
            logging.info(f"Video URL: {video_download_url}")
            logging.info(f"Downloading: {video_title}")

            # Stream video and save to user's download directory
            ydl.download([video_url])

            # Inform the user that the file has been downloaded to their Downloads directory
            return HttpResponse(f"Video '{video_title}' has been downloaded to your Downloads folder. Just search for the video ")

    except Exception as e:
        logging.error(f"Error downloading video: {str(e)}")
        return HttpResponseBadRequest(f"An error occurred: {str(e)}")
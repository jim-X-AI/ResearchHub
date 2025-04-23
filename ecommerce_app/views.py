from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests


def search_books(request):
    query = request.GET.get('query', '')
    search_by = request.GET.get('search_by', 'title')
    page_number = request.GET.get('page', 1)
    start_index = (int(page_number) - 1) * 9  # Display 9 results per page
    max_results = 40
    books = []
    error = None

    if query:
        try:
            # Fetch books based on search criteria with pagination
            response = fetch_books(query, search_by, start_index, max_results)
            if response:
                books = response
            else:
                error = 'No books found'
        except Exception as e:
            error = f'An error occurred: {str(e)}'
    else:
        # Fetch the most rated books if no query is provided
        books = fetch_most_rated_books()

    paginator = Paginator(books, max_results)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Update book list with purchase URLs based on title
    for book in page_obj.object_list:
        book.update({
            # The purchase links
            'amazon_url': get_amazon_url(book['title']),
            'ebay_url': get_ebay_url(book['title']),
            'barnes_and_noble_url': get_barnes_and_noble_url(book['title']),
            'book_depository_url': get_book_depository_url(book['title']),
            'books_a_million_url': get_books_a_million_url(book['title']),
            # The download links
            'zlib_url': get_zlib_url(book['title']),
            'libary_genesis_url': get_library_genesis_url(book['title']),
            'pdf_drive_url': get_pdf_drive_url(book['title']),
            'project_gutenberg_url': get_project_gutenberg_url(book['title']),
            'open_libary_url': get_open_libary_url(book['title']),
            'google_scholar_url': get_google_scholar_url(book['title']),
            'internet_archive_url': get_internet_archive_url(book['title']),
            # The read on links
            'scribd': get_scribd_url(book['title']),
            'kobo_books': get_kobo_books_url(book['title']),
            'audible_url': get_audible_url(book['title']),
            'barnes_nobles': get_barnes_nobles_url(book['title'])

        })

    # Render the search results template
    return render(request, 'ecommerce_app/search_results.html', {
        'books': page_obj,
        'query': query,
        'search_by': search_by,
        'error': error,
    })


def fetch_books(query, search_by, start_index=0, max_results=40):
    """Fetch books from an API based on search criteria with pagination support."""
    api_url = (
        f'https://www.googleapis.com/books/v1/volumes'
        f'?q={search_by}:{query}'
        f'&startIndex={start_index}'
        f'&maxResults={max_results}'
    )
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        books = []
        for item in data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            title = volume_info.get('title', 'No Title')
            book = {
                'title': title,
                'author': ', '.join(volume_info.get('authors', [])),
                'description': volume_info.get('description', 'No Description'),
                'isbn': next((identifier['identifier'] for identifier in volume_info.get('industryIdentifiers', []) if
                              identifier['type'] == 'ISBN_13'), ''),
                'published_date': volume_info.get('publishedDate', 'No Date'),
                'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', 'https://via.placeholder.com/150')
            }
            books.append(book)
        return books
    return None


# The buy on links
def get_amazon_url(title):
    """Construct an Amazon search URL based on the book title."""
    base_url = "https://www.amazon.com/s"
    query = title.replace(' ', '+')
    return f"{base_url}?k={query}"


def get_ebay_url(title):
    """Construct an eBay search URL based on the book title."""
    base_url = "https://www.ebay.com/sch/i.html"
    query = title.replace(' ', '+')
    return f"{base_url}?_nkw={query}"


def get_barnes_and_noble_url(title):
    """Construct a Barnes & Noble search URL based on the book title."""
    base_url = "https://www.barnesandnoble.com/s/"
    query = title.replace(' ', '+')
    return f"{base_url}{query}"


def get_book_depository_url(title):
    """Construct a Book Depository search URL based on the book title."""
    base_url = "https://www.bookdepositoryus.com/?s="
    query = title.replace(' ', '+')
    return f"{base_url}{query}"


def get_books_a_million_url(title):
    """Construct a Books-A-Million search URL based on the book title."""
    base_url = "https://www.booksamillion.com/search?query="
    query = title.replace(' ', '+')
    return f"{base_url}{query}"


# The download on links
def get_zlib_url(title):
    """Construct a zlib url based on book title"""
    base_url = "https://www.zlib.pub/search/"
    query = title.replace(' ', '+')
    return f"{base_url}{query}"


def get_library_genesis_url(title):
    base_url = "https://libgen.is/search.php?req="
    query = title.replace(' ', '+')
    return f"{base_url}{query}"


def get_pdf_drive_url(title):
    base_url = "https://www.pdfdrive.com/search?q="
    query = title.replace(' ', '+')
    return f"{base_url}{query}"


def get_project_gutenberg_url(title):
    base_url = "https://www.gutenberg.org/ebooks/search/?query="
    query = title.replace(' ', '+')
    return f"{base_url}{query}"


def get_open_libary_url(title):
    base_url = "https://openlibrary.org/search?q="
    query = title.replace(' ', '+')
    return f"{base_url}{query}"


def get_google_scholar_url(title):
    base_url = "https://www.google.com.ng/search?tbo=p&tbm=bks&q="
    query = title.replace(' ', '+')
    return f"{base_url}{query}"


def get_internet_archive_url(title):
    base_url = "https://archive.org/search?query="
    query = title.replace(' ', '+')
    return f"{base_url}{query}"

# The read on links

def get_scribd_url(title):
    base_url = "https://www.scribd.com/search?query="
    query = title.replace(' ', '+')
    return f"{base_url}{query}"

def get_kobo_books_url(title):
    base_url = "https://www.kobo.com/ww/en/search?query="
    query = title.replace(' ', '+')
    return f"{base_url}{query}"

def get_audible_url(title):
    base_url = "https://www.audible.com/search?keywords="
    query = title.replace(' ', '+')
    return f"{base_url}{query}"


def get_barnes_nobles_url(title):
    base_url = "https://www.barnesandnoble.com/s/"
    query = title.replace(' ', '+')
    return f"{base_url}{query}"



def fetch_most_rated_books():
    """Fetch the most rated books with additional purchase URLs."""
    api_url = 'https://www.googleapis.com/books/v1/volumes?q=most+popular+books&orderBy=relevance&maxResults=40'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        books = []
        for item in data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            title = volume_info.get('title', 'No Title')
            book = {
                'title': title,
                'author': ', '.join(volume_info.get('authors', [])),
                'description': volume_info.get('description', 'No Description'),
                'isbn': next((identifier['identifier'] for identifier in volume_info.get('industryIdentifiers', []) if
                              identifier['type'] == 'ISBN_13'), ''),
                'published_date': volume_info.get('publishedDate', 'No Date'),
                'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', 'https://via.placeholder.com/150')
            }
            books.append(book)
        return books
    return []


def index(request):
    """The home page for the learning log."""
    return render(request, 'ecommerce_app/index.html')

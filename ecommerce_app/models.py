from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    thumbnail = models.URLField()
    amazon_url = models.URLField()  # Amazon affiliate link
    average_rating = models.FloatField(null=True, blank=True)
    rating_count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='categories')

    def __str__(self):
        return self.name


class UserBookInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_interested = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True, blank=True)
    review = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class LearningLogEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    progress_percentage = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class AffiliateLink(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    url = models.URLField()
    source = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} link for {self.book.title}"

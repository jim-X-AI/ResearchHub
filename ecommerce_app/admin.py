from django.contrib import admin
from .models import Book, Category, UserBookInteraction, LearningLogEntry, AffiliateLink

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'published_date', 'average_rating')
    search_fields = ('title', 'author', 'isbn')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class UserBookInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'is_interested', 'rating')
    search_fields = ('user__username', 'book__title')

class LearningLogEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'title', 'progress_percentage', 'date_added')
    search_fields = ('user__username', 'book__title', 'title')

class AffiliateLinkAdmin(admin.ModelAdmin):
    list_display = ('book', 'source', 'created_at')
    search_fields = ('book__title', 'source')

# Register your models and custom admin classes
admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserBookInteraction, UserBookInteractionAdmin)
admin.site.register(LearningLogEntry, LearningLogEntryAdmin)
admin.site.register(AffiliateLink, AffiliateLinkAdmin)

from django.contrib import admin
from AzureViewerService.models import Book, Publisher, Author

class AuthorAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'email')
	search_fields = ('first_name', 'last_name')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date')
    list_filter = ('publication_date', 'authors', 'publisher')
    search_fields = ('title', 'authors', 'publisher')
    date_hierarchy = 'publication_date'
    ordering = ('publication_date','title','publisher')
    filter_horizontal = ('authors',)
    raw_id_fields = ('publisher',)

class PublisherAdmin(admin.ModelAdmin):
	search_fields = ('name',)

admin.site.register(Book, BookAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Author, AuthorAdmin)
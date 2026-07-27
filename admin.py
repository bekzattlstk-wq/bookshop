# Django admin панелиндеги китеп, жанр, категория жана товар интерфейсине жооп берет.
from django.contrib import admin
from django.utils.html import format_html
from .models import Book, Genre, Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'price',
        'is_available',
    )

    list_filter = (
        'category',
        'is_available',
    )

    search_fields = (
        'name',
        'description',
    )

    prepopulated_fields = {
        'slug': ('name',)
    }

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'created_at',
        'is_published',
        'preview_content',
        'image_preview'
    )

    list_display_links = ('id', 'title')

    list_editable = ('is_published',)

    list_filter = (
        'is_published',
        'created_at',
        'updated_at'
    )

    search_fields = (
        'title',
        'content',
        'slug'
    )

    ordering = ('-created_at',)

    prepopulated_fields = {'slug': ('title',)}

    filter_horizontal = ('genres',)

    readonly_fields = (
        'created_at',
        'updated_at',
        'image_preview_inline'
    )

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'content', 'image')
        }),
        ('Изображение (превью)', {
            'fields': ('image_preview_inline',),
            'classes': ('collapse',)  # Скрыто по умолчанию
        }),
        ('Публикация', {
            'fields': ('is_published',),
        }),
        ('Системные даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Скрыто по умолчанию
        }),
    )

    actions = ['make_published', 'make_unpublished']

    list_per_page = 50

    save_on_top = True

    def preview_content(self, obj):
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content

    preview_content.short_description = 'Превью текста'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 10px;" />',
                obj.image.url
            )
        return '-'

    image_preview.short_description = 'Фото'

    def image_preview_inline(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px;" />',
                obj.image.url
            )
        return 'Изображение не загружено'

    image_preview_inline.short_description = 'Превью изображения'

    def make_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f'Опубликовано {count} книг.')

    make_published.short_description = '✅ Опубликовать выбранные книги'

    def make_unpublished(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f'Снято с публикации {count} книг.')

    make_unpublished.short_description = '📌 Снять с публикации'

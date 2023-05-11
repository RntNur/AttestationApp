from django.contrib import admin

from .models import Tours, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')


class ToursAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'date_create', 'date_update', 'exist', 'category')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description', 'category__name')  # Поиск по категории
    list_editable = ('exist', )  # Изменяемое поле
    list_filter = ('exist', 'category')  # Фильтры полей
    readonly_fields = ('date_create', 'date_update')  # Только для чтения поля

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tours, ToursAdmin)
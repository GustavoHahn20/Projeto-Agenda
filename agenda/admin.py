from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'id', 'firstName', 'lastName', 'phone', 'category', 'owner'

    ordering = 'id',

    list_filter = 'createdDate', 'firstName',

    search_fields = 'id', 'firstName', 'lastName', 'email',

    list_per_page = 10

    list_max_show_all = 1000

    list_display_links = 'id', 'phone', 

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'
    ordering = 'id',
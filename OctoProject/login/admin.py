from django.contrib import admin
from models import customers,streams,aspects
from django.contrib.auth.models import User


# Register your models here.
class Streamlist(admin.ModelAdmin):
    list_display = ('name', 'aspect','bitrate','publish','streamtype','password','readonly')
    list_filter = ('aspect','streamtype','publish')
    search_fields = ['name']
admin.site.register(streams,Streamlist)

class Customerlist(admin.ModelAdmin):
    list_display = ('name', 'cpcode')
    search_fields = ['name']
    list_filter = ('cpcode',)
admin.site.register(customers,Customerlist)

class Aspectslist(admin.ModelAdmin):
    list_display = ('name', 'filter')
    search_fields = ['name']
    list_filter = ('filter',)
admin.site.register(aspects,Aspectslist)

admin.site.disable_action('delete_selected')
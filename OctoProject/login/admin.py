from django.contrib import admin
from models import customers,streams
from django.contrib.auth.models import User


# Register your models here.
class Streamlist(admin.ModelAdmin):
    list_display = ('name', 'aspect','bitrate','publish','streamtype','password')
    list_filter = ('aspect','streamtype','publish')
    search_fields = ['name']
admin.site.register(streams,Streamlist)

class Customerlist(admin.ModelAdmin):
    list_display = ('name', 'cpcode')
    search_fields = ['name']
    list_filter = ('cpcode',)
admin.site.register(customers,Customerlist)

admin.site.disable_action('delete_selected')



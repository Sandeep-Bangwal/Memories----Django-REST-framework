from django.contrib import admin
from .models import Posts

@admin.register(Posts)
class poll(admin.ModelAdmin):
    list_display =  (
        'user',
        'title',
        'description',
        'video',
        'images',

    )

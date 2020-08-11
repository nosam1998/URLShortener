from django.contrib import admin

from main.models import ShortenedUrl, ClickedBy


class ShortenedUrlAdmin(admin.ModelAdmin):
    list_display = ('slug', 'original_url', 'timestamp', 'used_count')


class ClickedByAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'timestamp', 'short_url')


admin.site.register(ShortenedUrl, ShortenedUrlAdmin)
admin.site.register(ClickedBy, ClickedByAdmin)

from django.db import models


class ShortenedUrl(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    original_url = models.CharField(max_length=2000)
    used_count = models.IntegerField(default=0)

    def __str__(self):
        return self.slug


class ClickedBy(models.Model):
    ip_address = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    short_url = models.ForeignKey(
        ShortenedUrl, on_delete=models.CASCADE, related_name="short_url_fk")

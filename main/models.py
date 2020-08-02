from django.db import models


class ShortenedUrl(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    original_url = models.CharField(max_length=2000)

    def __str__(self):
        return "{}".format(slug)

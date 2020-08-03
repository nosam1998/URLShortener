import random
import re
import string
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views import View

from .forms import CreateShortUrlForm
from .models import ShortenedUrl


class Home(View):
    template_name = "home.html"
    form_class = CreateShortUrlForm

    def get(self, request):
        return render(request, self.template_name, context={"final_url": "", "no_url": True})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            slug = form.cleaned_data.get('slug')
            # TODO Validate that the slug doesn't contain any bad characters

            new_slug = slugify(slug)
            slug_search = ShortenedUrl.objects.filter(slug=new_slug)

            if slug_search.count() != 0:
                db_row_count = ShortenedUrl.objects.all().count() + 1
                new_slug = "{s}-{num}".format(s=new_slug, num=db_row_count)

            new_short_url = ShortenedUrl()
            new_short_url.slug = new_slug
            new_short_url.original_url = form.cleaned_data.get('original_url')
            new_short_url.save()

            return render(request, self.template_name, context={"final_url": new_slug, "no_url": False})
        else:
            return redirect("/")


class RedirectUser(View):
    def get(self, request, short_url):
        obj = ShortenedUrl.objects.filter(slug=short_url)

        if obj.count() == 1:
            return redirect(obj[0].original_url)
        elif obj.count() == 0:
            return redirect("/")
        else:
            return redirect("/")

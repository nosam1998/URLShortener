import random
import re
import string
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views import View

from .forms import CreateShortUrlForm
from .models import ShortenedUrl, ClickedBy


def visitor_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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
            print(slug)
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
            my_obj = obj[0]
            click = ClickedBy()
            click.ip_address = visitor_ip_address(request)
            click.short_url = my_obj
            click.save()
            print(my_obj.used_count)
            my_obj.used_count = int(my_obj.used_count) + 1
            my_obj.save()
            print(my_obj.used_count)
            return redirect(my_obj.original_url)
        elif obj.count() == 0:
            return redirect("/")
        else:
            return redirect("/")

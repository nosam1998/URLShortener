from django.shortcuts import render, redirect
from django.views import View

from .forms import CreateShortUrlForm
from .models import ShortenedUrl


class Home(View):
    template_name = "home.html"
    form_class = CreateShortUrlForm

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            slug = form.cleaned_data.get('slug')
            # TODO Validate that the slug doesn't contain any bad characters

            if ShortenedUrl.objects.filter(slug=slug).count() == 0:
                new_short_url = ShortenedUrl()
                new_short_url.slug = slug
                new_short_url.original_url = form.cleaned_data.get('original_url')

                new_short_url.save()
        return redirect("/")


class RedirectUser(View):
    def get(self, request, short_url):
        obj = ShortenedUrl.objects.filter(slug=short_url)

        if obj.count() == 1:
            return redirect(obj[0].original_url)
        elif obj.count() == 0:
            return redirect("/")
        else:
            return redirect("Something Went wrong")

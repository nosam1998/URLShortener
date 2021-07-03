from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from main.models import ClickedBy


class UrlData(View):
    def parse_clicked_by_obj_arr(self, obj_arr):
        data = {
            "destination_url": obj_arr[0].short_url.original_url,
            "url_slug": obj_arr[0].short_url.slug,
            "used_count": obj_arr[0].short_url.used_count,
            "click_data": []
        }

        for obj in obj_arr:
            data["click_data"].append({
                "ip_address": obj.ip_address,
                "timestamp": obj.timestamp
            })

        return data

    def get(self, request, slug):
        url_data = ClickedBy.objects.filter(short_url__slug=slug)

        if url_data.count() == 0:
            return JsonResponse({"error": "No Data For that Url Slug!"})

        data = self.parse_clicked_by_obj_arr(url_data)

        return JsonResponse(data)

    def post(self, request):
        pass

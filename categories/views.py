####
### django restframework 를 사용하지않고 만든 API
### objects 를 불러올 때마다 새로 serializer 를 해줘야하기 때문에 비효율적
from django.http import JsonResponse
from django.core import serializers
from .models import Category


def categories(request):
    all_categories = Category.objects.all()
    return JsonResponse(
        {
            "ok": True,
            "categories": serializers.serialize("json", all_categories),
        }
    )

### categoy 모델의 value를 serializers.py 에 일일이 추가해줘야 하기 때문에 사용하지 않을 것임

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer


@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
        # serializer 는 django python 객체를 JSON으로 번역
    elif request.method == "POST":
        print(request.data)
        # request 는 URL에서 호출된 모든 함수에게 주어짐 또 request 객체에는 api view
        # 이기 때문에 data 라는게 있음. data는 유저가 보내는 데이터
        return Response({"created": True})


@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

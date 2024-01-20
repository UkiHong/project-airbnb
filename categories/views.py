### categoy 모델의 value를 serializers.py 에 일일이 추가해줘야 하기 때문에 사용하지 않을 것임

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Category
from .serializers import CategorySerializer


@api_view(["GET", "POST"])
def categories(request):
    # 전체 category 를 보는 restframework page. http://127.0.0.1:8000/categories
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
        # serializer 는 django python 객체를 JSON으로 번역
        # serializer 는 반대로 유저가 보낸 데이터를 django 객체로도 바꿔줌
    elif request.method == "POST":
        # print(request.data)
        # # request 는 URL에서 호출된 모든 함수에게 주어짐 또 request 객체에는 api view
        # # 이기 때문에 data 라는게 있음. data는 유저가 보내는 데이터
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            # serializer.save() 를 한다고해서 자동으로 create & save가 되는것이 아님
            # save() 가 serializer 에서 def create를 호출하기 떄문에
            # 직접 def create 를 만들어줘야 함
            return Response(
                CategorySerializer(new_category).data,
            )
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    # 하나의 category 를 보는 restframework page. http://127.0.0.1:8000/categories/1
    try:
        category = Category.objects.get(pk=pk)
    except:
        raise NotFound
    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
            # partial 을 사용하면 데이터 전체가 아닌 일부만 바꿀 수 있음.
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            # 여기선 def create 가 아닌 def update 를 실행
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)
    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)

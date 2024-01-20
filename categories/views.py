### categoy 모델의 value를 serializers.py 에 일일이 추가해줘야 하기 때문에 사용하지 않을 것임

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer


# 이 코드로 아래의 모든 코드 대체함 ㄷㄷ
# 하지만 더 다양하고 customizable 한 api를 만드려면 APIView를 통해 직접 커스텀하길 추천
# 간단히 get, put, delete 같은건 이렇게 짜는게 효율적
class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


# class Categories(APIView):
#     def get(self, request):
#         all_categories = Category.objects.all()
#         serializer = CategorySerializer(all_categories, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             new_category = serializer.save()
#             return Response(
#                 CategorySerializer(new_category).data,
#             )
#         else:
#             return Response(serializer.errors)


# class CategoryDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Category.objects.get(pk=pk)
#         except:
#             raise NotFound

#     # API의 상세한 부분을 작업할 때 항상 get_object로 객체를 가져온 뒤
#     # get_object 를 통해 category를 불러오고 get, put, delete method와 공유

#     def get(self, request, pk):
#         serializer = CategorySerializer(self.get_object(pk))
#         return Response(serializer.data)

#     def put(self, request, pk):
#         serializer = CategorySerializer(
#             self.get_object(pk),
#             data=request.data,
#             partial=True,
#             # partial 을 사용하면 데이터 전체가 아닌 일부만 바꿀 수 있음.
#         )
#         if serializer.is_valid():
#             updated_category = serializer.save()
#             # 여기선 def create 가 아닌 def update 를 실행
#             return Response(CategorySerializer(updated_category).data)
#         else:
#             return Response(serializer.errors)

#     def delete(self, request, pk):
#         self.get_object(pk).delete()
#         return Response(status=HTTP_204_NO_CONTENT)


# ^^^위 class Categories(APIView) 와 동일
# @api_view(["GET", "POST"])
# def categories(request):
#     # 전체 category 를 보는 restframework page. http://127.0.0.1:8000/categories
#     if request.method == "GET":
#         all_categories = Category.objects.all()
#         serializer = CategorySerializer(all_categories, many=True)
#         return Response(serializer.data)
#         # serializer 는 django python 객체를 JSON으로 번역
#         # serializer 는 반대로 유저가 보낸 데이터를 django 객체로도 바꿔줌
#     elif request.method == "POST":
#         # print(request.data)
#         # # request 는 URL에서 호출된 모든 함수에게 주어짐 또 request 객체에는 api view
#         # # 이기 때문에 data 라는게 있음. data는 유저가 보내는 데이터
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             new_category = serializer.save()
#             # serializer.save() 를 한다고해서 자동으로 create & save가 되는것이 아님
#             # save() 가 serializer 에서 def create를 호출하기 떄문에
#             # 직접 def create 를 만들어줘야 함
#             return Response(
#                 CategorySerializer(new_category).data,
#             )
#         else:
#             return Response(serializer.errors)


# ^^^위 class CategoryDetail(APIView) 와 동일
# @api_view(["GET", "PUT", "DELETE"])
# def category(request, pk):
#     # 하나의 category 를 보는 restframework page. http://127.0.0.1:8000/categories/1
#     try:
#         category = Category.objects.get(pk=pk)
#     except:
#         raise NotFound
#     if request.method == "GET":
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = CategorySerializer(
#             category,
#             data=request.data,
#             partial=True,
#             # partial 을 사용하면 데이터 전체가 아닌 일부만 바꿀 수 있음.
#         )
#         if serializer.is_valid():
#             updated_category = serializer.save()
#             # 여기선 def create 가 아닌 def update 를 실행
#             return Response(CategorySerializer(updated_category).data)
#         else:
#             return Response(serializer.errors)
#     elif request.method == "DELETE":
#         category.delete()
#         return Response(status=HTTP_204_NO_CONTENT)

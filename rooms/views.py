from rest_framework.views import APIView
from django.db import transaction
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer


class Amenities(APIView):
    def get(self, request):
        # 모든 View function은 자동으로 request를 받음
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def post(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
            # partial 을 사용하면 데이터 전체가 아닌 일부만 바꿀 수 있음.
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            # 여기선 def create 가 아닌 def update 를 실행
            return Response(AmenitySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_room = Room.objects.all()
        serializer = RoomListSerializer(all_room, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("Category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found.")
                try:
                    with transaction.atomic():
                        # 모든 코드가 성공하거나 아무 것도 성공하지 않기를 원할 때,트랜잭션을 사용한다.
                        # [장고 공식 문서]
                        # https://docs.djangoproject.com/en/4.1/topics/db/transactions/
                        room = serializer.save(
                            owner=request.user,
                            # owner는 이 url을 호출한 유저라는 뜻
                            category=category,
                        )
                        # 유저 데이터로만 serializer를 생성해서 save 메서드를 호출하면,
                        # 자동으로 serializer의 create 메서드 호출됨
                        # .save() 괄호 안에 추가하는 무엇이든 create 메서드의 validated_data에 추가됨
                        # 즉, request.data에 괄호 안의 데이터를 포함한 모든 validated_data를 가지고 방을 생성해 줌
                        # owner와 category는 Foreign Key임에 반해, amenities는 ManyToMany 필드임에 유의
                        # 따라서, 방이 생성된 다음 room.amenities.add()를 사용하여 amenity를 추가해줘야 함
                        amenities = request.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("Category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found.")
            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    amenities = request.data.get("amenities")
                    if amenities:
                        room.amenities.clear()
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        # 위에 elif를 사용하지 않는 이유는, elif를 사용할 경우 위의 if절이 해당되면
        # elif절은 작동하지 않을 것이기 때문. 위 아래 모두 작동하기 원하기 때문에 if를 사용
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)

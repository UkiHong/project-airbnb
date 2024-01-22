from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer()
    amenities = AmenitySerializer(many=True)
    # amenities 여러 value가 있기 때문에(array 혹은 list 이기 때문에) many=True 를 써줘야함
    category = CategorySerializer()
    # category는 array가 아닌 단 한개의 value 이므로 many=True 안씀

    class Meta:
        model = Room
        fields = "__all__"


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )
        # depth = 1
        # django에서 "id"값을 serialize해서 rest framework에서 관련 값을 보여줌

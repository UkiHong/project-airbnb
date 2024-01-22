from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    # create과 update method 도 자동으로 구현됨
    class Meta:
        model = Category
        fields = (
            "name",
            "kind",
        )


# 위 ModelSerializer로 아래 코드 전부를 위 코드로 구현가능.
# class CategorySerializer(serializers.Serializer):
#     pk = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(
#         required=True,
#         max_length=50,
#     )
#     kind = serializers.ChoiceField(
#         choices=Category.CategoryKindChoices.choices,
#     )
#     created_at = serializers.DateTimeField(read_only=True)
#     # read_only=True 를 사용함으로써 유저가 해당 데이터를 보내지않아도(not required) POST할 수 있음

#     def create(self, validated_data):
#         # views.py 에서 serializer.save() 시 꼭 필요한 method
#         # bcs save()가 serializer에서 def create method를 자동으로 찾기 때문에
#         return Category.objects.create(**validated_data)
#         # **validated_data 가
#         # {'name': 'Category from DRF', 'kind': 'rooms'}를
#         # name= 'Category from DRF'
#         # kind= 'room' 형태로 간편히 바꿔서 keyword arguments로 넣어줌

#     def update(self, instance, validated_data):
#         # 여기서 instance는 category를 의미
#         instance.name = validated_data.get("name", instance.name)
#         # get에서 새로운 "name"값이 없으면 현재 기본값인 instance.name 을 그대로 불러옴
#         instance.kind = validated_data.get("kind", instance.kind)
#         instance.save()
#         return instance

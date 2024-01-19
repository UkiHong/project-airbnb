from django.db import models
from common.models import CommonModel


# Create your models here.
class Room(CommonModel):
    # Room model definition

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_room", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(
        max_length=180,
        default="",
    )
    country = models.CharField(
        max_length=50,
        default="United Kingdom",
    )
    city = models.CharField(
        max_length=80,
        default="London",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
        # related_name="rooms" 는 User model 이 더이상 room_set을 가지지 않고
        # "rooms"를 가지게 됨
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
        # 위 owner에 쓴 related_name 과 마찬가지로 amenity 가 어떤 room에 할당되었는지
        # 알려면 "rooms" 로 찾아낼 수 있음
    )

    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        # SET_NULL 은 category 가 삭제되더라도 room은 삭제되지 않게 함
        # 삭제되었을 때 그냥 category 필드에 null 을 입력함
        related_name="rooms",
    )

    def __str__(room) -> str:
        return room.name

    def total_amenities(room):
        return room.amenities.count()

    def rating(room):
        count = room.reviews.count()
        # reverse accessor 를 사용해서 reviews model의 room 에 접근해서 데이터를 불러옴
        if count == 0:
            return "No Reviews"
        else:
            total_rating = 0
            for review in room.reviews.all().values("rating"):
                # .values("rating")을 한 이유는 reviews 전체 데이터가 아닌
                # "rating" 만 불러와서 데이터부하를 줄이고 속도를 빠르게 함
                total_rating += review["rating"]
                # review.ratings -> review["rating"] 왜냐하면 .values로 불러온
                # 값들은 [{'review': 5}] 이런식으로 리스트로 표현되기 때문
            return round(total_rating / count, 2)

    # #def rating(self):
    #     average_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
    #     if average_rating is None:
    #         return "No Reviews"
    #     else:
    #         return round(average_rating, 2)
    # 위 def rating은 리뷰 데이터가 많다면 모든 리뷰데이터에 대해 루프를 돌기 때문에
    # aggregate와 Avg를 사용해 한 번의 쿼리로 리뷰의 평균값을 계산함. 최적화된 버전


class Amenity(CommonModel):
    # Amenity Definition
    name = models.CharField(max_length=150)
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        # blank=True 는 django form 에서 공백을 의미
        # null=True 는 database 에서 null 일 수 있다는 의미
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"

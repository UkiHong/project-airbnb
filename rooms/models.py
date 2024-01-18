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
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
    )

    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        # SET_NULL 은 category 가 삭제되더라도 room은 삭제되지 않게 함
        # 삭제되었을 때 그냥 category 필드에 null 을 입력함
    )

    def __str__(self) -> str:
        return self.name


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

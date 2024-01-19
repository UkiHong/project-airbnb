from django.db import models
from common.models import CommonModel


# Create your models here.
class Experience(CommonModel):
    # Experience model definition
    country = models.CharField(
        max_length=50,
        default="United Kingdom",
    )
    city = models.CharField(
        max_length=80,
        default="London",
    )
    name = models.CharField(
        max_length=250,
    )
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField(
        "experiences.Perk",
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        # SET_NULL 은 category 가 삭제되더라도 experience 는 삭제되지 않게 함
        # 삭제되었을 때 그냥 category 필드에 null 을 입력함
        related_name="experiences",
    )

    def __str__(self) -> str:
        return self.name


class Perk(CommonModel):
    # What is included on our experience
    name = models.CharField(max_length=100)
    details = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    explanation = models.TextField(
        blank=True,
        default="",
    )

    def __str__(self) -> str:
        return self.name

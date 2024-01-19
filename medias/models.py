from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    file = models.ImageField()
    description = models.CharField(
        max_length=140,
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self) -> str:
        return "Photo File"


class Video(CommonModel):
    file = models.FileField()
    experience = models.OneToOneField(
        # OneToOneField 는 ForeignKey 와 거의 같지만 video 가
        # 단 한개의 Experience만 받도록 설정함
        # ex. 유저의 unique한 결제 정보를 하나만 만들어야 할 때 사용 가능
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="videos",
    )

    def __str__(self) -> str:
        return "Video File"

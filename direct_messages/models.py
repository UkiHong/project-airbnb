from django.db import models
from common.models import CommonModel


class ChattingRoom(CommonModel):
    # Room (Chat room) model definition

    users = models.ManyToManyField(
        "users.User",
        related_name="chatting_rooms",
    )

    def __str__(self) -> str:
        return "Chatting Room."


class Message(CommonModel):
    # Message Model definition
    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="messages",
    )
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
        # direct_messages app의 (chat)Room 이 삭제되면 messages 도 삭제
        related_name="messages",
    )

    def __str__(self) -> str:
        return f"{self.user} says: {self.text}"

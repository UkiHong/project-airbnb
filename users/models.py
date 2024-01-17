from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # House Model 의 유저와 다르게 커스텀 유저를 만듦.

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")
        # (value in database, label in admin page)

    class LanguageChoices(models.TextChoices):
        EN = ("en", "English")
        KR = ("kr", "Korean")

    class CurrencyChoices(models.TextChoices):
        GBP = ("gbp", "Pound")
        USD = ("usd", "Dollar")
        WON = ("won", "won")

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    avatar = models.ImageField(blank=True)
    name = models.CharField(
        max_length=150,
        default="",
    )
    is_host = models.BooleanField(
        default=False,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
    )

from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Review


# 8.3 Custom Filters
class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            reviews


# Filter by ratings
class ScoreFilter(admin.SimpleListFilter):
    title = "Filter by Score"
    parameter_name = "score"

    def lookups(self, request, model_admin):
        return [
            ("bad", "Bad"),
            ("good", "Good"),
        ]

    def queryset(self, request, reviews):
        score = self.value()
        if score:
            return reviews.filter(rating__lt=3)
        else:
            return reviews.filter(rating__gte=3)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        WordFilter,
        ScoreFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
        # ForeignKey 를 가진 value에 대해 필터링 옵션을 만들 수 있음
    )

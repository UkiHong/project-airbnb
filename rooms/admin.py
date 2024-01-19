from django.contrib import admin
from .models import Room, Amenity


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    # 3개의 parameter 가 꼭 필요함
    # 1st = 이 액션을 호출한 model_admin, 2st = 이 액션을 호출한 유저 정보를 가진 request 객체
    # 3rd = queryset (여기서 rooms 로 이름 붙임)
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices,)
    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
    )

    list_filter = (
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )

    def total_amenities(self, room):
        return room.amenities.count()

    search_fields = (
        "name",
        "^price",
        "owner__username",
        # __username 은 owner 의 username 을 검색
        # ^ 는 start with --- 로 시작하는 값만 검색
        # = 는 동일한 값만 검색, 아무것도 안 붙이면 contains 로 검색
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

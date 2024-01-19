from django.urls import path
from . import views


urlpatterns = [
    path("", views.see_all_rooms),
    path("<int:room_id>", views.see_one_room),
    # "<int:room_id>"는 rooms/<??> 의 parameter 를 의미, int 는 숫자를 의미
]

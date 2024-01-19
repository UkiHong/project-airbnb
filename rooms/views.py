# view 는 유저가 특정 url에 접근했을 때 작동하게되는 함수
from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


# template rendering
def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(
        request,
        "all_rooms.html",
        # request할 템플릿을 두번째 argument에 입력
        {
            "rooms": rooms,
            "title": "Hello! this title comes from django",
        },
        # {}안의 데이터는 "all_rooms.html" 로 보낼 데이터를 의미
    )


def see_one_room(request, room_id):
    return HttpResponse(f"see room with id: {room_id}")

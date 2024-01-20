from django.urls import path
from . import views

urlpatterns = [
    path("", views.Categories.as_view()),
    path("<int:pk>", views.CategoryDetail.as_view()),
]
# as_view()의 역할은 요청이 GET이면 'get' 메서드를 실행시키는 거고
# POST이면 'post' 메서드를 실행시키는 것이다.

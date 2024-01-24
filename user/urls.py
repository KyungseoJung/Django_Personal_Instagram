# //@7 urls.py도 앱별로 나눠서 정리 - user 파일
from django.urls import path
from .views import Join, Login

urlpatterns = [
    path('join', Join.as_view()),    # //@7 url 이름을 join으로 -> user/views.py에 있는 Join이라는 함수가 실행된다.
    path('login', Login.as_view())
]


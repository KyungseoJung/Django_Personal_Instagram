# //@7 urls.py도 앱별로 나눠서 정리 - user 파일
from django.urls import path
from .views import Join, Login, LogOut, UploadProfile  # //#9 LogOut 임포트

urlpatterns = [
    path('join', Join.as_view()),    # //@7 url 이름을 join으로 -> user/views.py에 있는 Join이라는 함수가 실행된다.
    path('login', Login.as_view()),
    path('logout', LogOut.as_view()),    # //#9 logout주소로 가면-> 로그아웃 함수로 넘어가도록
    path('profile/upload',UploadProfile().as_view())  # //#9 프로필 이미지 업로드 화면 -> UploadProfile 함수로 연결
]


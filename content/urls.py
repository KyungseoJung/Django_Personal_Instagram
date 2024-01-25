# //@7 urls.py도 앱별로 나눠서 정리
from django.urls import path
from .views import UploadFeed, Profile, Main


urlpatterns = [
    path('upload', UploadFeed.as_view()),
    # //@7 upload라 적으면, 자동으로 경로 이름으로 접근할 때, 앞에 앱 이름이 붙어

    path('profile', Profile.as_view()),
    # //#9 user/profile 링크로 접속하면, 자동으로 .views 파일의 Profile 클래스 실행되도록

    path('main', Main.as_view())
    # //#9 content/main 링크로 접속하면, 자동으로 .views 파일의 Main 클래스 실행되도록
]


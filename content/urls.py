# //@7 urls.py도 앱별로 나눠서 정리
from django.urls import path
from .views import UploadFeed

urlpatterns = [
    path('upload', UploadFeed.as_view())
    # //@7 upload라 적으면, 자동으로 경로 이름으로 접근할 때, 앞에 앱 이름이 붙어
]


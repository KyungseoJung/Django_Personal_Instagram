"""
URL configuration for Kyungstagram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include   #//@7 include 임포트! - 다른 앱에 있는 urls.py 가져오기 위함
from .views import Sub          #@ 현재 위치(현재 위치 (Kyungstgram 파일) 내 views 파일에서 Sub라는 클래스를 가져오도록
from content.views import Main, UploadFeed  #@ content 하위 views라는 파일에서 Main이라는 클래스를 가져오도록. 내가 이걸 쓰겠다
                                            #//@6 UploadFeed 클래스도 추가
from .settings import MEDIA_URL, MEDIA_ROOT #//@6 빨간 줄 없애기 위한 import 코드
from django.conf.urls.static import static  #//@6 코드 추가


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('main/',Sub.as_view())     # http://localhost:8000/main/ 사이트에 들어갈 때마다 Kyungstagram\views 파일의 Sub 클래스가 실행됨
    path('main/', Main.as_view()),    # http://localhost:8000/main/ 사이트에 들어갈 때마다 content\views 파일의 Main 클래스가 실행됨
    # path('content/upload', UploadFeed.as_view())   #//@6 content/upload/를 실행하면, UploadFeed 클래스를 as_view() 한다. //@7 아래 코드로 대체
    path('content/', include('content.urls')),   # //@7 위 코드를 이 코드로 대체 - 다른 앱에서 가져오도록

    path('user/', include('user.urls'))  # //@7 다른 앱에서 가져오도록

]

# Kyungstagram - media에 접근해서 파일을 조회할 수 있게 해주는 코드
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
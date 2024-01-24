from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed
    #@ 나랑 같은 폴더 내에 있는 models라는 파일(models.py)에서 Feed라는 클래스를 가져오겠다.
    #@ 항상 출처를 분명히 해줘야 함
from user.models import User    #//@8
import os   # //@6
from Kyungstagram.settings import MEDIA_ROOT    #//@6

# Create your views here.

class Main(APIView):
    def get(self, request):
        # print("겟으로 호출")
        feed_list = Feed.objects.all().order_by('-id')  # select * from content_feed; 와 같은 역할을 하는 것-> 그걸 feed_list라는 곳에 받겠다
                                                        #@ 업데이트 역순으로 가져오기
        # for feed in feed_list:  #@ 피드 하나씩 출력
        #     print(feed)       #@ 피드만 보고 싶다.
        #     print(feed.content) #@ 피드의 글 내용까지 보고 싶다.
        #
        # print(feed_list)  #@ 그냥 통째로 출력한 예

        #//@8 세션 정보 가져와서 확인하기
        # print('로그인한 사용자: ', request.session['email']) # //#9 있으면 에러 발생하므로
        # email = request.session['email']
        # //#9 위 코드: email이 없으면 에러가 나게 되어있으므로, 아래 코드로 변경
        email = request.session.get('email', None)  # //#9 없으면 에러가 나는 게 아니라, None으로 받도록 변경

        if email is None:
            return render(request, "user/login.html")   # //@8 유저 이메일 없으면, 로그인부터 하도록 로그인 화면 띄워
        user = User.objects.filter(email=email).first()     # //@8 고유 데이터인 이메일을 이용해서 로그인 한 사용자의 정보를 가져오기

        if user is None:
            return render(request, "user/login.html")   # //@8 사용자 정보 없으면, 로그인부터 하도록 로그인 화면 띄워


        return render(request, "kyungstagram/main.html", context=dict(feeds=feed_list, user=user)) #@ 키 이름 = 위에서 정의한 데이터 값

        #@ dictionary : key-value가 짝꿍으로 있는 상태
        #@ -> 이제 main.html에서 feeds를 변수로 그냥 사용 가능!

# //@6 main.html :  jQuery 코드 ajax에서 데이터를 서버로 올림
# -> 이제 content\views.py : 서버에서 데이터 받아주기
class UploadFeed(APIView):
    def post(self, request):

        # //@6 일단 파일 불러와
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)     #//@6 Ctrl + 클릭을 통해 들어가보면: '개인의 프로젝트 경로/media/uuid로 생성된 이름 문자'

        # //@6 파일을 저장해 - 파일의 청크를 하나씩 가져와서 - 파일을 만드는 역할
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        file = request.data.get('file')


        image = uuid_name   #//@6 클라이언트가 만든 request.data.get('image') 은 이제 필요 없어진 것.
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')

        Feed.objects.create(image=image, content=content, user_id=user_id, profile_image=profile_image, like_count=0)

        # response: Alt + Enter 눌러서 import하기
        return Response(status=200)


# //#9 프로필 화면으로 넘어가는 Profile 클래스 추가
class Profile(APIView):
    def get(self, request):

        # //#9 아래처럼 email(사용자 고유 정보)를 불러와야 profile.html에서 {{ user.nickname }} 같은 정보에 접근 가능
        email = request.session.get('email', None)  # //#9 없으면 에러가 나는 게 아니라, None으로 받도록 변경

        if email is None:
            return render(request, "user/login.html")   # //@8 유저 이메일 없으면, 로그인부터 하도록 로그인 화면 띄워
        user = User.objects.filter(email=email).first()     # //@8 고유 데이터인 이메일을 이용해서 로그인 한 사용자의 정보를 가져오기

        if user is None:
            return render(request, "user/login.html")   # //@8 사용자 정보 없으면, 로그인부터 하도록 로그인 화면 띄워

        # //#9 여기까지 위 email(사용자 공유 정보)를 불러와줘서 아래처럼 context=dict(user=user)를 통해 사용자 정보를 넘기는 것

        return render(request, 'content/profile.html', context=dict(user=user))
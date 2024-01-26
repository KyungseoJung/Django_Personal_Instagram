from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed, Like, Reply, Bookmark  # //#10 Like, Reply, Bookmark 임포트
# @ 나랑 같은 폴더 내에 있는 models라는 파일(models.py)에서 Feed라는 클래스를 가져오겠다.
# @ 항상 출처를 분명히 해줘야 함
from user.models import User  # //@8
import os  # //@6
from Kyungstagram.settings import MEDIA_ROOT  # //@6


# Create your views here.

class Main(APIView):
    def get(self, request):

        # print("겟으로 호출")
        feed_object_list = Feed.objects.all().order_by(
            '-id')  # select * from content_feed; 와 같은 역할을 하는 것-> 그걸 feed_list라는 곳에 받겠다
        # @ 업데이트 역순으로 가져오기
        # //#10 email을 이용해서만 데이터를 가져오다보니까, 피드를 올릴 때 필요한 데이터(사용자 닉네임, 프로피 이미지)가 없는 상태임
        # So, 위의 feed_list를 feed_object_list라는 이름으로 변경하고, 아래에서 직접 feed_list를 만들어서 데이터를 넣어줄거야.

        # //#10 중요!!: user 테이블은 프로필 변경할 때마다 실시간으로 갱신되기 때문에, 실시간으로 프로필 수정해도 아래 코드들이 적용이 가능하다!
        feed_list = []

        for feed in feed_object_list:

            # //#10-1 아래 user로부터 profile_image, nickname 가져오는 부분 자꾸 에러 발생 - 원인: user를 찾지 못해서
            # //#10-1 내 해결책: feed로부터 user를 찾는 게 아니라, 로그인 한 email로부터 user를 찾아서 email 가져오도록 코드 변경함
            # //#10-1 변경된 코드 부분: User.objects.filter(email=feed.email).first() -> User.objects.filter(email=email).first()
            email = request.session.get('email', None)
            if email is None:
                return render(request, "user/login.html")
            user = User.objects.filter(email=email).first()
            # //#10-1 사용자 고유 데이터(email)를 이용해서 user에 접근 -> 아래 feed_list.append할 때 nickname, profile_image 가져올 수 있도록

            # //#10-2 답글 데이터에 접근하기
            # (#10-1에서 했던 것과 같은 방식)
            # reply_object_list에는 사용자의 닉네임, 프사는 없고, 이메일만 있어 - 그래서 reply_list에 하나씩 append 해주는 것
            reply_object_list = Reply.objects.filter(feed_id = feed.id)
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email = reply.email).first()
                reply_list.append(dict(reply_content = reply.reply_content,
                                       nickname = user.nickname))

            feed_list.append(dict(image=feed.image,
                                  content=feed.content,
                                  like_count=feed.like_count,
                                  profile_image=user.profile_image, # //#10-1
                                  nickname=user.nickname,           # //#10-1

                                  reply_list = reply_list           # //#10-2 답글 데이터도 보이도록
                                  ))

        # for feed in feed_list:  #@ 피드 하나씩 출력
        #     print(feed)       #@ 피드만 보고 싶다.
        #     print(feed.content) #@ 피드의 글 내용까지 보고 싶다.
        #
        # print(feed_list)  #@ 그냥 통째로 출력한 예

        # //@8 세션 정보 가져와서 확인하기
        # print('로그인한 사용자: ', request.session['email']) # //#9 있으면 에러 발생하므로
        # email = request.session['email']
        # //#9 위 코드: email이 없으면 에러가 나게 되어있으므로, 아래 코드로 변경
        email = request.session.get('email', None)  # //#9 없으면 에러가 나는 게 아니라, None으로 받도록 변경

        if email is None:
            return render(request, "user/login.html")  # //@8 유저 이메일 없으면, 로그인부터 하도록 로그인 화면 띄워
        user = User.objects.filter(email=email).first()  # //@8 고유 데이터인 이메일을 이용해서 로그인 한 사용자의 정보를 가져오기

        if user is None:
            return render(request, "user/login.html")  # //@8 사용자 정보 없으면, 로그인부터 하도록 로그인 화면 띄워

        return render(request, "kyungstagram/main.html",
                      context=dict(feeds=feed_list, user=user))  # @ 키 이름 = 위에서 정의한 데이터 값

        # @ dictionary : key-value가 짝꿍으로 있는 상태
        # @ -> 이제 main.html에서 feeds를 변수로 그냥 사용 가능!


# //@6 main.html :  jQuery 코드 ajax에서 데이터를 서버로 올림
# -> 이제 content\views.py : 서버에서 데이터 받아주기
class UploadFeed(APIView):
    def post(self, request):
        # //@6 일단 파일 불러와
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)  # //@6 Ctrl + 클릭을 통해 들어가보면: '개인의 프로젝트 경로/media/uuid로 생성된 이름 문자'

        # //@6 파일을 저장해 - 파일의 청크를 하나씩 가져와서 - 파일을 만드는 역할
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        file = request.data.get('file')

        image = uuid_name  # //@6 클라이언트가 만든 request.data.get('image') 은 이제 필요 없어진 것.
        content = request.data.get('content')

        # user_id = request.data.get('user_id')
        # profile_image = request.data.get('profile_image')
        # //#10 이제 user_id, profile_image 데이터 대신 email 데이터만 받으면 됨.
        # //#10 사실 email을 받을 필요도 없음. 세션에 저장된 정보를 바로 가져오면 됨.(로그인을 하면서 email을 입력받았을테니까)
        email = request.session.get('email', None)

        Feed.objects.create(image=image, content=content, email=email, like_count=0)

        # response: Alt + Enter 눌러서 import하기
        return Response(status=200)


# //#9 프로필 화면으로 넘어가는 Profile 클래스 추가
class Profile(APIView):
    def get(self, request):

        # //#9 아래처럼 email(사용자 고유 정보)를 불러와야 profile.html에서 {{ user.nickname }} 같은 정보에 접근 가능
        email = request.session.get('email', None)  # //#9 없으면 에러가 나는 게 아니라, None으로 받도록 변경

        if email is None:
            return render(request, "user/login.html")  # //@8 유저 이메일 없으면, 로그인부터 하도록 로그인 화면 띄워
        user = User.objects.filter(email=email).first()  # //@8 고유 데이터인 이메일을 이용해서 로그인 한 사용자의 정보를 가져오기

        if user is None:
            return render(request, "user/login.html")  # //@8 사용자 정보 없으면, 로그인부터 하도록 로그인 화면 띄워

        # //#9 여기까지 위 email(사용자 공유 정보)를 불러와줘서 아래처럼 context=dict(user=user)를 통해 사용자 정보를 넘기는 것

        return render(request, 'content/profile.html', context=dict(user=user))


# //#10-2 댓글 달기 클래스
class UploadReply(APIView):
    def post(self, request):
        feed_id = request.session.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)


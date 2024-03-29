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
        # //#11-1 email 데이터 끌어올려서 위치 변경 - 처음부터 email 데이터를 확인하도록
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


        # print("겟으로 호출")
        feed_object_list = Feed.objects.all().order_by(
            '-id')  # select * from content_feed; 와 같은 역할을 하는 것-> 그걸 feed_list라는 곳에 받겠다
        # @ 업데이트 역순으로 가져오기
        # //#10 email을 이용해서만 데이터를 가져오다보니까, 피드를 올릴 때 필요한 데이터(사용자 닉네임, 프로피 이미지)가 없는 상태임
        # So, 위의 feed_list를 feed_object_list라는 이름으로 변경하고, 아래에서 직접 feed_list를 만들어서 데이터를 넣어줄거야.

        # //#10 중요!!: user 테이블은 프로필 변경할 때마다 실시간으로 갱신되기 때문에, 실시간으로 프로필 수정해도 아래 코드들이 적용이 가능하다!
        feed_list = []

        for feed in feed_object_list:

            # # //#10-1 아래 user로부터 profile_image, nickname 가져오는 부분 자꾸 에러 발생 - 원인: user를 찾지 못해서
            # # //#10-1 내 해결책: feed로부터 user를 찾는 게 아니라, 로그인 한 email로부터 user를 찾아서 email 가져오도록 코드 변경함
            # # //#10-1 변경된 코드 부분: User.objects.filter(email=feed.email).first() -> User.objects.filter(email=email).first()
            # email = request.session.get('email', None)
            # if email is None:
            #     return render(request, "user/login.html")
            # user = User.objects.filter(email=email).first()
            # # //#10-1 사용자 고유 데이터(email)를 이용해서 user에 접근 -> 아래 feed_list.append할 때 nickname, profile_image 가져올 수 있도록

            # //#10-2 답글 데이터에 접근하기
            # (#10-1에서 했던 것과 같은 방식)
            # reply_object_list에는 사용자의 닉네임, 프사는 없고, 이메일만 있어 - 그래서 reply_list에 하나씩 append 해주는 것
            reply_object_list = Reply.objects.filter(feed_id = feed.id)
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email = reply.email).first()
                reply_list.append(dict(reply_content = reply.reply_content,
                                       nickname = user.nickname))

            like_count = Like.objects.filter(feed_id = feed.id, is_like=True).count()
            # //#11-1 models.py의 Like 클래스에 접근해서 like_count를 가져오더라 - 아래 like_count에 넣어주기

            is_liked = Like.objects.filter(feed_id = feed.id, email=email, is_like = True).exists()
            # //#11-1 내가 특정 게시물에 좋아요 눌렀는지 확인 - 눌렀으면 true

            is_marked = Bookmark.objects.filter(feed_id = feed.id, email = email, is_marked = True).exists()
            # //#11-5 내가 특정 게시물에 북마크 눌렀는지 확인 - 눌렀으면 true

            feed_list.append(dict(id = feed.id,                     # //#10-3 피드 아이디를 main.htlm에서 받을 수 있도록
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=like_count,            # //#11-1 데이터 변경 feed.like_count,
                                  profile_image=user.profile_image, # //#10-1
                                  nickname=user.nickname,           # //#10-1

                                  reply_list = reply_list,          # //#10-2 답글 데이터도 보이도록
                                  is_liked =is_liked,               # //#11-1
                                  is_marked = is_marked             # //#11-5 북마크 정보도 보내도록
                                  ))

        # for feed in feed_list:  #@ 피드 하나씩 출력
        #     print(feed)       #@ 피드만 보고 싶다.
        #     print(feed.content) #@ 피드의 글 내용까지 보고 싶다.
        #
        # print(feed_list)  #@ 그냥 통째로 출력한 예


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

        Feed.objects.create(image=image, content=content, email=email)   # , like_count=0)  # //#11 전에 like_count는 이제 안 받기로 했으므로 여기서도 제거

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

        # //#11-6 여기부터: 3가지 피드 리스트를 가져와: 내 피드 리스트, 내가 좋아요 한 피드 리스트, 내가 북마크 한 피드 리스트
        feed_list = Feed.objects.filter(email=email).all()

        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))    # 내가 '좋아요' 한 컨텐츠의 리스트
        # print(like_list) # value_list와 flat=True로 주면, 오브젝트가 쿼리 리스트로 나옴. 거기에 list로 1번 더 감싸면 순수 리스트 형태로만 나옴
        like_feed_list = Feed.objects.filter(id__in=like_list)   # 내가 '좋아요'한 피드의 리스트. 그 리스트의 아이디만 가져온 것
            # @중요!! id__in 의미: Feed에 있는 id 주에 like_list를 포함하고 있는 애만 걸러내는 역할
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)
        
        # //#11-6 여기까지

        return render(request, 'content/profile.html', context=dict(feed_list = feed_list,
                                                                                 like_feed_list = like_feed_list,
                                                                                 bookmark_feed_list = bookmark_feed_list,
                                                                                 user=user))


# //#10-2 댓글 달기 클래스
class UploadReply(APIView):
    def post(self, request):

        # feed_id = request.session.get('feed_id', None)
        feed_id = request.data.get('feed_id', None)
        # //#10-3 session.get으로 받는 게 아님. 왜?: main.html에서 upload_reply ajax 함수에서 데이터를 받아서 답글을 다는 것이므로

        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)

# //#11-1 좋아요 기능 클래스
class ToggleLike(APIView):
    def post(self, request):

        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)

        # //#11-4 빈 하트일 때, 좋아요를 누른 거면 is_like = True(좋아요=True)인 거니까 DB에 좋아요 넣기
        if favorite_text == 'favorite':   # //#11-1 boolean 변수가 아니라 string으로 받을 것이기 때문에
            is_like = True
        else:
            is_like = False

        email = request.session.get('email', None)

        # //#11-4 이미 좋아요가 있는지 확인 - 좋아요는 한 사람당 하나씩만 달 수 있기 때문
        # //#11-4 이미 특정 유저가 같은 게시물에 좋아요를 2번 이상 눌렀다면, 가장 최신 데이터로 저장을 한다.
        like = Like.objects.filter(feed_id=feed_id, email=email).first()
        if like:
            like.is_like = is_like  # 위의 if문에서 업데이트 한 is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)  # //#11-4 없으면 좋아요 추가

        return Response(status=200)


# //#11-5 북마크 기능 클래스
class ToggleBookmark(APIView):
    def post(self, request):

        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)

        if bookmark_text == 'bookmark':   # //#11-1 boolean 변수가 아니라 string으로 받을 것이기 때문에
            is_marked = True
        else:
            is_marked = False

        email = request.session.get('email', None)

        # //#11-4 이미 좋아요가 있는지 확인 - 좋아요는 한 사람당 하나씩만 달 수 있기 때문
        # //#11-4 이미 특정 유저가 같은 게시물에 좋아요를 2번 이상 눌렀다면, 가장 최신 데이터로 저장을 한다.
        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()
        if bookmark:
            bookmark.is_marked = is_marked  # 위의 if문에서 업데이트 한 is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)  # //#11-4 없으면 좋아요 추가

        return Response(status=200)


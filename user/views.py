import os   # //#9
from uuid import uuid4  # //#9

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from Kyungstagram.settings import MEDIA_ROOT     # //#9
from .models import User     # //@8
from django.contrib.auth.hashers import make_password   #//@8 make_password 함수를 사용하기 위한 임포트


# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")
    # //@7 Join이라는 함수를 호출하면, get으로 호출했을 때, template 파일에 있는 join.html을 실행한다

    def post(self, request):
        # TODO 회원가입 //@8
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(email=email,
                            nickname=nickname,
                            name=name,
                            password=make_password(password),   # //@8 비밀번호는 암호화해서 넣기 위해 make_password라는 함수 사용
                            profile_image="default_profile.jpg") # //@8 회원가입 할 때는 프로필 이미지가 없기 때문에, 디폴트 넣음

        return Response(status=200)

class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")
    # //@7 Login이라는 함수를 호출하면, get으로 호출했을 때, template 파일에 있는 join.html을 실행한다

    def post(self, request):
        # TODO 로그인 //@8
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()    #//@8 고유의 아이디를 확인.
        # 어차피 고유값이기 때문에 중복되지는 않아. 그러므로 처음부터 first()로 지정
        #  하나만 리턴하면 아래 코드처럼 리스트 객체를 사용하지 않고, user 객체를 사용할 수 있다는 편리함이 있음
        # user_list = User.objects.filter(email=email) #<- 불편해! user_list[0] 또는 for user in user_list: 처럼 꼬아서 써야 돼

        if user is None:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))
        # //@8 TIP: 해커한테 어떠한 정보도 주지 않기 위해서 "회원정보가 없다"는 내용이 아닌, 회원정보를 잘못 입력했을 때에 나오는 경고창과 똑같은 메시지를 던지기

        if user.check_password(password):
            # TODO 로그인을 했다. 세션 or 쿠키에 넣기?
            request.session['email'] = email    #//@8 세션 정보에 이메일 정보 넣기
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

        # pass


# //#9 로그아웃 함수 설정
class LogOut(APIView):
    def get(self, request):
        # //#9 세션 지운 후, 로그인 화면 넘어가기
        request.session.flush()
        return render(request, "user/login.html")


# //#9 프로필 사진 업로드 함수 설정
class UploadProfile(APIView):
    def post(self, request):

        # 일단 파일과 email을 불러와
        file = request.FILES['file']
        email = request.data.get('email')

        # //#9 파일의 이름 - 랜덤으로 고유값을 만든 다음, MEDIA_ROOT에 저장
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        # 파일을 저장해 - 파일의 청크를 하나씩 가져와서 - 파일을 만드는 역할
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name   # //#9 프로필 이미지 이름으로 저장해

        user = User.objects.filter(email=email).first()
        # //#9 email 주소를 이용해서 사용자 찾기

        user.profile_image = profile_image
        user.save()
        # //#9 사용자를 찾았으니까, 그 사용자의 프로필 이미지에 <- 우리가 저장한 프로필 이미지를 넣어. 그리고 저장

        # response: Alt + Enter 눌러서 import하기
        return Response(status=200)


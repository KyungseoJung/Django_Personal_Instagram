from django.contrib.auth.base_user import AbstractBaseUser  # //@7 커스텀 유저 모델
from django.db import models


# Create your models here.
class User(AbstractBaseUser):  # //@7 커스텀 유저 모델
    """
        유저 프로필 사진
        유저 닉네임      -> 화면에 표기되는 이름
        유저 이름       -> 실제 사용자 이름
        유저 이메일주소   -> 회원가입 할 때 사용하는 아이디
        유저 비밀번호     -> 디폴트 쓰자
    """

    profile_image = models.TextField()  # 프로필 이미지
    nickname = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'nickname'
    # //@7 유저 선택하면, 유저의 이름을 'nickname'으로 설정하겠다.
    # - 단 고유해야 하므로(unique) 위에서 unique=True로 설정해준 것뿐

    class Meta:
        db_table = "User"

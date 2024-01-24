from django.db import models


# Create your models here.
class Feed(models.Model):  # @ models라는 곳에서 Model을 상속 받아서 쓰겠다.
    # 5개의 필드를 만들어
    content = models.TextField()  # 글 내용
    image = models.TextField()  # 피드 이미지
    profile_image = models.TextField()  # 프로필 이미지
    user_id = models.TextField()  # 글쓴이
    like_count = models.IntegerField()  # 좋아요 수

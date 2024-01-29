from django.db import models


# Create your models here.
class Feed(models.Model):  # @ models라는 곳에서 Model을 상속 받아서 쓰겠다.
    # 5개의 필드를 만들어
    content = models.TextField()  # 글 내용
    image = models.TextField()  # 피드 이미지

    # profile_image = models.TextField()  # 프로필 이미지
    # user_id = models.TextField()  # 글쓴이
    # //#10 위 데이터 필요 없어 - 아래 email 데이터로 대체해서 해야 돼.
    email = models.EmailField(default='')  # 글쓴이//#10 이메일 데이터(사용자의 고유 데이터)

    # like_count = models.IntegerField()  # 좋아요 수
    # //#11-1 필요 없다고 판단. 주석 처리 -> views.py에서 like_count를 어떻게 계산하는지 봐봐 - Like 클래스에서 가져오더라


class Like(models.Model):  # //#10 좋아요 클래스 따로 생성
    feed_id = models.IntegerField(default=0)  # 내가 어떤 글을 좋아요 눌렀는지
    email = models.EmailField(default='')  # 내가 어떤 사용자의 좋아요 눌렀는지
    is_like = models.BooleanField(default=True)
    # 내가 좋아요를 2번 누르면 취소가 됨
    # 방법 2가지 - (1) 좋아요 취소할 때마다 데이터 삭제, (2) 좋아요 취소할 때마다 변경되는 변수 설정
    # - 그때마다 데이터를 아예 삭제하지 않는 건 번거로우니, Bool형 변수를 주자


class Reply(models.Model):  # //#10 답글 클래스 따로 생성
    feed_id = models.IntegerField(default=0)  # 내가 어떤 글에 댓글을 달았는지
    email = models.EmailField(default='')  # 내가 어떤 사용자에게 댓글을 달았는지
    reply_content = models.TextField()


class Bookmark(models.Model):  # //#10 북마크 클래스 따로 생성
    feed_id = models.IntegerField(default=0)  # 내가 어떤 글에 북마크를 달았는지
    email = models.EmailField(default='')  # 내가 어떤 사용자에게 북마크를 달았는지
    is_marked = models.BooleanField(default = True)

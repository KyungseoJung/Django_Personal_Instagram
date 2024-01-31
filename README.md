<h4 align='center'> 인스타그램 클론 코딩 with Django </h4>

<h1 align='center'> 웹 개발 프로젝트 </h1>

<h3 align='center'> 프로젝트 소개 </h3>

이 리포지토리는 YouTube에서 찾은 포괄적인 튜토리얼을 따라 구현한 인스타그램 클론의 소스 코드를 포함하고 있습니다. 
사용 언어: JavaScript, HTML, CSS
웹 어플리케이션 프레임워크: Django

## 📍튜토리얼 상세 정보

- **튜토리얼 제목:** [Django를 활용한 인스타그램 클론 코딩](https://www.youtube.com/watch?v=M8UPyeF5DfM&t=4561s)
- **언어:** JavaScript, HTML, CSS
- **웹 어플리케이션 프레임워크:** Django

## 📍노션과 문서

프로젝트와 관련된 자세한 노트 및 문서는 다음 Notion 문서에서 찾을 수 있습니다:

- **Notion 문서:** [Django Python 클론 코딩](https://kyungseojung.notion.site/Django-Python-c0ed6525a6a84a6594f4aa34a9a6c06e?pvs=4)

## 📍프론트엔드 ↔ 백엔드 흐름

[참고 사이트](https://velog.io/@mynghn/django%EC%99%80-%EB%B0%B1%EC%97%94%EB%93%9C%EC%97%90-%EB%8C%80%ED%95%9C-%EC%9D%B4%ED%95%B4-%EC%9E%85%EB%AC%B8%EC%9E%90%EC%9D%98-%EC%9E%85%EC%9E%A5%EC%97%90%EC%84%9C)

### 프론트엔드 프로젝트 흐름:

```plaintext
html → css → javascript → ajax/jQuery → 백엔드
```

### 백엔드 프로젝트 흐름:
```plaintext
manage.py → settings.py // → urls.py → views.py (→template 내 .html 파일)
```

- manage.py
- settings.py
- urls.py: URL 경로를 관리하며, 사용자 관련 URL에 대한 user\urls.py를 포함
- views.py: GET 및 POST 요청을 처리하며, 요청 유형에 따라 특정 작업을 수행


## 📍학습 여정

#### 주요 학습 내용

1. Django 환경 설정 및 기본 웹페이지 생성.
2. Instagram 피드 화면의 왼쪽 및 오른쪽 섹션 구현.
3. 모델-뷰-템플릿 구조 이해 및 데이터베이스에서 피드 게시물 검색.

##### 프론트엔드 개발

- 이미지 업로드 등의 기능을 포함한 반응형 웹사이트 개발.
- CSS 스타일링에 Bootstrap 사용 및 JavaScript와 jQuery 관계 이해.

##### 백엔드 개발

- 등록, 로그인 및 프로필 관리와 같은 사용자 관련 기능 구현.
- Django 모델을 사용하여 피드, 댓글, 좋아요 및 북마크 구현.

# 보여지게 하기 위해서 이 파일이 필요
from django.shortcuts import render
from rest_framework.views import APIView

# ALT + Enter하면 자동으로 위 코드(import)를 만들어줌

class Sub(APIView):
    def get(self, request):
        print("겟으로 호출")
        return render(request, "kyungstagram/main.html")

    def post(self, request):
        print("포스트로 호출")
        return render(request, "kyungstagram/main.html")

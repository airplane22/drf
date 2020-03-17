import jwt
from django.conf import settings
# from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

from users.models import User

# drf 문서 custom authentication 참조

# AWS에서 header로 authentication : WSGIPassAuthorization on 해줘야함!
# elastic beanstalk

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # print(request.META)  # request meta 정보 열람
        # print(request.META.get("HTTP_AUTHORIZATION"))  # headers 에 key값 authorization으로 준 값 받아옴 , value 는 X-JWT jwt코드
        try:
            token = request.META.get("HTTP_AUTHORIZATION")
            if token is None:
                return None
            xjwt, jwt_token = token.split(" ")  # x-jwt 는 안써도 돼(convention)
            decoded = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])  # SECRET_KEY 의 의미?
            # print(decoded)  # id 출력됨 token decode해서 id 얻는것
            pk = decoded.get("pk")
            print(pk)
            user = User.objects.get(pk=pk)
            return (user, None)  # 딱히 이유ㅡㄴ 모름
        except (ValueError, jwt.exceptions.DecodeError):  # question : ValueError
            return None
        # except jwt.exceptions.DecodeError:  # jwt token 변경됨. 그냥 none 반환해도 ok
        #     raise exceptions.AuthenticationFailed(detail="JWT Format Invalid")


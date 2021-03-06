import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rooms.models import Room
from rooms.serializers import RoomSerializer
from users.models import User
from users.permissions import IsSelf
from users.serializers import UserSerializer


class UsersViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":  # 관리자만 user 목록
            permission_classes = [IsAdminUser]
        elif self.action == "create" or self.action=="retrieve" or self.action=="favs":  # 누구나 생성 가능, 누구나 1명 조회 가능
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]  # update, delete 는 본인만 가능하게 + toggle_favs 포함!!!
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["POST"])  # detail=False : /users/ detail=True: /users/pk/
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            # jwt : json web token - 개인정보 포함 X, pk 같은 식별자만. 토큰은 누구나 해독 가능 / 우리 토큰이 변경되었는지 변경되지 않았는지를 확인하는 것.
            # user 가 토큰 보내면 다시 확인해서 authentication. not from cookies, from token!
            encoded_jwt = jwt.encode({'pk': user.pk}, settings.SECRET_KEY, algorithm='HS256')  # never import settings.py / import from django.settings
            return Response(data={"token":encoded_jwt, "id":user.pk})  # data= 언제 쓰고 언제 안쓰는가? / id 보내줘서 내가 누군지 알게 하기
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True)  # permission_classes=
    def favs(self, request, pk):  # detail=True일때 pk 받아줘야 함!
        # user = request.user
        user = self.get_object()  # 로그아웃 상태에서도 favs 볼 수 있게
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)

    # different function, but same url(pk/favs/)
    @favs.mapping.put  #extending favs with mapping (delete, post, put...)
    def toggle_favs(self, request, pk):
        pk = request.data.get("pk", None)
        user = self.get_object()  # 어차피 permission 때문에 본인!
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)

                # favs 에 있으면 삭제, 없으면 추가
                # 두가지 방법: url 인자로 받기 / data 로 받기

                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)




# class UsersView(APIView):
#
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)  # create 이니가 instance 안받고, partial=True 쓰면 안돼 모두 필요 / password 는 입력받고 create 에서 바꿔줄예정
#         if serializer.is_valid():
#             new_user = serializer.save()
#             return Response(UserSerializer(new_user).data)  #question .data 안써도돼? nico는 안쓴거같던데
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# MeView / user_detail 분리 이유 - MeView 는 url 에서 pk 안받는다. pk 안받아도 pk 값 확인할 수 있는 url 필요.

# /me 안쓰고 그냥 id 보내주기
# class MeView(APIView):
#
#     permission_classes = [IsAuthenticated]  # fbv 에서는 @permission_classes([IsAuthenticated]) question header jwttoken으로 authenticated 되면 안되지 않나? 공개키인데
#
#     def get(self, request):
#         # permission_classes = [IsAuthenticated] 로 아래 주석 대체 가능
#         # if request.user.is_authenticated:  # is_authenticated : 로그인 여부 확인 user model attribute. @property 임!
#         #     return Response(ReadUserSerializer(request.user).data)
#         # else:
#         #     return Response(status=status.HTTP_401_UNAUTHORIZED)
#         return Response(UserSerializer(request.user).data)
#
#     def put(self, request):
#         serializer = UserSerializer(request.user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response()
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "POST"])
@permission_classes(["IsAuthenticated"])
def toggle_fav(request):
    room = request.data.get("room")
    print(room)


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     user = request.user
    #     serializer = RoomSerializer(user.favs.all(), many=True).data
    #     return Response(serializer)

    def put(self, request):
        pk = request.data.get("pk", None)
        user = request.user
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)

                # favs 에 있으면 삭제, 없으면 추가
                # 두가지 방법: url 인자로 받기 / data 로 받기

                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])  # 크기 작을때는 fbv 활용
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(UserSerializer(user).data)
        # question data vs validated_data
        # data vs validated_data
        # data : is a dict and you can see it only after is_valid()
        # validated_data : is an OrderedDict and you can see it only after is_valid() && is_valid() == True
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# UserView action으로 추가
# @api_view(["POST"])
# def login(request):
#     username = request.data.get("username")
#     password = request.data.get("password")
#     if not username or not password:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         # jwt : json web token - 개인정보 포함 X, pk 같은 식별자만. 토큰은 누구나 해독 가능 / 우리 토큰이 변경되었는지 변경되지 않았는지를 확인하는 것.
#         # user 가 토큰 보내면 다시 확인해서 authentication. not from cookies, from token!
#         encoded_jwt = jwt.encode({'pk': user.pk}, settings.SECRET_KEY, algorithm='HS256')  # never import settings.py / import from django.settings
#         return Response(data={"token":encoded_jwt})  # data= 언제 쓰고 언제 안쓰는가?
#     else:
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

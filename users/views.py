from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rooms.models import Room
from rooms.serializers import RoomSerializer
from users.models import User
from users.serializers import ReadUserSerializer, WriteUserSerializer


# MeView / user_detail 분리 이유 - MeView 는 url 에서 pk 안받는다. pk 안받아도 pk 값 확인할 수 있는 url 필요.


class MeView(APIView):

    permission_classes = [IsAuthenticated]  # fbv 에서는 @permission_classes([IsAuthenticated])

    def get(self, request):
        # permission_classes = [IsAuthenticated] 로 아래 주석 대체 가능
        # if request.user.is_authenticated:  # is_authenticated : 로그인 여부 확인 user model attribute. @property 임!
        #     return Response(ReadUserSerializer(request.user).data)
        # else:
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(ReadUserSerializer(request.user).data)

    def put(self, request):
        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])  # 크기 작을때는 fbv 활용
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(ReadUserSerializer(user).data)
        # question data vs validated_data
        # data vs validated_data
        # data : is a dict and you can see it only after is_valid()
        # validated_data : is an OrderedDict and you can see it only after is_valid() && is_valid() == True
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST"])
@permission_classes(["IsAuthenticated"])
def toggle_fav(request):
    room = request.data.get("room")
    print(room)


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)

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


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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


@ api_view(["GET"])  # 크기 작을때는 fbv 활용
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


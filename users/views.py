from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import ReadUserSerializer

# MeView / user_detail 분리 이유 - MeView 는 url 에서 pk 안받는다. pk 안받아도 pk 값 확인할 수 있는 url 필요.


class MeView(APIView):

    def get(self, request):
        if request.user.is_authenticated:  # question is_authenticated ? is_authenticated() ?
            return Response(ReadUserSerializer(request.user).data)

    def put(self, request):
        pass


@ api_view(["GET"])  # 크기 작을때는 fbv 활용
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(ReadUserSerializer(user).data)  # question data vs validated_data
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


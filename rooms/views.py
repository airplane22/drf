# from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
# generics : page 등의 정보를 가짐
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer


# from rest_framework.decorators import api_view

# @api_view(["GET"])  # ["GET", "POST"] 등 가능
# def list_rooms(request):
#     rooms = Room.objects.all()  # QuerySet
#     serialized_rooms = RoomSerializer(rooms, many=True)  # Room QuerySet 을 RoomSerializer 로 json 으로 serialize
#     return Response(data=serialized_rooms.data)

# class ListRoomsView(APIView):
#
#     def get(self, request):
#         rooms = Room.objects.all()
#         serializer = RoomSerializer(rooms, many=True)
#         return Response(serializer.data)


# 커스터마이징 필요없을 때
# class ListRoomsView(ListAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

@api_view(["GET", "POST"])  # django 가 아니라 rest_framework 에서 view 처리
def rooms_view(request):
    if request.method == "GET":
        rooms = Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)  # django response 와 rest_framework Response 는 다름!
    elif request.method == "POST":
        # print(request.data)  # dict type, not json 출력됨
        serializer = WriteRoomSerializer(data=request.data)
        print(serializer)
        print(serializer.is_valid())  # 전송된 data 가 serializer valid 한지 확인 ( 모든 필드 충족시키는지)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer
    # lookup_url_kwarg = "pkkk"  -url 인자 이름 변경






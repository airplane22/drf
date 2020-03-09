# from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
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
        rooms = Room.objects.all()[:5]
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)  # django response 와 rest_framework Response 는 다름!
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # print(request.data)  # dict type, not json 출력됨
        serializer = WriteRoomSerializer(data=request.data)  # instance 안받고 data 만 인수로 받아서 serializer initiate
        print(serializer)
        print(dir(serializer))  # serializer 어트리뷰트(대부분 메서드) 확인 --create, update, save 중요
        print(serializer.is_valid())  # 전송된 data 가 serializer valid 한지 확인 ( 모든 필드 충족시키는지)
        if serializer.is_valid():
            # serializer.create()  # never call create, update method directly
            room = serializer.save(user=request.user)  # save() 가 create / update 구분해서 call 해준다 + validated_data 자동 전송됨
            room_serializer = ReadRoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomsView(APIView):

    def get(self, request):
        rooms = Room.objects.all()[:5]
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)  # django response 와 rest_framework Response 는 다름!

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # print(request.data)  # dict type, not json 출력됨
        serializer = WriteRoomSerializer(data=request.data)
        print(serializer)
        print(dir(serializer))  # serializer 어트리뷰트(대부분 메서드) 확인 --create, update, save 중요
        print(serializer.is_valid())  # 전송된 data 가 serializer valid 한지 확인 ( 모든 필드 충족시키는지)
        if serializer.is_valid():
            # serializer.create()  # never call create, update method directly
            room = serializer.save(user=request.user)  # save method 가 create / update call 해준다 + validated_data 자동 전송됨
            room_serializer = ReadRoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SeeRoomView(RetrieveAPIView):  # RetrieveAPIView : read-only. get 요청만 받는다.
#     queryset = Room.objects.all()  # RetrieveAPIView 기본구조
#     serializer_class = ReadRoomSerializer
#     # lookup_url_kwarg = "pkkk"  -url 인자 이름 변경


class RoomView(APIView):

    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):  # url 에서 pk 인자 받아서 해당 room 을 get
        # get, put, delete 메서드 모두에서 활용되는 room object get 부분은 메서드(get_room) 활용하여 단축
        # try:
        #     room = Room.objects.get(pk=pk)
        #     serializer = ReadRoomSerializer(room).data
        #     return Response(serializer)
        # except Room.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        room = self.get_room(pk)
        if room is not None:
            serializer = ReadRoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = WriteRoomSerializer(room, data=request.data, partial=True)
            # instance 받았으므로 serializer 가 update 호출. partial=True : partial update 가능하게 해줌(required 다 안보내도 update)
            if serializer.is_valid():
                room = serializer.save()  # option update 호출
                return Response(ReadRoomSerializer(room).data)  # obj - ReadRoomSerializer 다시 호출 Response(obj or qs) 안돼!
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):  # serializer 호출 불필요한듯
        room = self.get_room(pk)
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if room is not None:
            room.delete()  # 장고
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, instance, validated_data):
        print(instance, validated_data)











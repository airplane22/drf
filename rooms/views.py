# from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
# generics : page 등의 정보를 가짐
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer


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


#
# @api_view(["GET", "POST"])  # django 가 아니라 rest_framework 에서 view 처리
# def rooms_view(request):
#     if request.method == "GET":
#         rooms = Room.objects.all()[:5]
#         serializer = RoomSerializer(rooms, many=True).data
#         return Response(serializer)  # django response 와 rest_framework Response 는 다름!
#     elif request.method == "POST":
#         if not request.user.is_authenticated:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         # print(request.data)  # dict type, not json 출력됨
#         serializer = RoomSerializer(data=request.data)  # instance 안받고 data 만 인수로 받아서 serializer initiate
#         print(serializer)
#         print(dir(serializer))  # serializer 어트리뷰트(대부분 메서드) 확인 --create, update, save 중요
#         print(serializer.is_valid())  # 전송된 data 가 serializer valid 한지 확인 ( 모든 필드 충족시키는지)
#         if serializer.is_valid():
#             # serializer.create()  # never call create, update method directly
#             room = serializer.save(user=request.user)  # save() 가 create / update 구분해서 call 해준다 + validated_data 자동 전송됨
#             room_serializer = RoomSerializer(room).data
#             return Response(data=room_serializer, status=status.HTTP_200_OK)
#         else:
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OwnPagination(PageNumberPagination):  # 반복 줄이기 / 공식 문서에서 다른 예시 찾아보기!
    page_size = 20


class RoomsView(APIView):

    def get(self, request):
        # paginator= PageNumberPagination()
        # paginator.page_size = 20
        paginator = OwnPagination()
        rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)  # parsing request - paginator 가 page query argument 찾는다.
        serializer = RoomSerializer(results, many=True)  # .data 안써도돼? - response에서 쓴다.
        # return response(serializer)  # django response 와 rest_framework Response 는 다름!
        return paginator.get_paginated_response(serializer.data)  # page number, previous/next 기능 활용 위해 paginator response 함께 보냄

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # print(request.data)  # dict type, not json 출력됨
        serializer = RoomSerializer(data=request.data)
        print(serializer)
        print(dir(serializer))  # serializer 어트리뷰트(대부분 메서드) 확인 --create, update, save 중요
        print(serializer.is_valid())  # 전송된 data 가 serializer valid 한지 확인 ( 모든 필드 충족시키는지)
        if serializer.is_valid():
            # serializer.create()  # never call create, update method directly
            room = serializer.save(user=request.user)  # save method 가 create / update call 해준다 + validated_data 자동 전송됨
            room_serializer = RoomSerializer(room).data
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
            serializer = RoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = RoomSerializer(room, data=request.data, partial=True)
            # instance 받았으므로 serializer 가 update 호출. partial=True : partial update 가능하게 해줌(required 다 안보내도 update)
            if serializer.is_valid():
                room = serializer.save()  # option update 호출
                return Response(RoomSerializer(room).data)  # obj - ReadRoomSerializer 다시 호출 Response(obj or qs) 안돼!
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


@api_view(["GET"])
def room_search(request):
    max_price = request.GET.get('max_price', None)  # url 에 포함될 argument, None 이 default
    min_price = request.GET.get('min_price', None)
    beds = request.GET.get('beds', None)
    bedrooms = request.GET.get('bedrooms', None)
    bathrooms = request.GET.get('bathrooms', None)
    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    filter_kwargs = {}
    if max_price is not None:
        filter_kwargs["price__lte"] = max_price  # django documentation querysets 참조 __lte(less_then, from django)/__gte/__startswith ...
    if min_price is not None:
        filter_kwargs["price__gte"] = min_price
    if beds is not None:
        filter_kwargs["beds__gte"] = beds
    if bedrooms is not None:
        filter_kwargs["bedrooms__gte"] = bedrooms
    if bathrooms is not None:
        filter_kwargs["bathrooms__gte"] = bathrooms
    if lat is not None and lng is not None:
        filter_kwargs["lat__gte"] = float(lat) - 0.005
        filter_kwargs["lat__lte"] = float(lat) + 0.005
        filter_kwargs["lng__gte"] = float(lng) - 0.005
        filter_kwargs["lng__lte"] = float(lng) + 0.005


    # print(filter_kwargs)  # {key:value} 형식 출력
    # print(*filter_kwargs)  # * : unpack once - key 값만 받음 ex. key, key
    # print(**filter_kwargs)  # ** : unpack twice - key(ex.price__lte)=value(ex.'80'), key=value 으로 parse. print 안됨

    paginator = OwnPagination()
    try:
        rooms = Room.objects.filter(**filter_kwargs)  # unpack 해서 넣어줌
    except ValueError:
        rooms = Room.objects.all()
    results = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)











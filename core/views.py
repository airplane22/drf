from django.core import serializers
from django.http import HttpResponse

from rooms.models import Room


# def list_rooms(request):
#     rooms = Room.objects.all()
#     response = HttpResponse(content=rooms)
#     return response

# import json

# def list_rooms(request):
#     rooms = Room.objects.all()
#     rooms_json = []
#     for room in rooms:
#         rooms_json.append(json.dumps(room))
#     json_rooms = json.dumps(rooms) # json.dumps : Python Object -> 문자열
#     response = HttpResponse(content=json_rooms)
#     return response

# Room objects / QuerySet is not JSON serializable
# json serializer 활용하여 QuerySet -> json object 변환
# +chrome extension JSONView - json 예쁘게 보여줌

def list_rooms(request):
    data = serializers.serialize("json", Room.objects.all())
    response = HttpResponse(content=data)
    return response

# ! but still need validation


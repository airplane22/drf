from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room


# class RoomSerializer(serializers.Serializer):
#     # Room model 에서 원하는 field 만 serialize
#     name = serializers.CharField(max_length=140)
#     price = serializers.IntegerField()
#     bedrooms = serializers.IntegerField()
#     instance_book = serializers.BooleanField()


class ReadRoomSerializer(serializers.ModelSerializer):

    user = UserSerializer()  # 바로 실행한다.

    class Meta:  # 모델 단위의 옵션
        model = Room
        # fields = ("name", "price", "instant_book", "user")
        exclude = ("modified",)


class WriteRoomSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=140)
    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField(help_text="USD per night")
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)

    # 메서드 활용하기 위해 커스텀
    def create(self, validated_data):
        return Room.objects.create(**validated_data)  # method create should return an object!!

    def validate(self, data):  # 전체 field validation
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        if check_in == check_out:
            raise serializers.ValidationError("Not enough time between changes")  # : "non_field_errors"
        else:
            return data  # data 보내야 확인 가능

    def validate_beds(self, beds):  # validate_<fieldname>() validation
        if beds < 5:
            raise serializers.ValidationError("Your house is too small")  # validation error raise : "beds"
        else:
            return beds







# class BigRoomSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Room
#         fields = "__all__"
#         # exclude = (,) 도 가능!

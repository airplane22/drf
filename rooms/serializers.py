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
    def create(self, validated_data):  # Question validated_data 의 의미
        return Room.objects.create(**validated_data)  # method create should return an object!!

    def validate(self, data):  # 전체 field validation
        if not self.instance:  # update 할 때 (instance 받을 때)는 validate 필요 없다
            check_in = data.get('check_in')
            check_out = data.get('check_out')
            if check_in == check_out:
                raise serializers.ValidationError("Not enough time between changes")  # : "non_field_errors"

        return data  # data 보내야 확인 가능

    def validate_beds(self, beds):  # def 내장유효성검사 validate_<fieldname>() +Method may be 'static'뜨는 이유 - 내장이라서 그런듯?
        if beds < 5:
            raise serializers.ValidationError("Your house is too small")  # validation error raise : "beds"
        else:
            return beds

    def update(self, instance, validated_data):  # data 만 받아서 저장할 경우 create / instance 와 data 받아서 저장할 경우 update
        # update 하려면 instance 받아와야 initialize 할 수 있어! 라고 알려주는것
        print(instance, validated_data)  # FIXME update 는 object 받아야함







# class BigRoomSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Room
#         fields = "__all__"
#         # exclude = (,) 도 가능!

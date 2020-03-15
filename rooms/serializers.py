from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    user = RelatedUserSerializer()  # 바로 실행한다.
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ("modified",)
        read_only_fields = ("user", "id", "created", "updated")  # update 못하게 / ModelSerializer 에서만

    def validate(self, data):  # 전체 field validation
        # if not self.instance:  # update 할 때 (instance 받을 때)는 validate 하지 않도록
        #     check_in = data.get('check_in')
        #     check_out = data.get('check_out')
        #     if check_in == check_out:
        #         raise serializers.ValidationError("Not enough time between changes")  # : "non_field_errors"
        # return data  # data 보내야 확인 가능

        # validation 경우의 수 나눠줌: update 할때-있으면 부르고, 없으면 default 불러주고, create 할때 불러서 // validate
        if self.instance:  # update 할때
            check_in = data.get("check_in", self.instance.check_in)  # python get method , 두번째 인자 default 로 받음
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
        if check_in == check_out:
            raise serializers.ValidationError("Not enouth time between changes") # : "non_field_errors"
        return data

    def validate_beds(self, beds):  # def 내장유효성검사 validate_<fieldname>() +Method may be 'static'뜨는 이유 - 내장이라서 그런듯?
        if beds < 5:
            raise serializers.ValidationError("Your house is too small")  # validation error raise : "beds"
        else:
            return beds

    def get_is_fav(self, obj):  # methodfield method / obj: current room
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()  # room 이 fav 에 있는지 확인, bool
        return False
        print(obj)
        return True

    # 메서드 활용하기 위해 커스텀
    def create(self, validated_data):
        return Room.objects.create(**validated_data)  # method create should return an object!!

    def update(self, instance, validated_data):  # data 만 받아서 저장할 경우 create / instance 와 data 받아서 저장할 경우 update
        # update 하려면 instance 받아와야 initialize 할 수 있어! 라고 알려주는것
        instance.name = validated_data.get("name", instance.name)  # 새로 받거나 없으면 none 말고 원래 instance 받아와!
        instance.address = validated_data.get("address", instance.address)
        instance.price = validated_data.get("price", instance.price)
        instance.beds = validated_data.get("beds", instance.beds)
        instance.lat = validated_data.get("lat", instance.lat)
        instance.lng = validated_data.get("lng", instance.lng)
        instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
        instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
        instance.check_in = validated_data.get("check_in", instance.check_in)
        instance.check_out = validated_data.get("check_out", instance.check_out)
        instance.instant_book = validated_data.get("instant_book", instance.instant_book)  # 신기하다! alt 해서 복사한거 줄마다 붙여진다.
        instance.save()
        return instance  # update 는 object 필수

# class RoomSerializer(serializers.Serializer):
#     # Room model 에서 원하는 field 만 serialize
#     name = serializers.CharField(max_length=140)
#     price = serializers.IntegerField()
#     bedrooms = serializers.IntegerField()
#     instance_book = serializers.BooleanField()


# class ReadRoomSerializer(serializers.ModelSerializer):
#
#     user = RelatedUserSerializer()  # 바로 실행한다.
#
#     class Meta:  # 모델 단위의 옵션
#         model = Room
#         # fields = ("name", "price", "instant_book", "user")
#         exclude = ("modified",)
#
#
# class WriteRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         exclude = ("user", "modified", "created")  # room update 중, user update 못하게
#
#     # Serializer 일때
#     # name = serializers.CharField(max_length=140)
#     # address = serializers.CharField(max_length=140)
#     # price = serializers.IntegerField(help_text="USD per night")
#     # beds = serializers.IntegerField(default=1)
#     # lat = serializers.DecimalField(max_digits=10, decimal_places=6)
#     # lng = serializers.DecimalField(max_digits=10, decimal_places=6)
#     # bedrooms = serializers.IntegerField(default=1)
#     # bathrooms = serializers.IntegerField(default=1)
#     # check_in = serializers.TimeField(default="00:00:00")
#     # check_out = serializers.TimeField(default="00:00:00")
#     # instant_book = serializers.BooleanField(default=False)
#
#     # 메서드 활용하기 위해 커스텀
#     def create(self, validated_data):  # Question validated_data 의 의미
#         return Room.objects.create(**validated_data)  # method create should return an object!!
#
#     def validate(self, data):  # 전체 field validation
#         # if not self.instance:  # update 할 때 (instance 받을 때)는 validate 하지 않도록
#         #     check_in = data.get('check_in')
#         #     check_out = data.get('check_out')
#         #     if check_in == check_out:
#         #         raise serializers.ValidationError("Not enough time between changes")  # : "non_field_errors"
#         # return data  # data 보내야 확인 가능
#
#         # Question view 에서 partial=True 줬는데 여기서 해결못하는 문제인가? 쉽지않네... 처음부터 다 맞는 데이터면 그냥 validation 돌려도 되지않을까? 그러면 모델 바꿨을때 심각해지긴하겠네
#         # validation 경우의 수 나눠줌: update 할때-있으면 부르고, 없으면 default 불러주고, create 할때 불러서 // validate
#         if self.instance:  # update 할때
#             check_in = data.get("check_in", self.instance.check_in)  # python get method , 두번째 인자 default 로 받음
#             check_out = data.get("check_out", self.instance.check_out)
#         else:
#             check_in = data.get("check_in")
#             check_out = data.get("check_out")
#         if check_in == check_out:
#             raise serializers.ValidationError("Not enouth time between changes") # : "non_field_errors"
#         return data
#
#     def validate_beds(self, beds):  # def 내장유효성검사 validate_<fieldname>() +Method may be 'static'뜨는 이유 - 내장이라서 그런듯?
#         if beds < 5:
#             raise serializers.ValidationError("Your house is too small")  # validation error raise : "beds"
#         else:
#             return beds
#
#     def update(self, instance, validated_data):  # data 만 받아서 저장할 경우 create / instance 와 data 받아서 저장할 경우 update
#         # update 하려면 instance 받아와야 initialize 할 수 있어! 라고 알려주는것
#         instance.name = validated_data.get("name", instance.name)  # 새로 받거나 없으면 none 말고 원래 instance 받아와!
#         instance.address = validated_data.get("address", instance.address)
#         instance.price = validated_data.get("price", instance.price)
#         instance.beds = validated_data.get("beds", instance.beds)
#         instance.lat = validated_data.get("lat", instance.lat)
#         instance.lng = validated_data.get("lng", instance.lng)
#         instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
#         instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
#         instance.check_in = validated_data.get("check_in", instance.check_in)
#         instance.check_out = validated_data.get("check_out", instance.check_out)
#         instance.instant_book = validated_data.get("instant_book", instance.instant_book)  # 신기하다! alt 해서 복사한거 줄마다 붙여진다.
#         instance.save()
#         return instance  # update 는 object 필수


# class BigRoomSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Room
#         fields = "__all__"
#         # exclude = (,) 도 가능!

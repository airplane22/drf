from rest_framework import serializers

from .models import User


class RelatedUserSerializer(serializers.ModelSerializer):  # room 보여줄때만 필요한 serializer
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost"
        )


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)  # password 보낼 수 있되 볼 수는 없게

    class Meta:
        model = User
        fields = ("id",
                  "username",
                  "first_name",
                  "last_name",
                  "email",
                  "avatar",
                  "superhost",
                  "password",
                  )
        read_only_fields = ("id",
                            "superhost",
                            "avatar"
                            )


    def validate_first_name(self, value):
        print(value)
        return value.upper()

    def create(self, validated_data):  # save()에서 call 되는 create method 인터셉트 (pw 받기 위해서)
        password = validated_data.get("password")  # validated_data.password 와 차이?
        user = super().create(validated_data)  # super() : 부모클래스인 ModelSerializer 의 create method 상속
        user.set_password(password)
        user.save()  #save()꼭 해줘야해!! question save() 언제 안해도돼?
        return user  # object 반환

# class ReadUserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         exclude = (
#             "groups",
#             "user_permissions",
#             "password",
#             "last_login",
#             "is_superuser",
#             "is_staff",
#             "is_active",
#             "favs",
#             "date_joined",
#         )
#
#
# class WriteUserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email"
#         )




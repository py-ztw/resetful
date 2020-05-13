from rest_framework import serializers, exceptions

from apps.models import Employee
from resetful import settings


class EmployeeModelSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()
    # gender = serializers.IntegerField()
    # pic = serializers.ImageField()

    # # 自定序列化字段
    test = serializers.SerializerMethodField()
    def get_test(self, obj):
        return "example"

    # # 直接返回性别
    gender = serializers.SerializerMethodField()
    def get_gender(self, obj):
        print(obj.gender, type(obj))
        return obj.get_gender_display()

    # # 自定义返回图片的全路径
    pic = serializers.SerializerMethodField()
    #
    def get_pic(self, obj):
    #   print(type(obj.pic))
    #   print("http://127.0.0.1:8000" + settings.MEDIA_URL + str(obj.pic))
    #   http://127.0.0.1:8000/media/pic/1.jpeg/
        return "%s%s%s" % ("http://127.0.0.1:8000", settings.MEDIA_URL, str(obj.pic))


class EmployeeDeserializer(serializers.Serializer):

    # 反序列化：前台--->数据
    # 序列化：数据库===>前台

    # 字符长度的规定
    username = serializers.CharField(
        max_length=10,
        min_length=5,
        error_messages={
            "max_length": "长度太长",
            "min_length": "长度太短"
        }
    )

    password = serializers.CharField()

    # phone不是必填参数---required=False
    phone = serializers.CharField(required=False)

    # 验证密码
    re_pwd = serializers.CharField()

    # 局部校验钩子 对某个字段进行校验
    def validate_username(self, value):
        if "1" in value:
            raise exceptions.ValidationError("用户名异常")
        return value

    # 全局的校验钩子，对有校验规则进行验证
    def validate(self, attrs):
        print(attrs, "attr")
        password = attrs.get("password")
        re_pwd = attrs.pop("re_pwd")
        if password != re_pwd:
            raise exceptions.ValidationError("两次密码不一致")
        return attrs

    # 员工新增需要实现create方法
    # z注意：在create方法完成之前  会先调用局部钩子和局钩子函数来完成校验
    def create(self, validated_data):
        print(validated_data)
        return Employee.objects.create(**validated_data)

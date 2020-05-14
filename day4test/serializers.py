from rest_framework import serializers

from apps.models import Book, Press


class PressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ("press_name", "address", "id")


class BookModelSerializer(serializers.ModelSerializer):
    # 为序列化器指定自定义的字段(不推荐)
    press_address = serializers.SerializerMethodField()
    def get_press_address(self, obj):
        print(obj)
        return obj.publish.address

    # 自定义连表查询 查询图书的图书的时候可以查询对应出版社的信息
    # 可以在一个序列化器中嵌套另外一个序列化器完成 连表查询
    # 在连表查询 较多字段时  推荐使用序列化器嵌套
    publish = PressModelSerializer()

    class Meta:
        model = Book
        fields = ("book_name", "price", "pic", "publish_name", "press_address", "author_list", "publish")

        # 直接序列化所有的字段
        # fields = "__all__"

        # 指定字段不进行展示
        # exclude = ("is_delete", "status", "id")

        # 可以指定关系字段展示的深度
        # depth = 1


class BookModelDeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "pic", "authors", "publish")
        extra_kwargs = {
            "book_name": {
                "required": True,
                "min_length": 5,
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "图书名长度不够"
                }
            }
        }
    # 局部钩子
    def validate_book_name(self, value):
        if "D" in value:
            raise serializers.ValidationError("D图书已存在")
        else:
            return value

    def validate(self, attrs):
        publish = attrs.get("publish")
        book_name = attrs.get("book_name")
        book_obj = Book.objects.filter(book_name=book_name, publish=publish)
        if book_obj:
            raise serializers.ValidationError("该出版社已经发布过该图书")

        return attrs


class BookModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Book
        # filed 应该填写哪些字段,应该填写序列化与反序列所有字段的并集
        fields = ("book_name", "price", "pic", "authors", "publish", "author_list", "publish_name",)
        extra_kwargs = {
            "book_name": {
                "required": True,
                "min_length": 5,
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "图书名长度不够"
                }
            },
            "authors": {
                "write_only": True  # 只参与反序列化
            },
            "publish": {
                "write_only": True
            },
            "author_list": {
                "read_only": True  # 序列化
            },
            "publish_name": {
                "read_only": True
            },
            "pic": {
                "read_only": True
            },
        }

    def validate_book_name(self, value):
        if "D" in value:
            raise serializers.ValidationError("D图书已存在")
        else:
            return value

    def validate(self, attrs):
        publish = attrs.get("publish")
        book_name = attrs.get("book_name")
        book_obj = Book.objects.filter(book_name=book_name, publish=publish)
        if book_obj:
            raise serializers.ValidationError("该出版社已经发布过该图书")

        return attrs
